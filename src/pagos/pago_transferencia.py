from .metodo_pago import MetodoPago

class PagoTransferencia(MetodoPago):
    def procesar_pago(self, monto):
        print(f"Procesando pago por transferencia de ${monto}")
        return True
