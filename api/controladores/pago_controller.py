from fastapi import APIRouter, HTTPException, Depends
from api.modelos.schemas import PagoRequest, PagoResponse
from api.servicios.pago_service import PagoService
from api.servicios.cliente_service import ClienteService
from api.dependencies import get_pago_service, get_cliente_service

router = APIRouter(
    prefix="/pagos",
    tags=["pagos"]
)


@router.post("/procesar", response_model=PagoResponse)
async def procesar_pago(
    pago_request: PagoRequest,
    pago_service: PagoService = Depends(get_pago_service),
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    """Procesa un pago usando el método especificado"""
    try:
        # Validar que el cliente existe
        cliente = cliente_service.obtener_cliente(pago_request.cliente_email)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Procesar el pago
        pago_response = pago_service.procesar_pago(pago_request, cliente)
        return pago_response
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/metodos")
async def obtener_metodos_pago(
    pago_service: PagoService = Depends(get_pago_service)
):
    """Obtiene la lista de métodos de pago disponibles"""
    try:
        metodos = pago_service.obtener_metodos_disponibles()
        return {
            "metodos_pago": metodos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
