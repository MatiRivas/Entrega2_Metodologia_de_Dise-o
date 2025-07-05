from abc import abstractmethod
from .pedido import Pedido

class PedidoConCobro(Pedido):
    def __init__(self, id_pedido, estado, productos, cliente):
        super().__init__(id_pedido, estado, productos, cliente)
    
    @abstractmethod
    def sumar_cobro(self):
        pass
