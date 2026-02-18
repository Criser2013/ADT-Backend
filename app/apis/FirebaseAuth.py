import firebase_admin.auth
from firebase_admin.auth import *
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO, COD_EXITO
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
        return (COD_EXITO, datos) if obtener_datos else COD_EXITO
    except (ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError):
        return (COD_ERROR_ESPERADO, None) if obtener_datos else COD_ERROR_ESPERADO
    except (ValueError, CertificateFetchError, InvalidIdTokenError):
        return (COD_ERROR_INESPERADO, None) if obtener_datos else COD_ERROR_INESPERADO


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
            COD_ERROR_ESPERADO
            if (not reg_validacion)
            else validar_token(token, firebase_app, False)
        )

        return res_validacion
    except Exception:
        return COD_ERROR_INESPERADO


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
            return (
                COD_ERROR_ESPERADO,
                {"error": f"{textos[idioma]['errTokenInvalido']}"},
            )

        CODIGO, RES = validar_token(token, firebase_app, True)
        error = (
            {"error": f"{textos[idioma]['errTokenInvalido']}"}
            if CODIGO == COD_ERROR_ESPERADO
            else {"error": f"{textos[idioma]['errValidarToken']}"}
        )

        return (CODIGO, RES if CODIGO == COD_EXITO else error)

    except Exception as e:
        return (
            COD_ERROR_INESPERADO,
            {"error": f"{textos[idioma]['errProcesarToken']}: {e}."},
        )


async def ver_datos_usuarios(firebase_app) -> tuple[int, list[dict] | None]:
    """
    Obtiene los datos de los usuarios registrados en Firebase.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
    Returns:
        tuple[int, list[dict] | None]: Un código de estado y los datos de los usuarios si se obtuvieron correctamente, o None si hubo un error.
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

        return (COD_EXITO, AUX)
    except Exception:
        return (COD_ERROR_INESPERADO, None)


async def ver_datos_usuario(firebase_app, uid: str) -> tuple[int, dict | None]:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app: La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.
    Returns:
        tuple[int, dict | str | None]: Un código de estado y los datos del usuario si se encuentra.
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

        return (COD_EXITO, RES)
    except UserNotFoundError:
        return (COD_ERROR_ESPERADO, None)
    except Exception as e:
        return (COD_ERROR_INESPERADO, e)


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
        RES = firebase_admin.auth.get_user(uid, firebase_app)
        return (COD_EXITO, RES)
    except UserNotFoundError:
        return (COD_ERROR_ESPERADO, None)
    except Exception:
        return (COD_ERROR_INESPERADO, None)


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
        USUARIO = firebase_admin.auth.update_user(
            uid=uid, disabled=estado, app=firebase_app
        )

        RES = {
            "correo": USUARIO.email,
            "uid": USUARIO.uid,
            "nombre": USUARIO.display_name,
            "estado": not USUARIO.disabled,
            "fecha_registro": convertir_datetime_str(
                USUARIO.user_metadata.creation_timestamp
            ),
            "ultima_conexion": convertir_datetime_str(
                USUARIO.user_metadata.last_refresh_timestamp
            ),
        }

        return (COD_EXITO, RES)
    except ValueError:
        return (COD_ERROR_ESPERADO, None)
    except Exception as e:
        return (COD_ERROR_INESPERADO, e)
