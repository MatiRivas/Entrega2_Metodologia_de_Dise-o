from pydantic import BaseModel
from typing import Optional, Dict

# === MODELOS DE REQUEST (Entrada) ===

class ClienteRequest(BaseModel):
    nombre: str
    email: str
    direccion: str
    tipo_cliente: str  # "VIP", "FRECUENTE", "NORMAL"

class ProductoRequest(BaseModel):
    nombre: str
    codigo: str
    precio: float
    stock: int

class PagoRequest(BaseModel):
    pedido_id: int
    metodo_pago: str  # "tarjeta" o "qr"
    monto: float
    cliente_email: str
    token_temporal: Optional[str] = None  # Solo para QR

class TokenRequest(BaseModel):
    cliente_email: str

# === MODELOS DE RESPONSE (Salida) ===

class ClienteResponse(BaseModel):
    email: str
    nombre: str
    tipo: str
    descuento: float
    direccion: str

class ProductoResponse(BaseModel):
    codigo: str
    nombre: str
    precio: float
    stock: int

class PagoResponse(BaseModel):
    success: bool
    message: str
    metodo_pago: str
    monto: float
    cliente_email: str
    transaction_id: Optional[str] = None

class TokenResponse(BaseModel):
    token: str
    expires_in_seconds: int
    cliente_email: str

# === MODELOS DE RESPUESTA GENERALES ===

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Dict] = None

class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: int
