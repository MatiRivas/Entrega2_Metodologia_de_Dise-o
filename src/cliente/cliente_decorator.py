from .cliente_base import ClienteBase

class ClienteDecorator(ClienteBase):
    def __init__(self, cliente):
        self._cliente = cliente
    def get_descuento(self):
        return self._cliente.get_descuento()
    def tiene_envio_gratis(self):
        return self._cliente.tiene_envio_gratis()
    def get_nombre(self):
        return self._cliente.get_nombre()
    def get_tipo_cliente(self):
        return self._cliente.get_tipo_cliente()
    def get_direccion(self):
        return self._cliente.get_direccion()
