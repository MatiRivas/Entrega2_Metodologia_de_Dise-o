from .metodo_pago import MetodoPago
from .pago_QR import PagoQR
from src.auditoria.registro_transacciones import RegistroTransacciones
from src.seguridad.gestor_tokens_temporales import GestorTokensTemporales
from src.cliente.cliente_concreto import Cliente # Para tipo hinting

import uuid # Para generar IDs de transacción únicos

class ProxyPagoQR(MetodoPago):
    def __init__(self, metodo_pago_real: PagoQR, registro: RegistroTransacciones, gestor_tokens: GestorTokensTemporales):
        # Es una buena práctica verificar que el objeto envuelto sea del tipo esperado
        if not isinstance(metodo_pago_real, PagoQR):
            raise TypeError("ProxyPagoQR debe envolver una instancia de PagoCodigoQR.")
        
        self._cliente_actual = None
        self._token_actual = None
        self._metodo_pago_real = metodo_pago_real
        self._registro = registro
        self._gestor_tokens = gestor_tokens
    
    def set_datos_qr(self, cliente: Cliente, token_temporal: str):
        self._cliente_actual = cliente
        self._token_actual = token_temporal

    def procesar_pago(self, monto: float) -> bool:
        Cliente =self._cliente_actual
        token_temporal = self._token_actual
        
        # Validar que el cliente y el token son proporcionados (son cruciales para este proxy)
        if not Cliente or not token_temporal:
            print("[ProxyPagoQR] Error: Datos QR no establecidos")
            return False

        transaccion_id = str(uuid.uuid4())
        cliente_email = Cliente.get_email()

        print(f"\n[ProxyPagoQR] --- Iniciando flujo de pago QR para {cliente_email} (ID Transacción: {transaccion_id}) ---")

        # 1. Autenticación con tokens temporales
        if not self._gestor_tokens.validar_token(token_temporal, cliente_email):
            self._registro.registrar_fallida(transaccion_id, monto, "QR", cliente_email, "Token temporal inválido o expirado")
            print("  [ProxyPagoQR] Autenticación con token fallida. Pago abortado.")
            return False
        
        # 2. Validaciones adicionales (geolocalización, IP segura)
        print(f"  [ProxyPagoQR] Simulando validación de geolocalización para cliente {cliente_email}...")
        
        print(f"  [ProxyPagoQR] Simulando validación de IP segura para cliente {cliente_email}...")
        
        print("[ProxyPagoQR] Todas las validaciones de seguridad (token, geolocalización, IP) pasaron. Delegando al sujeto real.")

        # 3. Delegar al Sujeto Real (PagoCodigoQR)
        try:
            
            exito_pago_real = self._metodo_pago_real.procesar_pago(monto, cliente=Cliente) 
            
            # 4. Registro de Transacciones Exitosas y Fallidas
            if exito_pago_real:
                self._registro.registrar_exitosa(transaccion_id, monto, "QR", cliente_email)
                print("[ProxyPagoQR] Pago QR procesado exitosamente por la pasarela real y registrado.")
                return True
            else:
                # El sujeto real retornó False, significa que la pasarela lo rechazó
                self._registro.registrar_fallida(transaccion_id, monto, "QR", cliente_email, "Pago rechazado por la pasarela real (retorno False)")
                print("[ProxyPagoQR] Pago QR rechazado por la pasarela real y registrado como fallido.")
                return False
        except Exception as e:
            # Captura cualquier excepción que ocurra durante el procesamiento del pago real
            self._registro.registrar_fallida(transaccion_id, monto, "QR", cliente_email, f"Error inesperado durante el procesamiento real: {str(e)}")
            print(f"[ProxyPagoQR] Error crítico al procesar pago QR: {e}. Registrado como fallido.")
            return False