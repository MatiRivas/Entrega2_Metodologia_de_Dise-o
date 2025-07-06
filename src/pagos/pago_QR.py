from .metodo_pago import MetodoPago

class PagoQR(MetodoPago):
    def procesar_pago(self, monto, **kwargs):
        if monto >= 50:
            print(f"Procesando pago con código QR por ${monto}")
            return True
        else: 
            print(f"Pago con código QR rechazado: monto mínimo es $50, recibido ${monto}")
            return False  # Rechaza pagos menores a $50