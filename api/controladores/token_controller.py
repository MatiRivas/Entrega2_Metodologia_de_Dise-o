from fastapi import APIRouter, HTTPException, Depends
from api.modelos.schemas import TokenRequest, TokenResponse
from api.servicios.token_service import TokenService
from api.servicios.cliente_service import ClienteService
from api.dependencies import get_token_service, get_cliente_service

router = APIRouter(
    prefix="/tokens",
    tags=["tokens"]
)


@router.post("/generar", response_model=TokenResponse)
async def generar_token(
    token_request: TokenRequest,
    token_service: TokenService = Depends(get_token_service),
    cliente_service: ClienteService = Depends(get_cliente_service)
):
    """Genera un token temporal para un cliente"""
    try:
        # Verificar que el cliente existe
        if not cliente_service.cliente_existe(token_request.cliente_email):
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        token_response = token_service.generar_token(token_request)
        return token_response
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/validar")
async def validar_token(
    token: str,
    cliente_email: str,
    token_service: TokenService = Depends(get_token_service)
):
    """Valida un token temporal"""
    try:
        es_valido = token_service.validar_token(token, cliente_email)
        return {
            "valid": es_valido,
            "message": "Token válido" if es_valido else "Token inválido o expirado"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
