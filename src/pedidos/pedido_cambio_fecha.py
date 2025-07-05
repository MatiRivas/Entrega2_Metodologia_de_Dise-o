from abc import abstractmethod
from .pedido import Pedido

class PedidoCambioFecha(Pedido):
    def __init__(self, id_pedido, estado, productos, cliente):
        super().__init__(id_pedido, estado, productos, cliente)
    
    @abstractmethod
    def cambiar_fecha(self):
        pass
