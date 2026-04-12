from django.conf import settings
from .providers.stripe_provider import StripeProvider
# from .providers.mercadopago_provider import MercadoPagoProvider # Futuro

def get_payment_provider():
    """
    Factory que retorna la instancia del proveedor configurado en settings.
    """
    provider_name = getattr(settings, 'PAYMENT_PROVIDER', 'stripe')
    
    if provider_name == 'stripe':
        return StripeProvider()
    # elif provider_name == 'mercadopago':
    #     return MercadoPagoProvider()
    
    raise ValueError(f"Proveedor de pago '{provider_name}' no soportado.")
