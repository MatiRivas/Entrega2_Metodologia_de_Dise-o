import uuid
from src.pagos.gestor_metodos_pago import GestorMetodosPago
from src.pagos.pago_tarjeta import PagoTarjeta
from src.pagos.pago_QR import PagoQR
from src.pagos.proxy_pagoQR import ProxyPagoQR
from src.auditoria.registro_transacciones import RegistroTransacciones
from src.seguridad.gestor_tokens_temporales import GestorTokensTemporales
from src.cliente.cliente_concreto import Cliente
from api.modelos.schemas import PagoRequest, PagoResponse

class PagoService:
    """Servicio para gestionar operaciones de pago"""
    
    def __init__(self):
        self.gestor_pagos = GestorMetodosPago()
        self.registro_transacciones = RegistroTransacciones(archivo_log="log_uvshop_transacciones_qr.log")
        self.gestor_tokens = GestorTokensTemporales()
        
        # Configurar métodos de pago
        self._configurar_metodos_pago()
    
    def _configurar_metodos_pago(self):
        """Configura los métodos de pago disponibles en el sistema"""
        # Registrar tarjeta
        self.gestor_pagos.registrar_metodo("tarjeta", PagoTarjeta())
        
        # Registrar QR con proxy
        pago_qr_real = PagoQR()
        proxy_pago_qr = ProxyPagoQR(
            metodo_pago_real=pago_qr_real,
            registro=self.registro_transacciones,
            gestor_tokens=self.gestor_tokens
        )
        self.gestor_pagos.registrar_metodo("qr", proxy_pago_qr)
    
    def procesar_pago(self, pago_request: PagoRequest, cliente: Cliente) -> PagoResponse:
        """Procesa un pago usando el método especificado"""
        # Obtener método de pago
        metodo_pago = self.gestor_pagos.obtener_metodo(pago_request.metodo_pago)
        if not metodo_pago:
            raise ValueError("Método de pago no válido")
        
        # Generar ID de transacción
        transaction_id = str(uuid.uuid4())
        
        # Procesar pago según el método
        if pago_request.metodo_pago == "qr":
            if not pago_request.token_temporal:
                raise ValueError("Token temporal requerido para pago QR")
            
            # Configurar datos QR en el proxy usando el nuevo método
            metodo_pago.set_datos_qr(cliente, pago_request.token_temporal)
            resultado = metodo_pago.procesar_pago(pago_request.monto)
        else:
            resultado = metodo_pago.procesar_pago(pago_request.monto)
        
        return PagoResponse(
            success=resultado,
            message="Pago procesado exitosamente" if resultado else "Pago fallido",
            metodo_pago=pago_request.metodo_pago,
            monto=pago_request.monto,
            cliente_email=pago_request.cliente_email,
            transaction_id=transaction_id if resultado else None
        )
    
    def obtener_metodos_disponibles(self) -> list:
        """Obtiene la lista de métodos de pago disponibles"""
        return ["tarjeta", "qr"]
