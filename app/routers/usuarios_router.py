from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import *
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

@router.patch("/{correo}")
async def actualizar_usuario(
    correo: str, desactivar: bool, res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(verificar_usuario_administrador)
) -> JSONResponse:
    try:
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        correo = unquote(correo)
        VALIDACION = validar_correo(correo)

        if not VALIDACION:
            raise ValueError("Correo inválido")

        DATOS = ver_usuario_firebase(firebase_app, correo)
        if DATOS[0] == 0:
            return JSONResponse(
                {"error": "Usuario no encontrado"},
                status_code=404,
                media_type="application/json",
            )
        elif DATOS[0] == -1:
            raise Exception("Error al obtener el usuario")

        return actualizar_estado_usuario(firebase_app, DATOS[1].uid, desactivar)
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