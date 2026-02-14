from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, Response, Header
from routers.main_router import router as main_router
from routers.usuarios_router import router as usuarios_router
from apis.FirebaseAuth import verificar_token
from constants import CORS_ORIGINS, ALLOWED_HOSTS, ACTIVAR_DOCS, ORIGENES_AUTORIZADOS
from utils.Validadores import validar_origen
from utils.Diccionario import ver_si_existe_clave
from firebase_admin_config import firebase_app

app = FastAPI(docs_url=None if not ACTIVAR_DOCS else "/docs", redoc_url=None if not ACTIVAR_DOCS else "/redoc")

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
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=ALLOWED_HOSTS
)

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
    """RUTAS_NO_PROTEGIDAS = ("/recaptcha",)
    METODOS_RESTRINGIDOS = ("POST",)

    token = peticion.headers["authorization"] if ver_si_existe_clave(peticion.headers, "authorization") else ""
    idioma = peticion.headers["language"] if ver_si_existe_clave(peticion.headers, "language") else "es"

    if peticion.method in METODOS_RESTRINGIDOS and (peticion.url.path not in RUTAS_NO_PROTEGIDAS):
        return await verificar_token(peticion, firebase_app, call_next, idioma, token)
    else:
        return await call_next(peticion)"""

    return await call_next(peticion)