from apis.FirebaseAuth import registrar_usuario_firebase
from apis.Recaptcha import verificar_peticion_recaptcha
from dependencies.general_dependencies import verificar_idioma, verificar_autenticado
from dependencies.usuarios_dependencies import validador_uid
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.Diagnostico import Diagnostico
from models.Excepciones import ErrorInterno
from models.Peticiones import *

router = APIRouter()


@router.get("/credenciales")
async def obtener_credenciales(peticion: Request) -> JSONResponse:
    CREDS_FIREBASE_CLIENTE = peticion.state.credenciales
    return CREDS_FIREBASE_CLIENTE


@router.post("/diagnosticar", dependencies=[Depends(verificar_autenticado)])
async def diagnosticar(
    peticion: Request,
    instancia: InstanciaDiagnostico,
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    MODELO = peticion.state.modelo
    EXPLICADOR = peticion.state.explicador

    try:
        DATOS = instancia.obtener_diccionario_instancia()
        DIAGNOSTICO = Diagnostico(DATOS, MODELO, EXPLICADOR)
        RES = DIAGNOSTICO.generar_diagnostico()
        return JSONResponse(
            RES.model_dump(), status_code=200, media_type="application/json"
        )
    except:
        raise ErrorInterno(TEXTOS[idioma]["errGenerarDiagnostico"])


@router.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}


@router.post("/registrar", dependencies=[Depends(verificar_autenticado)])
async def registrar_usuario(
    peticion: Request,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    FIREBASE_APP = peticion.state.firebase_app
    registrar_usuario_firebase(FIREBASE_APP, uid, TEXTOS, idioma)
    return JSONResponse(
        {"resultado": "ok"}, status_code=200, media_type="application/json"
    )


@router.post("/recaptcha")
async def verificar_recaptcha(
    peticion: Request,
    token_recaptcha: TokenRecaptcha,
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    RES = verificar_peticion_recaptcha(token_recaptcha.token, idioma, TEXTOS)
    return JSONResponse(
        RES,
        status_code=200 if RES["success"] else 401,
        media_type="application/json",
    )
