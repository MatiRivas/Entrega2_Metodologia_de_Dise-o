from fastapi import APIRouter
from api.controladores.cliente_controller import router as cliente_router
from api.controladores.producto_controller import router as producto_router
from api.controladores.token_controller import router as token_router
from api.controladores.pago_controller import router as pago_router
from api.controladores.health_controller import router as health_router

# Router principal que incluye todos los sub-routers
api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(cliente_router)
api_router.include_router(producto_router)
api_router.include_router(token_router)
api_router.include_router(pago_router)
api_router.include_router(health_router)

# Endpoint raíz
@api_router.get("/")
async def root():
    return {"message": "UVShop API - Sistema de Pagos con QR"}
