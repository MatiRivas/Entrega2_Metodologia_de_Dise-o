import datetime

class RegistroTransacciones:
    def __init__(self, archivo_log="transacciones.log"):
        self.archivo_log = archivo_log

    def _escribir_log(self, mensaje: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.archivo_log, "a") as f:
            f.write(f"[{timestamp}] {mensaje}\n")

    def registrar_exitosa(self, id_transaccion: str, monto: float, metodo: str, cliente_email: str):
        mensaje = f"TRANSACCION EXITOSA | ID: {id_transaccion} | Monto: {monto} | Metodo: {metodo} | Cliente: {cliente_email}"
        self._escribir_log(mensaje)
        print(f"[REGISTRO] Transacción exitosa: {id_transaccion}")

    def registrar_fallida(self, id_transaccion: str, monto: float, metodo: str, cliente_email: str, razon: str):
        mensaje = f"TRANSACCION FALLIDA | ID: {id_transaccion} | Monto: {monto} | Metodo: {metodo} | Cliente: {cliente_email} | Razon: {razon}"
        self._escribir_log(mensaje)
        print(f"[REGISTRO] Transacción fallida: {id_transaccion} - {razon}")