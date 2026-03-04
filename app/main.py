from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from routers.main_router import router as main_router
from routers.usuarios_router import router as usuarios_router
from constants import *
from utils.Validadores import validar_origen
from utils.Diccionario import ver_si_existe_clave
from contextlib import asynccontextmanager
from firebase_admin_config import inicializar_firebase
from models.Excepciones import *

load_dotenv()


# Inicialización de los modelos y recursos necesarios para la aplicación
@asynccontextmanager
async def inicializar_modelos(app: FastAPI):
    # Esto se ejecuta al iniciar el backend
    FIREBASE_APP = inicializar_firebase()
    MODELOS = inicializar_modelos()
    CREDS_FIREBASE_CLIENTE = cargar_credenciales_cliente_firebase()

    yield {
        "explicador": MODELOS["explicador"],
        "textos": MODELOS["textos"],
        "modelo": MODELOS["modelo"],
        "firebase_app": FIREBASE_APP,
        "credenciales": CREDS_FIREBASE_CLIENTE,
    }

    # Esto se ejecuta después de cerrar el backend

    FIREBASE_APP._cleanup()

    del MODELOS["explicador"]
    del MODELOS["textos"]
    del MODELOS["modelo"]
    del FIREBASE_APP
    del CREDS_FIREBASE_CLIENTE


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


# Manejadores globales de excepciones personalizadas
@app.exception_handler(AccesoNoAutorizado)
async def manejar_acceso_no_autorizado(peticion: Request, excepcion: AccesoNoAutorizado):
    return JSONResponse(
        excepcion.mensaje,
        status_code=excepcion.codigo,
        media_type="application/json",
    )


@app.exception_handler(UIDInvalido)
async def manejar_uid_invalido(peticion: Request, excepcion: UIDInvalido):
    return JSONResponse(
        excepcion.mensaje,
        status_code=400,
        media_type="application/json",
    )

@app.exception_handler(UsuarioInexistente)
async def manejar_usuario_inexistente(peticion: Request, excepcion: UsuarioInexistente):
    return JSONResponse(
        excepcion.mensaje,
        status_code=404,
        media_type="application/json",
    )

@app.exception_handler(ErrorInterno)
async def manejar_error_interno(peticion: Request, excepcion: ErrorInterno):
    return JSONResponse(
        excepcion.mensaje,
        status_code=400,
        media_type="application/json",
    )