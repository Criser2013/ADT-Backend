from firebase_admin.auth import *
from firebase_admin.exceptions import NotFoundError
from firebase_admin import App
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO, COD_EXITO
from models.Peticiones import UsuarioActualizar
from utils.Validadores import validar_txt_token
from utils.Fechas import convertir_datetime_str



def validar_token(
    token: str, firebase_app: App, obtener_datos: bool
) -> int | tuple[int, dict | None]:
    """
    Verifica si el token de Firebase es válido.
    Args:
        token (str): El token de Firebase a verificar.
        firebase_app (App): La instancia de la aplicación Firebase.
        obtener_datos (bool): Si True, retorna los datos del token si es válido.
    Returns:
        int: 1 si el token es válido, 0 en caso contrario y -1 si hay un error de validación.
    """
    try:
        datos = verify_id_token(token, firebase_app, check_revoked=True)
        return (COD_EXITO, datos) if obtener_datos else COD_EXITO
    except (ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError):
        return (COD_ERROR_ESPERADO, None) if obtener_datos else COD_ERROR_ESPERADO
    except (ValueError, CertificateFetchError, InvalidIdTokenError):
        return (COD_ERROR_INESPERADO, None) if obtener_datos else COD_ERROR_INESPERADO


async def verificar_token(firebase_app: App, token: str) -> int:
    """
    Verifica el token de Firebase en la solicitud.
    Args:
        token (str | None): El token de autorización de la solicitud.
        firebase_app (App): La instancia de la aplicación Firebase.
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
    token: str, firebase_app: App, idioma: str, textos: dict[str, str]
) -> tuple[int, dict]:
    """
    Obtiene los datos del token de Firebase.
    Args:
        token (str): El token de autorización de la solicitud.
        firebase_app (App): La instancia de la aplicación Firebase.
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
        if CODIGO != COD_EXITO:
            error = (
                {"error": f"{textos[idioma]['errTokenInvalido']}"}
                if CODIGO == COD_ERROR_ESPERADO
                else {"error": f"{textos[idioma]['errValidarToken']}"}
            )

        return (CODIGO, RES if CODIGO == COD_EXITO else error)

    except Exception as e:
        return (
            COD_ERROR_INESPERADO,
            {"error": f"{textos[idioma]['errProcesarToken']}: {str(e)}."},
        )


async def ver_datos_usuarios(firebase_app: App) -> tuple[int, list[dict] | None]:
    """
    Obtiene los datos de los usuarios registrados en Firebase.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
    Returns:
        tuple[int, list[dict] | None]: Un código de estado y los datos de los usuarios si se obtuvieron correctamente, o None si hubo un error.
    """
    try:
        AUX = []
        usuarios = list_users(app=firebase_app)

        while True:
            lista = []
            for x in usuarios.users:
                if x.custom_claims["eliminado"] == False:
                    lista.append({
                        "correo": x.email,
                        "uid": x.uid,
                        "nombre": x.display_name,
                        "administrador": x.custom_claims["admin"],
                        "estado": not x.disabled,
                        "fecha_registro": convertir_datetime_str(
                            x.user_metadata.creation_timestamp
                        ),
                        "ultima_conexion": convertir_datetime_str(
                            x.user_metadata.last_refresh_timestamp
                        )
                    })
            AUX.extend(lista)
            if not usuarios.has_next_page:
                break
            else:
                usuarios = usuarios.get_next_page()

        return (COD_EXITO, AUX)
    except:
        return (COD_ERROR_INESPERADO, None)


async def ver_datos_usuario(firebase_app: App, uid: str) -> tuple[int, dict | None]:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.
    Returns:
        tuple[int, dict | str | None]: Un código de estado y los datos del usuario si se encuentra.
    """
    try:
        usuario = get_user(uid, firebase_app)

        if usuario.custom_claims["eliminado"] == True:
            raise UserNotFoundError("")

        RES = {
            "correo": usuario.email,
            "uid": usuario.uid,
            "nombre": usuario.display_name,
            "administrador": usuario.custom_claims["admin"],
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
    except Exception:
        return (COD_ERROR_INESPERADO, None)


def ver_usuario_firebase(firebase_app: App, uid: str) -> tuple[int, UserRecord | None]:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
    Returns:
        tuple[int, UserRecord | None]: Un código de estado y el registro del usuario si se encuentra.
    """
    try:
        RES = get_user(uid, firebase_app)
        return (COD_EXITO, RES)
    except UserNotFoundError:
        return (COD_ERROR_ESPERADO, None)
    except Exception:
        return (COD_ERROR_INESPERADO, None)


def actualizar_estado_usuario(
    firebase_app: App, uid: str, usuario: UsuarioActualizar
) -> tuple[int, dict | None]:
    """
    Actualiza el estado (activado/desactivado) de un usuario específico.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a actualizar.
        usuario (UsuarioActualizar): La instancia de usuario a actualizar con los nuevos valores de estado y administrador.
    Returns:
        tuple[int, dict | None]: Un código de estado y los datos del usuario actualizado si se actualiza correctamente.
    """
    try:
        USUARIO = update_user(
            uid=uid,
            disabled=usuario.desactivar,
            app=firebase_app,
            custom_claims={"admin": usuario.administrador, "eliminado": usuario.eliminado},
        )

        RES = {
            "correo": USUARIO.email,
            "uid": USUARIO.uid,
            "nombre": USUARIO.display_name,
            "estado": not USUARIO.disabled,
            "administrador": USUARIO.custom_claims["admin"],
            "fecha_registro": convertir_datetime_str(
                USUARIO.user_metadata.creation_timestamp
            ),
            "ultima_conexion": convertir_datetime_str(
                USUARIO.user_metadata.last_refresh_timestamp
            ),
        }

        return (COD_EXITO, RES)
    except NotFoundError:
        return (COD_ERROR_ESPERADO, None)
    except Exception as e:
        return (COD_ERROR_INESPERADO, str(e))


def establecer_rol_usuario(firebase_app: App, uid: str) -> tuple[int, str | None]:
    """
    Establece el rol de un usuario específico cuando este se registra.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario al que se le asignará el rol.
    Returns:
        tuple[int, str | None]: Un código de estado indicando el resultado de la operación.
    """
    try:
        set_custom_user_claims(uid, {"admin": False, "eliminado": False}, app=firebase_app)
        return (COD_EXITO, None)
    except NotFoundError:
        return (COD_ERROR_ESPERADO, None)
    except Exception as e:
        return (COD_ERROR_INESPERADO, str(e))
