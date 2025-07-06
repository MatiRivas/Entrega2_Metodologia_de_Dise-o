# src/pagos/proxy_pago.py
from .metodo_pago import MetodoPago

class ProxyPago(MetodoPago):
    def __init__(self, metodo_pago, cliente):
        self.metodo_pago = metodo_pago
        self.cliente = cliente

    def procesar_pago(self, monto, **kwargs):
        if not self.verificar_datos_cliente():
            print('Datos del cliente inválidos')
            return False
        if not self.control_fraude(monto):
            print('Fraude o límite detectado')
            return False
        self.registrar_auditoria(monto)
        return self.metodo_pago.procesar_pago(monto)

    def verificar_datos_cliente(self):
        # Ejemplo: verifica que el email y dirección no estén vacíos
        return bool(getattr(self.cliente, 'email', None)) and bool(self.cliente.get_direccion())

    def control_fraude(self, monto):
        # Ejemplo: rechaza pagos mayores a 1_000_000
        return monto <= 1_000_000

    def registrar_auditoria(self, monto):
        print(f'Auditoría: Cliente {self.cliente.get_nombre()} pagó {monto}')