from ..pedidos.estado_pedido import EstadoPedido

class Factura:
    def __init__(self, pedido):
        self.pedido = pedido
        self.pagado = pedido.get_estado() == EstadoPedido.PAGADO
        self.calcular_valores()
    
    def calcular_valores(self):
        self.total_bruto = self._calcular_total_bruto()
        self.descuento = self._calcular_descuento()
        self.impuesto = self._calcular_impuesto()
        self.monto_final = self.total_bruto - self.descuento + self.impuesto
    
    def _calcular_total_bruto(self):
        total = 0
        for producto, cantidad in self.pedido.get_productos().items():
            total += producto.get_precio() * cantidad
        return total
    
    def _calcular_descuento(self):
        cliente = self.pedido.get_cliente()
        return self.total_bruto * cliente.get_descuento()
    
    def _calcular_impuesto(self):
        # Simulación simple: si en la dirección aparece "internacional", aplicamos impuesto
        if "internacional" in self.pedido.get_cliente().get_direccion().lower():
            return self.total_bruto * 0.2  # 20% de impuesto aduanero
        return 0
    
    def imprimir_factura(self):
        print("----- FACTURA -----")
        print(f"Pedido ID: {self.pedido.get_id()}")
        print(f"Cliente: {self.pedido.get_cliente().get_nombre()}")
        print("Productos:")
        for producto, cantidad in self.pedido.get_productos().items():
            total_producto = producto.get_precio() * cantidad
            print(f" - {producto.get_nombre()} x{cantidad} = ${total_producto}")
        print(f"Total bruto: ${self.total_bruto}")
        print(f"Descuento aplicado: -${self.descuento}")
        print(f"Impuestos: +${self.impuesto}")
        print(f"Total final: ${self.monto_final}")
        print(f"Estado de pago: {'Pagado' if self.pagado else 'Pendiente'}")
        print("-------------------")
    
    def pagar_factura(self, nombre_metodo, gestor):
        if self.pagado:
            print("La factura ya esta pagada")
            return False
        
        if not gestor.existe_metodo(nombre_metodo):
            print(f"Metodo de pago no encontrado: {nombre_metodo}")
            return False
        
        metodo = gestor.obtener_metodo(nombre_metodo)
        exito = metodo.procesar_pago(self.monto_final)
        
        if exito:
            self.pagado = True
            self.pedido.cambiar_estado(EstadoPedido.PAGADO)
            print(f"Pago exitoso con {nombre_metodo}")
        else:
            print(f"Fallo al procesar el pago con {nombre_metodo}")
        
        return exito
    
    def get_total_bruto(self):
        return self.total_bruto
    
    def get_descuento(self):
        return self.descuento
    
    def get_impuesto(self):
        return self.impuesto
    
    def get_monto_final(self):
        return self.monto_final
    
    def is_pagado(self):
        return self.pagado
    
    def get_pedido(self):
        return self.pedido
