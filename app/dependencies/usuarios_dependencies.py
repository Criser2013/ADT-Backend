from apis.FirebaseAuth import verificar_token
from dependencies.general_dependencies import verificar_idioma
from fastapi import Header, Request, Depends
from models.Excepciones import AccesoNoAutorizado, UIDInvalido
from urllib.parse import unquote
from utils.Validadores import validar_uid


async def verificar_usuario_administrador(
    peticion: Request,
    authorization: str = Header(default=""),
    idioma: str = Depends(verificar_idioma),
):
    """
    Verifica si el usuario está autenticado y es administrador antes de permitir el acceso a las rutas protegidas.

    Args:
        peticion (Request): La solicitud HTTP entrante.
        authorization (str | None): El token de autorización de Firebase.
        idioma (str): El idioma preferido del usuario, obtenido a través de la dependencia `verificar_idioma`.
    Raises:
        AccesoNoAutorizado: Si el token no es válido o ha expirado
        ErrorInterno: Si ocurre alguna excepción al tratar de validar el token
    """
    firebase_app = peticion.state.firebase_app
    TEXTOS = peticion.state.textos
    DATOS = verificar_token(firebase_app, authorization, TEXTOS, idioma) or {}

    if not DATOS.get("admin", False):
        raise AccesoNoAutorizado(TEXTOS[idioma]["errAccesoDenegado"])


async def validador_uid(uid: str) -> str:
    """
    Valida el UID proporcionado en la solicitud. Si es inválido lanza una excepción.

    Args:
        peticion (Request): La solicitud HTTP entrante.
    Raises:
        UIDInvalido: Si el UID proveído no sigue el formato especificado.
    Returns:
        str: El UID validado.
    """
    uid = unquote(uid)
    VALIDACION = validar_uid(uid)

    if not VALIDACION:
        raise UIDInvalido()

    return uid
