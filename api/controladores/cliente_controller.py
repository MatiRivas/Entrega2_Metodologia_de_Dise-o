from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.modelos.schemas import ClienteRequest, ClienteResponse
from api.servicios.cliente_service import ClienteService
from api.dependencies import get_cliente_service

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]
)


@router.post("/", response_model=dict)
async def crear_cliente(
    cliente_request: ClienteRequest,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    """Crea un nuevo cliente"""
    try:
        cliente_response = cliente_service.crear_cliente(cliente_request)
        return {
            "message": "Cliente creado exitosamente",
            "cliente": cliente_response.dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=dict)
async def listar_clientes(
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    """Lista todos los clientes"""
    try:
        clientes = cliente_service.listar_clientes()
        return {
            "clientes": [cliente.dict() for cliente in clientes]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{email}")
async def obtener_cliente(
    email: str,
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    """Obtiene un cliente por email"""
    try:
        cliente = cliente_service.obtener_cliente(email)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        return {
            "cliente": {
                "email": cliente.get_email(),
                "nombre": cliente.get_nombre(),
                "tipo": cliente.get_tipo_cliente().value,
                "descuento": cliente.get_descuento(),
                "direccion": cliente.get_direccion()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
