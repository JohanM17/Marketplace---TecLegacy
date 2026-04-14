from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import models
from .models import Category, Product, Review

def index(request):
    """Vista de la página principal con productos destacados."""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'products/index.html', context)


def product_list(request, category_slug=None):
    """Lista de productos, puede filtrarse por categoría."""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    # Paginación: 12 productos por página
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, category_slug, product_slug):
    """Detalle de un producto específico."""
    product = get_object_or_404(
        Product,
        slug=product_slug,
        category__slug=category_slug,
        is_available=True
    )

    # Productos relacionados: misma categoría, excepto el actual
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'can_review': product.can_user_review(request.user)
    }
    return render(request, 'products/product_detail.html', context)


def search_products(request):
    """Búsqueda de productos."""
    query = request.GET.get('q', '')
    products = []

    if query:
        # Buscar por nombre, descripción o categoría
        products = Product.objects.filter(
            is_available=True
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)


def search_autocomplete(request):
    """API para autocompletado en vivo del buscador."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})
        
    products = Product.objects.filter(is_available=True).filter(
        models.Q(name__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(category__name__icontains=query)
    ).distinct()[:5]  # Limitamos a 5 resultados rápidos
    
    results = []
    for p in products:
        results.append({
            'name': p.name,
            'price': float(p.price),
            'url': f"/products/{p.category.slug}/{p.slug}/",
            'image_url': p.image.url if p.image else ''
        })
        
    return JsonResponse({'results': results})


@login_required
def add_review(request, product_id):
    """Procesa el envío de una nueva reseña vía AJAX."""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Verificación extra de seguridad en el servidor
        if not product.can_user_review(request.user):
            return JsonResponse({
                'success': False, 
                'message': 'No cumples los requisitos para reseñar este producto.'
            })
            
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        
        # Validación de longitud
        if len(comment) < 100:
            return JsonResponse({
                'success': False, 
                'message': f'Tu reseña es muy corta ({len(comment)} caracteres). Por favor, escribe al menos 100 caracteres para ayudar a otros compradores.'
            })
        
        if len(comment) > 3000:
            return JsonResponse({
                'success': False, 
                'message': 'Tu reseña es demasiado larga. El máximo son 3000 caracteres.'
            })
        
        if rating and comment:
            try:
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=int(rating),
                    comment=comment
                )
                return JsonResponse({
                    'success': True, 
                    'message': '¡Tu reseña ha sido publicada con éxito!'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'message': 'Hubo un error al guardar tu reseña.'
                })
                
    return JsonResponse({'success': False, 'message': 'Petición no válida.'})


def error_404(request, exception):
    """Vista personalizada para error 404."""
    return render(request, '404.html', status=404)


def error_500(request):
    """Vista personalizada para error 500."""
    return render(request, '500.html', status=500)