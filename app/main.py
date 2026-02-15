from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, Response
from dotenv import load_dotenv
from os import getenv
from routers.main_router import router as main_router
from utils.Dominios import obtener_lista_dominios
from routers.usuarios_router import router as usuarios_router
from apis.FirebaseAuth import verificar_token
from constants import (
    CORS_ORIGINS,
    ALLOWED_HOSTS,
    ACTIVAR_DOCS,
    ORIGENES_AUTORIZADOS
)
from utils.Validadores import validar_origen
from utils.Diccionario import ver_si_existe_clave
from contextlib import asynccontextmanager
from pathlib import Path
from dill import load as dload
from json import load as jload
from onnxruntime import InferenceSession
from firebase_admin_config import inicializar_firebase

load_dotenv()


# Inicialización de los modelos y recursos necesarios para la aplicación
@asynccontextmanager
async def inicializar_modelos(app: FastAPI):
    # Esto se ejecuta al iniciar el backend
    PATH_BASE = Path(__file__).resolve().parent
    FIREBASE_APP = inicializar_firebase()

    CREDS_FIREBASE_CLIENTE = {
    "apiKey": getenv("CLIENTE_FIREBASE_API_KEY"),
    "authDomain": getenv("CLIENTE_FIREBASE_AUTH_DOMAIN"),
    "projectId": getenv("CLIENTE_FIREBASE_PROJECT_ID"),
    "storageBucket": getenv("CLIENTE_FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": getenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID"),
    "appId": getenv("CLIENTE_FIREBASE_APP_ID"),
    "measurementId": getenv("CLIENTE_FIREBASE_MEASUREMENT_ID"),
    "driveScopes": obtener_lista_dominios(getenv("CLIENTE_DRIVE_SCOPES","")),
    "reCAPTCHA": getenv("CLIENTE_CAPTCHA"),
}

    with open(f"{PATH_BASE}/bin/explicador.pkl", "rb") as archivo:
        EXPLAINER = dload(archivo)

    with open(f"{PATH_BASE}/bin/textos.json") as archivo:
        TEXTOS = jload(archivo)

    MODELO = InferenceSession(
        f"{PATH_BASE}/bin/modelo_red_neuronal.onnx",
        providers=["CPUExecutionProvider"],
    )

    yield {
        "explicador": EXPLAINER,
        "textos": TEXTOS,
        "modelo": MODELO,
        "firebase_app": FIREBASE_APP,
        "credenciales": CREDS_FIREBASE_CLIENTE,
    }

    # Esto se ejecuta después de cerrar el backend

    FIREBASE_APP._cleanup()
    del EXPLAINER, TEXTOS, MODELO, FIREBASE_APP, CREDS_FIREBASE_CLIENTE

# Inicialización de la aplicación FastAPI
app = FastAPI(
    lifespan=inicializar_modelos,
    docs_url=None if not ACTIVAR_DOCS else "/docs",
    redoc_url=None if not ACTIVAR_DOCS else "/redoc",
)

# Añadiendo los enrutadores
app.include_router(main_router)
app.include_router(usuarios_router, prefix="/admin")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Language"],
)

# Middleware que no permite peticiones de hosts no autorizados
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)


# Middlewares personalizados
@app.middleware("http")
async def verificar_origen_autorizado(peticion: Request, call_next) -> Response:
    """
    Middleware para verificar el origen de la solicitud.
    Args:
        peticion (Diagnostico): La solicitud que contiene el token.
        call_next: La función para pasar al siguiente middleware o ruta.
    """
    EXISTE = ver_si_existe_clave(peticion.headers, "origin")
    if not EXISTE:
        return Response(status_code=400, content="Encabezado 'origin' inválido")
    ORIGEN = peticion.headers["origin"]
    RES = validar_origen(ORIGEN, ORIGENES_AUTORIZADOS)

    if not RES:
        return Response(status_code=403, content="Origen no autorizado")
    else:
        return await call_next(peticion)


@app.middleware("http")
async def verificar_credenciales(peticion: Request, call_next) -> Response:
    """
    Middleware para verificar las credenciales de Firebase en cada solicitud de diagnóstico.
    Args:
        peticion (Diagnostico): La solicitud que contiene el token.
        call_next: La función para pasar al siguiente middleware o ruta.
    """
    RUTAS_NO_PROTEGIDAS = ("/recaptcha",)
    METODOS_RESTRINGIDOS = ("POST",)
    firebase_app = peticion.state.firebase_app
    TEXTOS = peticion.state.textos

    token = (
        peticion.headers["authorization"]
        if ver_si_existe_clave(peticion.headers, "authorization")
        else ""
    )
    idioma = (
        peticion.headers["language"]
        if ver_si_existe_clave(peticion.headers, "language")
        else "es"
    )

    if peticion.method in METODOS_RESTRINGIDOS and (
        peticion.url.path not in RUTAS_NO_PROTEGIDAS
    ):
        return await verificar_token(peticion, firebase_app, call_next, token, TEXTOS, idioma)
    else:
        return await call_next(peticion)
