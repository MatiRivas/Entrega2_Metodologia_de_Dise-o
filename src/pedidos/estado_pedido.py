from enum import Enum

class EstadoPedido(Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    EN_PREPARACION = "EN_PREPARACION"
    ENVIADO = "ENVIADO"
    CANCELADO = "CANCELADO"
