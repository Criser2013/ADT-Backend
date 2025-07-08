from dotenv import load_dotenv
import firebase_admin
from pathlib import Path
from os import getenv
from os.path import join
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, Response
from controller import router as controller_router
from apis.FirebaseAuth import verificar_token
from utils.Dominios import obtener_lista_dominios

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Inicialización del servicio de Firebase
cred = firebase_admin.credentials.Certificate(join(BASE_DIR, "../firebase_token.json"))
firebase_app = firebase_admin.initialize_app(cred)

app = FastAPI()

# CORS
CORS_ORIGINS = obtener_lista_dominios(getenv("CORS_ORIGINS"))
ALLOWED_HOSTS = obtener_lista_dominios(getenv("ALLOWED_HOSTS"))

app.include_router(controller_router)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Middleware que no permite peticiones de hosts no confiables
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