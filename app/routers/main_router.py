from models.Diagnostico import Diagnostico
from models.PeticionDiagnostico import PeticionDiagnostico
from models.PeticionRecaptcha import PeticionRecaptcha
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from apis.Recaptcha import verificar_peticion_recaptcha
from dependencies.general_dependencies import verificar_idioma

router = APIRouter(dependencies=[Depends(verificar_idioma)])

@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse({"status": "ok"}, status_code=200, media_type="application/json")

@router.get("/credenciales")
async def obtener_credenciales(peticion: Request, idioma: str = Depends(verificar_idioma)):
    TEXTOS = peticion.state.textos
    CREDS_FIREBASE_CLIENTE = peticion.state.credenciales
    return JSONResponse(
        CREDS_FIREBASE_CLIENTE, status_code=200, media_type="application/json"
    )


@router.post("/diagnosticar")
async def diagnosticar(peticion: Request, req: PeticionDiagnostico) -> JSONResponse:
    MODELO = peticion.state.modelo
    EXPLICADOR = peticion.state.explicador
    DATOS = req.obtener_diccionario_instancia()
    DIAGNOSTICO = Diagnostico(DATOS, MODELO, EXPLICADOR)
    RES = await DIAGNOSTICO.generar_diagnostico()

    return JSONResponse(RES, status_code=200, media_type="application/json")
    
@router.post("/recaptcha")
async def verificar_recaptcha(peticion: Request, req: PeticionRecaptcha, idioma: str = Depends(verificar_idioma)) -> JSONResponse:
    TEXTOS = peticion.state.textos
    resultado = verificar_peticion_recaptcha(req.token, idioma, TEXTOS)
    return JSONResponse(resultado, status_code=200, media_type="application/json")