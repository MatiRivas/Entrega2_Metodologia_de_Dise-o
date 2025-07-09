from .metodo_pago import MetodoPago

class PagoTarjeta(MetodoPago):
    def procesar_pago(self, monto):
        print(f"Procesando pago con tarjeta por ${monto}")
        return True
