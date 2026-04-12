from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_confirmation_email(order):
    """
    Envía un correo electrónico de confirmación de pedido al cliente.
    """
    subject = f'Confirmación de Pedido TecLegacy #{order.id}'
    
    # Contexto para la plantilla
    context = {
        'order': order,
        'items': order.items.all(),
    }
    
    # Renderizar el HTML del correo (crearemos esta plantilla luego)
    html_message = render_to_string('cart/emails/order_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False
