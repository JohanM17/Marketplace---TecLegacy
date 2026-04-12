from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from payments.factory import get_payment_provider
import json
import uuid


def _get_or_create_cart(request):
    """Función auxiliar para obtener o crear un carrito."""
    # Si el usuario está autenticado, busca su carrito
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    # Si no está autenticado, usa la sesión
    else:
        # Asegúrate de que la sesión exista
        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        # Guardar el ID en los datos de sesión — sobrevive la rotación de clave al hacer login
        request.session['_cart_session_id'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    return cart


def cart_detail(request):
    """Vista para mostrar el detalle del carrito."""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Añadir un producto al carrito."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = _get_or_create_cart(request)

    # Si la petición es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quantity = max(int(request.GET.get('quantity', 1)), 1)

        # Comprueba si el producto ya está en el carrito
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            new_quantity = cart_item.quantity + quantity
            # Tope de seguridad: nunca superar el stock disponible
            capped = new_quantity > product.stock
            cart_item.quantity = min(new_quantity, product.stock)
            cart_item.save()
        except CartItem.DoesNotExist:
            capped = quantity > product.stock
            cart_item = CartItem.objects.create(
                cart=cart, product=product,
                quantity=min(quantity, product.stock)
            )

        message = f'{product.name} añadido al carrito'
        if capped:
            message = f'Stock máximo alcanzado para {product.name} ({product.stock} disponibles)'

        # Devuelve respuesta JSON con información actualizada del carrito
        return JsonResponse({
            'success': True,
            'capped': capped,
            'message': message,
            'cart_quantity': cart_item.quantity,
            'cart_items_count': cart.get_total_items(),
            'cart_total': str(cart.get_total_price())
        })

    # Si la petición no es AJAX
    else:
        quantity = max(int(request.POST.get('quantity', 1)), 1)

        # Comprueba si el producto ya está en el carrito
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            new_quantity = cart_item.quantity + quantity
            capped = new_quantity > product.stock
            cart_item.quantity = min(new_quantity, product.stock)
            cart_item.save()
            if capped:
                messages.warning(request, f'Stock máximo alcanzado para {product.name}. Se ajustó a {product.stock} unidades disponibles.')
            else:
                messages.success(request, f'La cantidad de {product.name} ha sido actualizada en tu carrito')
        except CartItem.DoesNotExist:
            capped = quantity > product.stock
            cart_item = CartItem.objects.create(
                cart=cart, product=product,
                quantity=min(quantity, product.stock)
            )
            if capped:
                messages.warning(request, f'Stock máximo alcanzado. Se añadieron {product.stock} unidades de {product.name}.')
            else:
                messages.success(request, f'{product.name} ha sido añadido a tu carrito')

        return redirect('cart:cart_detail')


def update_cart(request):
    """Actualizar cantidades en el carrito."""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')

        cart_item = get_object_or_404(CartItem, id=item_id)

        if action == 'increase':
            # Validar stock antes de aumentar
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Stock máximo alcanzado'
                })
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'removed': True,
                    'cart_total': str(cart_item.cart.get_total_price()),
                    'cart_items_count': cart_item.cart.items.count()
                })
        elif action == 'remove':
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'removed': True,
                'cart_total': str(cart_item.cart.get_total_price()),
                'cart_items_count': cart_item.cart.items.count()
            })

        cart_item.save()

        return JsonResponse({
            'success': True,
            'item_total': str(cart_item.get_cost()),
            'quantity': cart_item.quantity,
            'cart_total': str(cart_item.cart.get_total_price()),
            'cart_items_count': cart_item.cart.items.count()
        })

    return JsonResponse({'success': False})


@login_required
def checkout(request):
    """Vista para el proceso de checkout."""
    cart = _get_or_create_cart(request)

    # Si el carrito está vacío, redirige a la vista del carrito
    if cart.items.count() == 0:
        messages.info(request, 'Tu carrito está vacío. Añade algunos productos antes de hacer checkout.')
        return redirect('cart:cart_detail')

    # Si es una petición POST, procesa el formulario de pedido
    if request.method == 'POST':
        # Validar que todos los campos necesarios estén presentes
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'country', 'postal_code',
                           'payment_method']

        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f'El campo {field} es obligatorio')
                return redirect('cart:checkout')

        # Crear un nuevo pedido
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            postal_code=request.POST.get('postal_code'),
            total_paid=cart.get_total_price(),
            payment_method=request.POST.get('payment_method')
        )

        # Crear items del pedido basados en el carrito
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # No vaciamos el carrito aquí todavía, lo haremos en payment_success
        return redirect('cart:payment_initiate', order_id=order.id)

    # Prepopular campos con información del perfil si existe
    initial_data = {}
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'country': profile.country,
            'postal_code': profile.postal_code
        }

    context = {
        'cart': cart,
        'initial_data': initial_data
    }
    return render(request, 'cart/checkout.html', context)


@login_required
def payment_initiate(request, order_id):
    """Vista para iniciar el proceso de pago con el proveedor configurado."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Obtener el proveedor desde el factory
    provider = get_payment_provider()
    
    # URLs de retorno
    success_url = request.build_absolute_uri(reverse('cart:payment_success', args=[order.id]))
    cancel_url = request.build_absolute_uri(reverse('cart:payment_cancel', args=[order.id]))
    
    try:
        # Esto genera la URL de Stripe (o el proveedor que sea)
        checkout_url = provider.create_checkout_session(order, success_url, cancel_url)
        return redirect(checkout_url)
    except Exception as e:
        messages.error(request, f"Error al iniciar el pago: {str(e)}")
        return redirect('cart:checkout')


@login_required
def payment_execute(request, order_id):
    """Vista para ejecutar el pago después de aprobación."""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Simular un pago exitoso
        payment_id = request.POST.get('payment_id', '')

        if not payment_id:
            # Generar un ID de pago simulado
            payment_id = f"PAY-{uuid.uuid4().hex[:16].upper()}"

        # Actualizar la orden
        order.payment_status = 'completado'
        order.payment_reference = payment_id
        order.status = 'procesando'  # El estado del pedido pasa a procesando
        order.save()

        messages.success(request, '¡Tu pago se ha procesado correctamente!')
        return redirect('cart:payment_success', order_id=order.id)

    return redirect('cart:payment_process', order_id=order_id)


@login_required
def payment_success(request, order_id):
    """Vista de éxito después del pago."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Para el demo, si llegamos aquí, asumimos que el pago fue exitoso
    if order.payment_status != 'completado':
        order.payment_status = 'completado'
        order.status = 'procesando'
        if not order.payment_reference:
            order.payment_reference = f"STRIPE-{uuid.uuid4().hex[:12].upper()}"
        order.save()
        
        # 1. ACTUALIZAR STOCK: Descontar productos del inventario
        for item in order.items.all():
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                # Caso borde: Se quedó sin stock en el proceso (se podría manejar un aviso)
                product.stock = 0
                product.save()

        # 2. LIMPIEZA: Vaciar el carrito solo cuando el pago es exitoso
        cart = _get_or_create_cart(request)
        cart.items.all().delete()
        
        # 3. NOTIFICACIÓN: Mensaje de éxito final y correo
        from .utils import send_order_confirmation_email
        send_order_confirmation_email(order)
        
        messages.success(request, f'¡Gracias por tu compra! El pedido #{order.id} ha sido confirmado.')

    context = {
        'order': order,
    }
    return render(request, 'cart/payment_success.html', context)


@login_required
def payment_cancel(request, order_id):
    """Vista para cancelar el pago."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Actualizar la orden
    order.payment_status = 'fallido'
    order.save()

    messages.warning(request, 'El pago ha sido cancelado.')
    return redirect('cart:checkout')
@login_required
def order_list(request):
    """Vista para listar todos los pedidos del usuario."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'cart/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Vista para ver el detalle de un pedido específico."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'cart/order_detail.html', context)
