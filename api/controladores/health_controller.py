from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"]
)


@router.get("/")
async def health_check():
    """Endpoint de salud del sistema"""
    return {
        "status": "healthy", 
        "service": "UVShop API"
    }


@router.get("/info")
async def info():
    """Información del sistema"""
    return {
        "name": "UVShop API",
        "version": "1.0.0",
        "description": "API para el sistema de pagos UVShop con soporte para QR"
    }
