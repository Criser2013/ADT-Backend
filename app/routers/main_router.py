from models.Diagnostico import Diagnostico
from models.Peticiones import *
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from apis.Recaptcha import verificar_peticion_recaptcha
from dependencies.general_dependencies import verificar_idioma

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@router.get("/credenciales")
async def obtener_credenciales(peticion: Request, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
    CREDS_FIREBASE_CLIENTE = peticion.state.credenciales
    return CREDS_FIREBASE_CLIENTE


@router.post("/diagnosticar")
async def diagnosticar(peticion: Request, req: InstanciaDiagnostico, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
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
async def verificar_recaptcha(peticion: Request, req: TokenRecaptcha, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
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