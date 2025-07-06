from .cliente_decorator import ClienteDecorator

class DescuentoExtraDecorator(ClienteDecorator):
    def __init__(self, cliente, extra):
        super().__init__(cliente)
        self.extra = extra
    def get_descuento(self):
        return self._cliente.get_descuento() + self.extra
