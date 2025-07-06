from .metodo_pago import MetodoPago

class PagoQR(MetodoPago):
    def procesar_pago(self, monto, **kwargs):
        print(f"Procesando pago con código QR por ${monto}")
        return True