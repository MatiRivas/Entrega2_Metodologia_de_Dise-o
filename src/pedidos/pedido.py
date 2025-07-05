from abc import ABC, abstractmethod
from .estado_pedido import EstadoPedido

class Pedido(ABC):
    def __init__(self, id_pedido, estado, productos, cliente):
        self.id = id_pedido
        self.estado = estado
        self.productos = productos  # dict {Producto: cantidad}
        self.cliente = cliente
    
    def cambiar_estado(self, nuevo_estado):
        if self._es_transicion_valida(self.estado, nuevo_estado):
            anterior = self.estado
            self.estado = nuevo_estado
            print(f"Cambio exitoso: {anterior.value} > {nuevo_estado.value}")
            return True
        else:
            print(f"Transición inválida: {self.estado.value} > {nuevo_estado.value}")
            return False
    
    def _es_transicion_valida(self, actual, nuevo):
        transiciones = {
            EstadoPedido.PENDIENTE: [EstadoPedido.PAGADO],
            EstadoPedido.PAGADO: [EstadoPedido.EN_PREPARACION, EstadoPedido.CANCELADO],
            EstadoPedido.EN_PREPARACION: [EstadoPedido.ENVIADO, EstadoPedido.CANCELADO],
            EstadoPedido.ENVIADO: [],
            EstadoPedido.CANCELADO: []
        }
        return nuevo in transiciones.get(actual, [])
    
    def calcular_total(self):
        subtotal = 0
        for producto, cantidad in self.productos.items():
            subtotal += producto.get_precio() * cantidad
        
        descuento = subtotal * self.cliente.get_descuento()
        total = subtotal - descuento
        return total
    
    def descontar_stock_de_productos(self):
        for producto, cantidad in self.productos.items():
            producto.descontar_stock(cantidad)
    
    def get_cliente(self):
        return self.cliente
    
    def get_id(self):
        return self.id
    
    def get_productos(self):
        return self.productos
    
    def get_estado(self):
        return self.estado
    
    def set_estado(self, estado):
        self.estado = estado
