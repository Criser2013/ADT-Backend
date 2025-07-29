import firebase_admin.auth
from firebase_admin.auth import *
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from utils.Validadores import validar_txt_token
from datetime import datetime, timedelta, timezone
from utils.Fechas import convertir_datetime_str
from utils.Diccionario import ver_si_existe_clave
from apis.Firestore import obtener_roles_usuarios, obtener_rol_usuario
import asyncio


def validar_token(
    token: str, firebase_app, obtener_datos: bool
) -> int | tuple[int, dict | None]:
    """
    Verifica si el token de Firebase es válido.
    Args:
        token (str): El token de Firebase a verificar.
        firebase_app: La instancia de la aplicación Firebase.
        obtener_datos (bool): Si True, retorna los datos del token si es válido.
    Returns:
        int: 1 si el token es válido, 0 en caso contrario y -1 si hay un error de validación.
    """
    try:
        datos = firebase_admin.auth.verify_id_token(
            token, firebase_app, check_revoked=True
        )
        return (1, datos) if obtener_datos else 1
    except (ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError):
        return (0, None) if obtener_datos else 0
    except (ValueError, CertificateFetchError, InvalidIdTokenError):
        return (-1, None) if obtener_datos else -1


async def verificar_token(peticion: Request, firebase_app, call_next) -> JSONResponse:
    """
    Verifica el token de Firebase en la solicitud.
    Args:
        peticion (Diagnostico): La solicitud que contiene el token.
        firebase_app: La instancia de la aplicación Firebase.
        call_next: La función para pasar al siguiente middleware o ruta.
    Returns:
        JSONResponse: La respuesta de la solicitud, o un error si el token es inválido.
    """
    try:
        token = peticion.headers["authorization"].split("Bearer ")[1]
        reg_validacion = validar_txt_token(token)
        res_validacion = (
            0 if (not reg_validacion) else validar_token(token, firebase_app, False)
        )
        match res_validacion:
            case 1:
                return await call_next(peticion)
            case 0:
                return JSONResponse(
                    {"error": "Token inválido"},
                    status_code=403,
                    media_type="application/json",
                )
            case _:
                return JSONResponse(
                    {"error": "Error al validar el token"},
                    status_code=400,
                    media_type="application/json",
                )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {e}"},
            status_code=500,
            media_type="application/json",
        )


def ver_datos_token(peticion: Request, firebase_app) -> tuple[int, dict]:
    """
    Obtiene los datos del token de Firebase.
    Args:
        peticion (Request): La solicitud que contiene el token.
        firebase_app: La instancia de la aplicación Firebase.
    Returns:
        tuple: (True, datos) si el token es válido, (False, error) si hay un error.
    """
    try:
        token = peticion.headers["authorization"].split("Bearer ")[1]
        reg_validacion = validar_txt_token(token)

        if not reg_validacion:
            return (0, {"error": "Token inválido"})

        res_validacion = validar_token(token, firebase_app, True)

        match res_validacion[0]:
            case 1:
                return res_validacion
            case 0:
                return (0, {"error": "Token inválido"})
            case _:
                return (-1, {"error": "Error al validar el token"})

    except Exception as e:
        return (-1, {"error": f"Error al procesar el token: {e}."})


async def ver_datos_usuarios(firebase_app) -> JSONResponse:
    """
    Obtiene los datos de los usuarios registrados en Firebase.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
    Returns:
        JSONResponse: Los datos de los usuarios, o un error si ocurre un problema.
    """
    try:
        AUX = []
        roles_task = asyncio.create_task(obtener_roles_usuarios())
        usuarios = firebase_admin.auth.list_users(app=firebase_app)
        ROLES = await roles_task

        while True:
            AUX.extend(
                [
                    {
                        "correo": x.email,
                        "nombre": x.display_name,
                        "rol": (
                            ROLES[x.email]
                            if ver_si_existe_clave(ROLES, x.email)
                            else "N/A"
                        ),
                        "estado": not x.disabled,
                        "ultima_conexion": convertir_datetime_str(
                            datetime.fromtimestamp(
                                x.user_metadata.last_sign_in_timestamp / 1000,
                                tz=timezone(timedelta(hours=-5)),
                            )
                        ),
                    }
                    for x in usuarios.users
                ]
            )
            if not usuarios.has_next_page:
                break
            else:
                usuarios = usuarios.get_next_page()

        return JSONResponse(
            {"usuarios": AUX},
            status_code=200,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al obtener los datos de los usuarios: {e}"},
            status_code=400,
            media_type="application/json",
        )


async def ver_datos_usuario(firebase_app, correo: str) -> JSONResponse:
    """
    Obtiene los datos de un usuario específico usando el correo electrónico.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        correo (str): El correo del usuario a buscar.
    Returns:
        JSONResponse: Los datos del usuario, o un error si ocurre un problema.
    """
    try:
        roles_task = asyncio.create_task(obtener_rol_usuario(correo))
        usuario = firebase_admin.auth.get_user_by_email(correo, firebase_app)
        ROL = await roles_task

        if ROL == -1:
            raise UserNotFoundError("Usuario no encontrado")

        RES = {
            "correo": usuario.email,
            "nombre": usuario.display_name,
            "rol": ROL,
            "estado": not usuario.disabled,
            "ultima_conexion": convertir_datetime_str(
                datetime.fromtimestamp(
                    usuario.user_metadata.last_sign_in_timestamp / 1000,
                    tz=timezone(timedelta(hours=-5)),
                )
            ),
        }

        return JSONResponse(
            RES,
            status_code=200,
            media_type="application/json",
        )
    except UserNotFoundError:
        return JSONResponse(
            {"error": "Usuario no encontrado"},
            status_code=404,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al obtener los datos del usuario: {e}"},
            status_code=400,
            media_type="application/json",
        )

def ver_usuario_firebase(firebase_app, correo: str) -> tuple[int, UserRecord | None]:
    """
    Obtiene los datos de un usuario específico usando el correo electrónico.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        correo (str): El correo del usuario a buscar.
    Returns:
        tuple[int, UserRecord | None]: Un código de estado y el registro del usuario si se encuentra.
    """
    try:
        return 1, firebase_admin.auth.get_user_by_email(correo, firebase_app)
    except UserNotFoundError:
        return 0, None
    except:
        return -1, None

def actualizar_estado_usuario(firebase_app, uid: str, estado: bool) -> JSONResponse:
    """
    Actualiza el estado (activado/desactivado) de un usuario específico.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        correo (str): El correo del usuario a actualizar.
    Returns:
        JSONResponse | Response: Mensaje de éxito o error.
    """
    try:
        firebase_admin.auth.update_user(uid=uid, disabled=estado, app=firebase_app)

        return JSONResponse(
            {"mensaje": "Estado del usuario actualizado correctamente"},
            status_code=200,
            media_type="application/json",
        )
    except ValueError:
        return JSONResponse(
            {"error": "Estado inválido"},
            status_code=401,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )