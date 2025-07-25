from models.Diagnostico import Diagnostico
from models.PeticionDiagnostico import PeticionDiagnostico
from models.PeticionUsuarios import PeticionUsuarios
from apis.Firestore import verificar_rol_usuario
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from constants import CREDS_FIREBASE_CLIENTE
from apis.FirebaseAuth import ver_datos_usuarios
from firebase_admin_config import firebase_app

router = APIRouter()


@router.get("/credenciales")
async def obtener_credenciales():
    try:
        return JSONResponse(
            CREDS_FIREBASE_CLIENTE, status_code=200, media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al obtener las credenciales: {e}"},
            status_code=500,
            media_type="application/json",
        )


@router.post("/diagnosticar")
async def diagnosticar(req: PeticionDiagnostico) -> JSONResponse:
    try:
        DATOS = req.obtener_array_instancia()
        DIAGNOSTICO = Diagnostico(DATOS)
        RES = DIAGNOSTICO.generar_diagnostico()

        return JSONResponse(RES, status_code=200, media_type="application/json")
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.post("/usuarios")
async def ver_usuarios(req: PeticionUsuarios) -> JSONResponse:
    try:
        VALIDAR_ROL = await verificar_rol_usuario(req.correo)

        if not VALIDAR_ROL:
            return JSONResponse(
                {"error": "Acceso denegado."},
                status_code=403,
                media_type="application/json",
            )

        return ver_datos_usuarios(firebase_app)
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
