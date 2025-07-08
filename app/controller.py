from models.Diagnostico import Diagnostico
from models.PeticionDiagnostico import PeticionDiagnostico
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import getenv

load_dotenv()

FIREBASE_CLIENTE = {
    "apiKey": getenv("CLIENTE_FIREBASE_API_KEY"),
    "authDomain": getenv("CLIENTE_FIREBASE_AUTH_DOMAIN"),
    "projectId": getenv("CLIENTE_FIREBASE_PROJECT_ID"),
    "storageBucket": getenv("CLIENTE_FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": getenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID"),
    "appId": getenv("CLIENTE_FIREBASE_APP_ID"),
    "measurementId": getenv("CLIENTE_FIREBASE_MEASUREMENT_ID"),
    "driveScopes": getenv("CLIENTE_DRIVE_SCOPES"),
}

router = APIRouter()

@router.get("/credenciales")
async def obtener_credenciales():
    try:
        return JSONResponse(
            FIREBASE_CLIENTE, status_code=200, media_type="application/json"
        )
    except:
        return JSONResponse({ "error": "Error al obtener las credenciales" }, status_code=500, media_type="application/json")


@router.post("/diagnosticar")
async def diagnosticar(req: PeticionDiagnostico) -> JSONResponse:
    try:
        DATOS = req.obtener_array_instancia()
        DIAGNOSTICO = Diagnostico(DATOS)
        RES = DIAGNOSTICO.generar_diagnostico()

        return JSONResponse(RES, status_code=200, media_type="application/json")
    except Exception as e:
        return JSONResponse({ "error": f"Error al procesar la solicitud: {str(e)}" }, status_code=500, media_type="application/json")