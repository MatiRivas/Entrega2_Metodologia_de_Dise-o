from .pedido_cambio_fecha import PedidoCambioFecha

class ExpressPedido(PedidoCambioFecha):
    def __init__(self, id_pedido, estado, productos, cliente, cargo_extra):
        super().__init__(id_pedido, estado, productos, cliente)
        self.cargo_extra = cargo_extra
    
    def cambiar_fecha(self):
        print("La fecha del pedido express ha sido cambiada.")
    
    def sumar_cobro(self):
        total = super().calcular_total()
        return total + self.cargo_extra
