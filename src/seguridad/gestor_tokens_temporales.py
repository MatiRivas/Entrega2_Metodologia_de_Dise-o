import jwt
import datetime
from datetime import timezone, timedelta
import os

class GestorTokensTemporales:
    # Para fines académicos, la clave secreta se hardcodea.
    # ¡En un entorno real, DEBE obtenerse de variables de entorno o un servicio de secretos!
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_very_strong_and_secret_key_for_uvshop_2025")
    ALGORITHM = "HS256"
    TOKEN_EXPIRATION_SECONDS = 60 # Reducido a 60 segundos para pruebas más rápidas

    def generar_token(self, cliente_email: str) -> str:
        expire_time = datetime.datetime.now(timezone.utc) + timedelta(seconds=self.TOKEN_EXPIRATION_SECONDS)
        
        payload = {
            "sub": cliente_email,
            "exp": expire_time,
            "iat": datetime.datetime.now(timezone.utc)
        }
        
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        print(f"[TOKEN] Token temporal JWT generado para {cliente_email}. Expira en {self.TOKEN_EXPIRATION_SECONDS} minutos (UTC: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}).")
        return token

    def validar_token(self, token: str, cliente_email: str) -> bool:
        print(f"[TOKEN] Intentando validar token '{token}' para '{cliente_email}'...")
        try:
            decoded_payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            
            if decoded_payload.get("sub") != cliente_email:
                print(f"[TOKEN] Validación fallida: Token no corresponde al cliente {cliente_email}. (Token sub: {decoded_payload.get('sub')})")
                return False
                
            print(f"[TOKEN] Token válido para {cliente_email}.")
            return True
            
        except jwt.ExpiredSignatureError:
            print(f"[TOKEN] Validación fallida: Token expirado para {cliente_email}.")
            return False
        except jwt.InvalidTokenError as e:
            print(f"[TOKEN] Validación fallida: Token inválido para {cliente_email}. Error: {e}")
            return False
        except Exception as e:
            print(f"[TOKEN] Error desconocido al validar token: {e}")
            return False