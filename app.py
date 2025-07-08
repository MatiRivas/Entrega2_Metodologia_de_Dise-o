from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

# Imports de tu sistema existente
from src.cliente.cliente_concreto import Cliente
from src.cliente.tipo_cliente import TipoCliente
from src.producto.producto import Producto
from src.pedidos.estado_pedido import EstadoPedido
from src.pedidos.estandar_pedido import EstandarPedido
from src.pagos.gestor_metodos_pago import GestorMetodosPago
from src.pagos.pago_tarjeta import PagoTarjeta
from src.pagos.pago_QR import PagoQR
from src.pagos.proxy_pagoQR import ProxyPagoQR
from src.auditoria.registro_transacciones import RegistroTransacciones
from src.seguridad.gestor_tokens_temporales import GestorTokensTemporales
from src.factura.factura import Factura

# Inicializar FastAPI
app = FastAPI(
    title="UVShop API",
    description="API para el sistema de pagos UVShop con soporte para QR",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias globales (en producción, usar dependency injection)
gestor_pagos = GestorMetodosPago()
registro_transacciones = RegistroTransacciones(archivo_log="log_uvshop_transacciones_qr.log")
gestor_tokens = GestorTokensTemporales()

# Configurar métodos de pago
gestor_pagos.registrar_metodo("tarjeta", PagoTarjeta())
pago_qr_real = PagoQR()
proxy_pago_qr = ProxyPagoQR(
    metodo_pago_real=pago_qr_real,
    registro=registro_transacciones,
    gestor_tokens=gestor_tokens
)
gestor_pagos.registrar_metodo("qr", proxy_pago_qr)

# Modelos Pydantic para las requests
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

class PedidoRequest(BaseModel):
    cliente: ClienteRequest
    productos: Dict[str, int]  # {codigo_producto: cantidad}

class PagoRequest(BaseModel):
    pedido_id: int
    metodo_pago: str  # "tarjeta" o "qr"
    monto: float
    cliente_email: str
    token_temporal: Optional[str] = None  # Solo para QR

class TokenRequest(BaseModel):
    cliente_email: str

# Almacenamiento temporal (en producción usar base de datos)
clientes_db = {}
productos_db = {}
pedidos_db = {}

@app.get("/")
async def root():
    return {"message": "UVShop API - Sistema de Pagos con QR"}

@app.post("/clientes")
async def crear_cliente(cliente_request: ClienteRequest):
    try:
        tipo_cliente = TipoCliente(cliente_request.tipo_cliente)
        cliente = Cliente(
            cliente_request.nombre,
            cliente_request.email,
            cliente_request.direccion,
            tipo_cliente
        )
        clientes_db[cliente_request.email] = cliente
        return {
            "message": "Cliente creado exitosamente",
            "cliente": {
                "email": cliente.get_email(),
                "nombre": cliente.get_nombre(),
                "tipo": cliente.get_tipo_cliente().value,
                "descuento": cliente.get_descuento()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/productos")
async def crear_producto(producto_request: ProductoRequest):
    try:
        producto = Producto(
            producto_request.nombre,
            producto_request.codigo,
            producto_request.precio,
            producto_request.stock
        )
        productos_db[producto_request.codigo] = producto
        return {
            "message": "Producto creado exitosamente",
            "producto": {
                "codigo": producto.get_codigo(),
                "nombre": producto.get_nombre(),
                "precio": producto.get_precio(),
                "stock": producto.get_stock()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tokens/generar")
async def generar_token(token_request: TokenRequest):
    try:
        if token_request.cliente_email not in clientes_db:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        token = gestor_tokens.generar_token(token_request.cliente_email)
        return {
            "token": token,
            "expires_in_seconds": gestor_tokens.TOKEN_EXPIRATION_SECONDS,
            "cliente_email": token_request.cliente_email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/pagos/procesar")
async def procesar_pago(pago_request: PagoRequest):
    try:
        # Validar cliente
        if pago_request.cliente_email not in clientes_db:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        cliente = clientes_db[pago_request.cliente_email]
        
        # Obtener método de pago
        metodo_pago = gestor_pagos.obtener_metodo(pago_request.metodo_pago)
        if not metodo_pago:
            raise HTTPException(status_code=400, detail="Método de pago no válido")
        
        # Procesar pago según el método
        if pago_request.metodo_pago == "qr":
            if not pago_request.token_temporal:
                raise HTTPException(status_code=400, detail="Token temporal requerido para pago QR")
            
            resultado = metodo_pago.procesar_pago(
                pago_request.monto,
                cliente=cliente,
                token_temporal=pago_request.token_temporal
            )
        else:
            resultado = metodo_pago.procesar_pago(pago_request.monto)
        
        return {
            "success": resultado,
            "message": "Pago procesado exitosamente" if resultado else "Pago fallido",
            "metodo_pago": pago_request.metodo_pago,
            "monto": pago_request.monto,
            "cliente_email": pago_request.cliente_email
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/productos")
async def listar_productos():
    productos = []
    for codigo, producto in productos_db.items():
        productos.append({
            "codigo": producto.get_codigo(),
            "nombre": producto.get_nombre(),
            "precio": producto.get_precio(),
            "stock": producto.get_stock()
        })
    return {"productos": productos}

@app.get("/clientes")
async def listar_clientes():
    clientes = []
    for email, cliente in clientes_db.items():
        clientes.append({
            "email": cliente.get_email(),
            "nombre": cliente.get_nombre(),
            "tipo": cliente.get_tipo_cliente().value,
            "descuento": cliente.get_descuento()
        })
    return {"clientes": clientes}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "UVShop API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
