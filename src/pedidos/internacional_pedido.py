from .pedido_con_cobro import PedidoConCobro

class InternacionalPedido(PedidoConCobro):
    def __init__(self, id_pedido, estado, productos, cliente, cobro_aduana):
        super().__init__(id_pedido, estado, productos, cliente)
        self.impuesto_aduana = cobro_aduana
    
    def sumar_cobro(self):
        total = super().calcular_total()
        return total + self.impuesto_aduana
