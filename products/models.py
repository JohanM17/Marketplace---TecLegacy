from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', max_length=500)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.category.slug, self.slug])

    def get_add_to_cart_url(self):
        return reverse('cart:add_to_cart', args=[self.id])

    def can_user_review(self, user):
        """Verifica si el usuario puede dejar una reseña (compró y no ha reseñado)."""
        if not user.is_authenticated:
            return False
        
        # 1. ¿Ya reseñó este producto?
        already_reviewed = self.reviews.filter(user=user).exists()
        if already_reviewed:
            return False

        # 2. ¿Lo compró y el pedido fue entregado?
        # Accedemos a los pedidos del usuario, buscamos si algún ítem de esos pedidos es este producto
        from cart.models import Order
        has_purchased = Order.objects.filter(
            user=user, 
            status='entregado', 
            items__product=self
        ).exists()
        
        return has_purchased

    @property
    def average_rating(self):
        """Calcula el promedio de estrellas del producto."""
        from django.db.models import Avg
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def star_range(self):
        return range(int(self.average_rating))

    @property
    def empty_star_range(self):
        return range(5 - int(self.average_rating))


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)  # Escala de 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'
        ordering = ['-created_at']
        unique_together = ('product', 'user')  # Un usuario solo puede dejar una reseña por producto

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.rating})'

    @property
    def star_range(self):
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)
