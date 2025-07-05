from .pedido import Pedido

class EstandarPedido(Pedido):
    def __init__(self, id_pedido, estado, productos, cliente):
        super().__init__(id_pedido, estado, productos, cliente)
