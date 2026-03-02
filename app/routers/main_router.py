from models.Diagnostico import Diagnostico
from models.Peticiones import *
from fastapi import APIRouter, Depends, Request, Header
from fastapi.responses import JSONResponse
from apis.Recaptcha import verificar_peticion_recaptcha
from apis.FirebaseAuth import establecer_rol_usuario, ver_datos_usuario
from dependencies.general_dependencies import verificar_idioma, verificar_autenticado
from dependencies.usuarios_dependencies import validador_uid
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO
from models.Excepciones import UsuarioInexistente, AccesoNoAutorizado
from firebase_admin.auth import verify_id_token

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@router.get("/credenciales")
async def obtener_credenciales(peticion: Request) -> JSONResponse:
    CREDS_FIREBASE_CLIENTE = peticion.state.credenciales
    return CREDS_FIREBASE_CLIENTE


@router.post("/diagnosticar", dependencies=[Depends(verificar_autenticado)])
async def diagnosticar(
    peticion: Request,
    req: InstanciaDiagnostico,
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    MODELO = peticion.state.modelo
    EXPLICADOR = peticion.state.explicador

    try:
        DATOS = req.obtener_diccionario_instancia()
        DIAGNOSTICO = Diagnostico(DATOS, MODELO, EXPLICADOR)
        RES = DIAGNOSTICO.generar_diagnostico()

        return RES
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.post("/recaptcha")
async def verificar_recaptcha(
    peticion: Request, req: TokenRecaptcha, idioma: str = Depends(verificar_idioma)
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    try:
        RES = verificar_peticion_recaptcha(req.token, idioma, TEXTOS)
        return RES
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.post("/registrar")
async def registrar_usuario(
    peticion: Request,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    FIREBASE_APP = peticion.state.firebase_app

    COD, RES = establecer_rol_usuario(FIREBASE_APP, uid)

    if COD == COD_ERROR_ESPERADO:
        raise UsuarioInexistente({"error": TEXTOS[idioma]["errUsuarioNoEncontrado"]})
    elif COD == COD_ERROR_INESPERADO:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {RES}"},
            status_code=500,
            media_type="application/json",
        )

    return {"resultado": "ok"}


@router.get("/ver-rol")
async def ver_rol_usuario(
    usuario: dict = Depends(verificar_autenticado),
) -> JSONResponse:

    return {"administrador": usuario["admin"]}