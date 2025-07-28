from apis.FirebaseAuth import ver_datos_token
from apis.Firestore import verificar_rol_usuario
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import ver_datos_usuarios, ver_datos_usuario
from firebase_admin_config import firebase_app
from utils.Validadores import validar_correo
from urllib.parse import unquote

router = APIRouter(prefix="/usuarios")

@router.get("")
async def ver_usuarios(req: Request) -> JSONResponse:
    try:
        RES, DATOS = ver_datos_token(req, firebase_app)

        if RES in (-1, 0):
            return JSONResponse(
                DATOS,
                status_code=403 if RES == 0 else 400,
                media_type="application/json",
            )

        VALIDAR_ROL = await verificar_rol_usuario(DATOS["email"])

        if not VALIDAR_ROL:
            return JSONResponse(
                {"error": "Acceso denegado."},
                status_code=403,
                media_type="application/json",
            )

        return await ver_datos_usuarios(firebase_app)
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
    
@router.get("/{correo}")
async def ver_usuario(req: Request, correo: str) -> JSONResponse:
    try:
        correo = unquote(correo)
        RES, DATOS = ver_datos_token(req, firebase_app)

        if RES in (-1, 0):
            return JSONResponse(
                DATOS,
                status_code=403 if RES == 0 else 400,
                media_type="application/json",
            )

        VALIDAR_ROL = await verificar_rol_usuario(DATOS["email"])

        if not VALIDAR_ROL:
            return JSONResponse(
                {"error": "Acceso denegado."},
                status_code=403,
                media_type="application/json",
            )

        VALIDACION = validar_correo(correo)

        if not VALIDACION:
            raise ValueError("Correo inválido")

        return await ver_datos_usuario(firebase_app, correo)
    except ValueError:
        return JSONResponse(
            {"error": "Correo inválido"},
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )