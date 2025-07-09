from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.modelos.schemas import ProductoRequest, ProductoResponse
from api.servicios.producto_service import ProductoService
from api.dependencies import get_producto_service

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)


@router.post("/", response_model=dict)
async def crear_producto(
    producto_request: ProductoRequest,
    producto_service: ProductoService = Depends(get_producto_service)
):
    """Crea un nuevo producto"""
    try:
        producto_response = producto_service.crear_producto(producto_request)
        return {
            "message": "Producto creado exitosamente",
            "producto": producto_response.dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=dict)
async def listar_productos(
    producto_service: ProductoService = Depends(get_producto_service)
):
    """Lista todos los productos"""
    try:
        productos = producto_service.listar_productos()
        return {
            "productos": [producto.dict() for producto in productos]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{codigo}")
async def obtener_producto(
    codigo: str,
    producto_service: ProductoService = Depends(get_producto_service)
):
    """Obtiene un producto por código"""
    try:
        producto = producto_service.obtener_producto(codigo)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return {
            "producto": {
                "codigo": producto.get_codigo(),
                "nombre": producto.get_nombre(),
                "precio": producto.get_precio(),
                "stock": producto.get_stock()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
