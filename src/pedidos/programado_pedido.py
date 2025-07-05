from .pedido_cambio_fecha import PedidoCambioFecha

class ProgramadoPedido(PedidoCambioFecha):
    def __init__(self, id_pedido, estado, productos, cliente, fecha_entrega):
        super().__init__(id_pedido, estado, productos, cliente)
        self.fecha_entrega = fecha_entrega
    
    def cambiar_fecha(self):
        print("La fecha del pedido programado ha sido cambiada al día elegido.")
