from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, Response
from routers.main_router import router as main_router
from apis.FirebaseAuth import verificar_token
from constants import CORS_ORIGINS, ALLOWED_HOSTS
from firebase_admin_config import firebase_app

app = FastAPI()

app.include_router(main_router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Middleware que no permite peticiones de hosts no autorizados
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=ALLOWED_HOSTS
)

@app.middleware("http")
async def verificar_credenciales(peticion: Request, call_next) -> Response:
    """
        Middleware para verificar las credenciales de Firebase en cada solicitud de diagnóstico.
        Args:
            peticion (Diagnostico): La solicitud que contiene el token.
            call_next: La función para pasar al siguiente middleware o ruta.
    """
    if peticion.method == "POST":
        return await verificar_token(peticion, firebase_app, call_next)
    else:
        return await call_next(peticion)