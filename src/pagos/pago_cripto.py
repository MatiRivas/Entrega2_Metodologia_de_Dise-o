from .metodo_pago import MetodoPago

class PagoCripto(MetodoPago):
    def procesar_pago(self, monto, **kwargs):
        print(f"Procesando pago con criptomoneda por ${monto}")
        return True
