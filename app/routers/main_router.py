from app.models.Diagnostico import Diagnostico
from app.models.PeticionDiagnostico import PeticionDiagnostico
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.constants import CREDS_FIREBASE_CLIENTE

router = APIRouter()

@router.get("/credenciales")
async def obtener_credenciales():
    try:
        return JSONResponse(
            CREDS_FIREBASE_CLIENTE, status_code=200, media_type="application/json"
        )
    except Exception as e:
        return JSONResponse({ "error": f"Error al obtener las credenciales: {e}" }, status_code=500, media_type="application/json")


@router.post("/diagnosticar")
async def diagnosticar(req: PeticionDiagnostico) -> JSONResponse:
    try:
        DATOS = req.obtener_array_instancia()
        DIAGNOSTICO = Diagnostico(DATOS)
        RES = DIAGNOSTICO.generar_diagnostico()

        return JSONResponse(RES, status_code=200, media_type="application/json")
    except Exception as e:
        return JSONResponse({ "error": f"Error al procesar la solicitud: {str(e)}" }, status_code=500, media_type="application/json")