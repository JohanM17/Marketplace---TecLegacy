from abc import ABC, abstractmethod

class PaymentProvider(ABC):
    """
    Clase base abstracta (Interfaz) para los proveedores de pago.
    Todos los proveedores (Stripe, MercadoPago, etc.) deben heredar de aquí.
    """

    @abstractmethod
    def create_checkout_session(self, order, success_url, cancel_url):
        """
        Crea una sesión de pago y devuelve una URL para redirigir al cliente.
        """
        pass

    @abstractmethod
    def verify_webhook(self, payload, sig_header):
        """
        Verifica que la notificación del webhook provenga realmente del proveedor.
        """
        pass

    @abstractmethod
    def handle_webhook_event(self, event):
        """
        Gestiona el evento recibido (ej. pago aprobado, rechazado).
        """
        pass
