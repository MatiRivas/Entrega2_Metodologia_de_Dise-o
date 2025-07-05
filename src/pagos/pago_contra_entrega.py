from .metodo_pago import MetodoPago

class PagoContraEntrega(MetodoPago):
    def procesar_pago(self, monto):
        print(f"Pago contra entrega: ${monto}")
        return True
