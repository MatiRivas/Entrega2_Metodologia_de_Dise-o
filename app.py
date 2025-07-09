from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar el router principal de la capa de controladores
from api.controladores.main_router import api_router

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
    allow_headers=["*"]
)

# Incluir todas las rutas de la API
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
