from src.seguridad.gestor_tokens_temporales import GestorTokensTemporales
from api.modelos.schemas import TokenRequest, TokenResponse

class TokenService:
    """Servicio para gestionar tokens temporales"""
    
    def __init__(self):
        self.gestor_tokens = GestorTokensTemporales()
    
    def generar_token(self, cliente_email: str) -> TokenResponse:
        """Genera un token temporal para un cliente"""
        token = self.gestor_tokens.generar_token(cliente_email)
        
        return TokenResponse(
            token=token,
            expires_in_seconds=self.gestor_tokens.TOKEN_EXPIRATION_SECONDS,
            cliente_email=cliente_email
        )
    
    def validar_token(self, token: str, cliente_email: str) -> bool:
        """Valida un token temporal"""
        return self.gestor_tokens.validar_token(token, cliente_email)
