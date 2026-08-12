from constants import COD_EXITO
from firebase_admin import App
from firebase_admin.auth import (
    ExpiredIdTokenError,
    get_user,
    list_users,
    RevokedIdTokenError,
    set_custom_user_claims,
    update_user,
    UserDisabledError,
    verify_id_token,
)
from firebase_admin.exceptions import NotFoundError
from models.Excepciones import AccesoNoAutorizado, ErrorInterno, UsuarioInexistente
from models.Peticiones import UsuarioActualizar
from utils.Fechas import convertir_datetime_str
from utils.Validadores import validar_txt_token


def actualizar_estado_usuario(
    firebase_app: App, uid: str, usuario: UsuarioActualizar, textos: dict, idioma: str
) -> dict:
    """
    Actualiza el estado (activado/desactivado) de un usuario específico.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a actualizar.
        usuario (UsuarioActualizar): La instancia de usuario a actualizar con los nuevos valores de estado y administrador.
        textos (dict): El diccionario de textos para los mensajes de error.
        idioma (str): El idioma para los mensajes de error.
    Raises:
        UsuarioInexistente: Si el UID del usuario proveído es inexistente.
        Errorinterno: Si ocurre alguna excepción al tratar de validar el token.
    Returns:
        dict: Datos del usuario actualizado si se actualiza correctamente.
    """
    try:
        USUARIO = update_user(
            uid=uid,
            disabled=usuario.desactivar,
            app=firebase_app,
            custom_claims={
                "admin": usuario.administrador,
                "eliminado": usuario.eliminado,
            },
        )

        return {
            "correo": USUARIO.email,
            "uid": USUARIO.uid,
            "nombre": USUARIO.display_name,
            "estado": not USUARIO.disabled,
            "administrador": USUARIO.custom_claims.get("admin", False),
            "fecha_registro": convertir_datetime_str(
                USUARIO.user_metadata.creation_timestamp
            ),
            "ultima_conexion": convertir_datetime_str(
                USUARIO.user_metadata.last_refresh_timestamp
            ),
        }
    except NotFoundError:
        raise UsuarioInexistente()
    except:
        raise ErrorInterno(textos[idioma]["errActualizarUsuario"])


def registrar_usuario(firebase_app: App, uid: str, textos: dict, idioma: str) -> int:
    """
    Establece el rol de un usuario específico cuando este se registra.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario al que se le asignará el rol.
    Raises:
        UsuarioInexistente: Si el UID del usuario proveído es inexistente.
        Errorinterno: Si ocurre alguna excepción al tratar de validar el token.
    Returns:
        int: Código de estado indicando el resultado de la operación.
    """
    try:
        set_custom_user_claims(
            uid, {"admin": False, "eliminado": False}, app=firebase_app
        )
        return COD_EXITO
    except NotFoundError:
        raise UsuarioInexistente()
    except:
        raise ErrorInterno(textos[idioma]["errAsignarRol"])


def validar_token(
    firebase_app: App, token: str, textos: dict, idioma: str
) -> dict | None:
    """
    Verifica si el token de Firebase es válido.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        token (str): El token de Firebase a verificar.
        textos (dict): Diccionario con los textos de la aplicación.
        idioma (str): Código de idioma de la aplicación
    Raises:
        AccesoNoAutorizado: Si el token no es válido o ha expirado
        ErrorInterno: Si ocurre alguna excepción al tratar de validar el token
    Returns:
        dict: Datos del token si este es válido y está vigente.
    """
    try:
        return verify_id_token(token, firebase_app, check_revoked=True)
    except (ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError):
        raise AccesoNoAutorizado({"error": textos[idioma]["errTokenExpirado"]})
    except:
        raise ErrorInterno(textos[idioma]["errValidartoken"])


def ver_datos_usuario(firebase_app: App, uid: str, textos: dict, idioma: str) -> dict:
    """
    Obtiene los datos de un usuario específico usando el UID.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        uid (str): El UID del usuario a buscar.
        textos (dict): El diccionario de textos para los mensajes de error.
        idioma (str): El idioma para los mensajes de error.
    Raises:
        UsuarioInexistente: Si el UID del usuario proveído es inexistente.
        Errorinterno: Si ocurre alguna excepción al tratar de validar el token.
    Returns:
        dict: Datos del usuario si se encuentra.
    """
    try:
        usuario = get_user(uid, firebase_app)
        claims = usuario.custom_claims or {}

        if claims.get("eliminado", False):
            raise UsuarioInexistente()

        return {
            "correo": usuario.email,
            "uid": usuario.uid,
            "nombre": usuario.display_name,
            "administrador": claims.get("admin", False),
            "estado": not usuario.disabled,
            "fecha_registro": convertir_datetime_str(
                usuario.user_metadata.creation_timestamp
            ),
            "ultima_conexion": convertir_datetime_str(
                usuario.user_metadata.last_refresh_timestamp
            ),
        }
    except:
        raise ErrorInterno(textos[idioma]["errObtenerUsuario"])


def ver_datos_usuarios(firebase_app: App, textos: dict, idioma: str) -> list[dict]:
    """
    Obtiene los datos de los usuarios registrados en Firebase.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        textos (dict): Diccionario con los textos de la aplicación.
        idioma (str): Código de idioma de la aplicación
    Raises:
        Errorinterno: Si ocurre alguna excepción al tratar de validar el token
    Returns:
        list[dict]: Los datos de los usuarios si se obtuvieron correctamente
    """
    try:
        AUX = []
        usuarios = list_users(app=firebase_app)

        while True:
            lista = []
            for x in usuarios.users:
                CLAIMS = x.custom_claims or {}
                if not CLAIMS.get("eliminado", True):
                    lista.append(
                        {
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
                            ),
                        }
                    )
            AUX.extend(lista)
            if not usuarios.has_next_page:
                break
            else:
                usuarios = usuarios.get_next_page()
        return AUX
    except:
        raise ErrorInterno(textos[idioma]["errObtenerDatosUsuarios"])


def verificar_token(
    firebase_app: App, token: str, textos: dict, idioma: str
) -> dict | None:
    """
    Verifica el token de Firebase en la solicitud.
    Args:
        firebase_app (App): La instancia de la aplicación Firebase.
        token (str): El token de autorización de la solicitud.
        textos (dict): Diccionario con los textos de la aplicación.
        idioma (str): Código de idioma de la aplicación
    Raises:
        AccesoNoAutorizado: Si el token no es válido o ha expirado
        ErrorInterno: Si ocurre alguna excepción al tratar de validar el token
    Returns:
        dict: Datos del token si este es válido y está vigente.
    """
    token = token.split("Bearer ")[1]
    reg_validacion = validar_txt_token(token)

    if not reg_validacion:
        raise AccesoNoAutorizado({"error": textos[idioma]["errTokenInvalido"]})

    return validar_token(firebase_app, token, textos, idioma)
