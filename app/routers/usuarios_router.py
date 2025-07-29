from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import ver_datos_usuarios, ver_datos_usuario
from firebase_admin_config import firebase_app
from utils.Validadores import validar_correo
from urllib.parse import unquote
from dependencies.usuarios_dependencies import verificar_usuario_administrador

router = APIRouter(
    prefix="/usuarios", dependencies=[Depends(verificar_usuario_administrador)]
)


@router.get("")
async def ver_usuarios(
    res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(verificar_usuario_administrador),
) -> JSONResponse:
    try:
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        return await ver_datos_usuarios(firebase_app)
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.get("/{correo}")
async def ver_usuario(
    correo: str, res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(verificar_usuario_administrador)
) -> JSONResponse:
    try:
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        correo = unquote(correo)
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
