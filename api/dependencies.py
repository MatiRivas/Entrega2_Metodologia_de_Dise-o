"""
Configuración de dependencias para la aplicación.
Manejo de instancias singleton para servicios compartidos.
"""

from api.servicios.cliente_service import ClienteService
from api.servicios.producto_service import ProductoService
from api.servicios.token_service import TokenService
from api.servicios.pago_service import PagoService

# Instancias singleton de servicios
_cliente_service_instance = None
_producto_service_instance = None
_token_service_instance = None
_pago_service_instance = None


def get_cliente_service() -> ClienteService:
    """Obtiene la instancia singleton del servicio de clientes"""
    global _cliente_service_instance
    if _cliente_service_instance is None:
        _cliente_service_instance = ClienteService()
    return _cliente_service_instance


def get_producto_service() -> ProductoService:
    """Obtiene la instancia singleton del servicio de productos"""
    global _producto_service_instance
    if _producto_service_instance is None:
        _producto_service_instance = ProductoService()
    return _producto_service_instance


def get_token_service() -> TokenService:
    """Obtiene la instancia singleton del servicio de tokens"""
    global _token_service_instance
    if _token_service_instance is None:
        _token_service_instance = TokenService()
    return _token_service_instance


def get_pago_service() -> PagoService:
    """Obtiene la instancia singleton del servicio de pagos"""
    global _pago_service_instance
    if _pago_service_instance is None:
        _pago_service_instance = PagoService()
    return _pago_service_instance
