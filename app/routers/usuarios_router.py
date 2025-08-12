from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import *
from firebase_admin_config import firebase_app
from utils.Validadores import validar_uid
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


@router.get("/{uid}")
async def ver_usuario(
    uid: str, res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(verificar_usuario_administrador)
) -> JSONResponse:
    try:
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        uid = unquote(uid)
        VALIDACION = validar_uid(uid)

        if not VALIDACION:
            raise ValueError("UID inválido")

        return await ver_datos_usuario(firebase_app, uid)
    except ValueError:
        return JSONResponse(
            {"error": "UID inválido"},
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )

@router.patch("/{uid}")
async def actualizar_usuario(
    uid: str, desactivar: bool, res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(verificar_usuario_administrador)
) -> JSONResponse:
    try:
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        uid = unquote(uid)
        VALIDACION = validar_uid(uid)

        if not VALIDACION:
            raise ValueError("UID inválido")

        DATOS = ver_usuario_firebase(firebase_app, uid)
        if DATOS[0] == 0:
            return JSONResponse(
                {"error": "Usuario no encontrado"},
                status_code=404,
                media_type="application/json",
            )
        elif DATOS[0] == -1:
            raise Exception("Error al obtener el usuario")

        return actualizar_estado_usuario(firebase_app, uid, desactivar)
    except ValueError:
        return JSONResponse(
            {"error": "UID inválido"},
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )