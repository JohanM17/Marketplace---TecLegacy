import stripe
from decouple import config
from .base import PaymentProvider

class StripeProvider(PaymentProvider):
    def __init__(self):
        stripe.api_key = config('STRIPE_SECRET_KEY')
        self.webhook_secret = config('STRIPE_WEBHOOK_SECRET', default='')

    def create_checkout_session(self, order, success_url, cancel_url):
        # Preparar los line_items con los productos de la orden
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'cop',
                    'product_data': {
                        'name': item.product.name,
                        # Solo enviamos la imagen si la URL es absoluta (empieza con http)
                        # En localhost, Stripe rechaza las URLs relativas
                        'images': [item.product.image.url] if item.product.image and item.product.image.url.startswith('http') else [],
                    },
                    'unit_amount': int(item.product.price * 100), # Stripe usa centavos
                },
                'quantity': item.quantity,
            })

        # Crear la sesión en Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(order.id),
            customer_email=order.email,
        )
        return session.url

    def verify_webhook(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            return event
        except Exception:
            return None

    def handle_webhook_event(self, event):
        # Aquí manejaremos el evento una vez verificado
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            return {
                'order_id': session.client_reference_id,
                'status': 'paid',
                'reference': session.payment_intent
            }
        return None
