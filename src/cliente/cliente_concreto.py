from .cliente_base import ClienteBase
from .tipo_cliente import TipoCliente

class Cliente(ClienteBase):
    def __init__(self, nombre, email, direccion, tipo_cliente):
        self.nombre = nombre
        self.email = email
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
    def get_descuento(self):
        descuentos = {
            TipoCliente.NUEVO: 0.05,
            TipoCliente.FRECUENTE: 0.10,
            TipoCliente.VIP: 0.15
        }
        return descuentos.get(self.tipo_cliente, 0.0)
    def tiene_envio_gratis(self):
        return self.tipo_cliente == TipoCliente.VIP
    def get_nombre(self):
        return self.nombre
    def get_tipo_cliente(self):
        return self.tipo_cliente
    def get_direccion(self):
        return self.direccion
    def get_email(self):
        return self.email
