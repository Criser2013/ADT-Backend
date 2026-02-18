import firebase_admin.auth
from firebase_admin.auth import *
from fastapi.responses import JSONResponse
from utils.Validadores import validar_txt_token
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


async def verificar_token(firebase_app, token: str) -> int:
    """
    Verifica el token de Firebase en la solicitud.
    Args:
        token (str | None): El token de autorización de la solicitud.
        firebase_app (object): La instancia de la aplicación Firebase.
    Returns:
        int: Código de estado: 1 si el token es válido, 0 si es inválido, -1 si hay un error.
    """
    try:
        token = token.split("Bearer ")[1]
        reg_validacion = validar_txt_token(token)
        res_validacion = (
            0 if (not reg_validacion) else validar_token(token, firebase_app, False)
        )

        return res_validacion
    except Exception:
        return -1


def ver_datos_token(
    token: str, firebase_app, idioma: str, textos: dict[str, str]
) -> tuple[int, dict]:
    """
    Obtiene los datos del token de Firebase.
    Args:
        token (str): El token de autorización de la solicitud.
        firebase_app: La instancia de la aplicación Firebase.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.
    Returns:
        tuple: (True, datos) si el token es válido, (False, error) si hay un error.
    """
    try:
        token = token.split("Bearer ")[1]
        reg_validacion = validar_txt_token(token)

        if not reg_validacion:
            return (0, {"error": f"{textos[idioma]['errTokenInvalido']}"})

        CODIGO, RES = validar_token(token, firebase_app, True)
        error = (
            {"error": f"{textos[idioma]['errTokenInvalido']}"}
            if CODIGO == 0
            else {"error": f"{textos[idioma]['errValidarToken']}"}
        )

        return (CODIGO, RES if CODIGO == 1 else error)

    except Exception as e:
        return (-1, {"error": f"{textos[idioma]['errProcesarToken']}: {e}."})


async def ver_datos_usuarios(firebase_app) -> list[dict] | None:
    """
    Obtiene los datos de los usuarios registrados en Firebase.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
    Returns:
        list[dict] | None: Los datos de los usuarios, o None si ocurre un problema.
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
                        "uid": x.uid,
                        "nombre": x.display_name,
                        "rol": (
                            ROLES[x.uid] if ver_si_existe_clave(ROLES, x.uid) else "N/A"
                        ),
                        "estado": not x.disabled,
                        "fecha_registro": convertir_datetime_str(
                            x.user_metadata.creation_timestamp
                        ),
                        "ultima_conexion": convertir_datetime_str(
                            x.user_metadata.last_refresh_timestamp
                        ),
                    }
                    for x in usuarios.users
                ]
            )
            if not usuarios.has_next_page:
                break
            else:
                usuarios = usuarios.get_next_page()

        return AUX
    except Exception:
        return None


async def ver_datos_usuario(firebase_app, uid: str) -> tuple[int, dict | None]:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.
    Returns:
        tuple[int, dict]: Un código de estado y los datos del usuario si se encuentra.
    """
    try:
        roles_task = asyncio.create_task(obtener_rol_usuario(uid))
        usuario = firebase_admin.auth.get_user(uid, firebase_app)
        ROL = await roles_task

        if ROL == -1:
            raise UserNotFoundError("")

        RES = {
            "correo": usuario.email,
            "uid": usuario.uid,
            "nombre": usuario.display_name,
            "rol": ROL,
            "estado": not usuario.disabled,
            "fecha_registro": convertir_datetime_str(
                usuario.user_metadata.creation_timestamp
            ),
            "ultima_conexion": convertir_datetime_str(
                usuario.user_metadata.last_refresh_timestamp
            ),
        }

        return (1, RES)
    except UserNotFoundError:
        return (0, None)
    except Exception as e:
        return (-1, e)


def ver_usuario_firebase(firebase_app, uid: str) -> tuple[int, UserRecord | None]:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
    Returns:
        tuple[int, UserRecord | None]: Un código de estado y el registro del usuario si se encuentra.
    """
    try:
        return (1, firebase_admin.auth.get_user(uid, firebase_app))
    except UserNotFoundError:
        return (0, None)
    except:
        return (-1, None)


def actualizar_estado_usuario(
    firebase_app, uid: str, estado: bool
) -> tuple[int, dict | None]:
    """
    Actualiza el estado (activado/desactivado) de un usuario específico.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a actualizar.
        estado (bool): El nuevo estado del usuario (True para desactivado, False para activado).
    Returns:
        tuple[int, dict | None]: Un código de estado y los datos del usuario actualizado si se actualiza correctamente.
    """
    try:
        RES = firebase_admin.auth.update_user(
            uid=uid, disabled=estado, app=firebase_app
        )
        return (1, RES)
    except ValueError:
        return (0, None)
    except Exception as e:
        return (-1, None)
