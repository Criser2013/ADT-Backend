from models.Diagnostico import Diagnostico
from models.PeticionDiagnostico import PeticionDiagnostico
from models.PeticionRecaptcha import PeticionRecaptcha
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from constants import CREDS_FIREBASE_CLIENTE, TEXTOS
from apis.Recaptcha import verificar_peticion_recaptcha
from dependencies.general_dependencies import verificar_idioma

router = APIRouter(dependencies=[Depends(verificar_idioma)])

@router.get("/credenciales")
async def obtener_credenciales(idioma: str = Depends(verificar_idioma)):
    try:
        return JSONResponse(
            CREDS_FIREBASE_CLIENTE, status_code=200, media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.post("/diagnosticar")
async def diagnosticar(req: PeticionDiagnostico, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
    try:
        DATOS = req.obtener_array_instancia()
        DIAGNOSTICO = Diagnostico(DATOS)
        RES = DIAGNOSTICO.generar_diagnostico()

        return JSONResponse(RES, status_code=200, media_type="application/json")
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
    
@router.post("/recaptcha")
async def verificar_recaptcha(req: PeticionRecaptcha, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
    try:
        resultado = verificar_peticion_recaptcha(req.token, idioma)
        return JSONResponse(resultado, status_code=200, media_type="application/json")
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )