from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    Fusiona el carrito anónimo con el del usuario al iniciar sesión.
    Funciona para login por email/contraseña y por Google OAuth.

    Técnica: _cart_session_id se guarda en los datos de sesión cuando el usuario
    anónimo añade al carrito. Django copia esos datos al rotar la session key
    durante el login (cycle_key), por lo que el valor sigue disponible aquí.
    """
    cart_session_id = request.session.get('_cart_session_id')
    if not cart_session_id:
        return

    try:
        session_cart = Cart.objects.get(session_id=cart_session_id)
    except Cart.DoesNotExist:
        return

    if not session_cart.items.exists():
        session_cart.delete()
        return

    # Obtener o crear el carrito del usuario
    user_cart, _ = Cart.objects.get_or_create(user=user)

    # Fusionar ítem por ítem usando filter().first() (robusto ante DoesNotExist sobrescrito)
    for session_item in session_cart.items.all():
        existing = user_cart.items.filter(product=session_item.product).first()
        if existing:
            new_qty = existing.quantity + session_item.quantity
            existing.quantity = min(new_qty, session_item.product.stock)
            existing.save()
        else:
            session_item.cart = user_cart
            session_item.save()

    session_cart.delete()

    # Limpiar la clave temporal de sesión
    try:
        del request.session['_cart_session_id']
    except KeyError:
        pass
