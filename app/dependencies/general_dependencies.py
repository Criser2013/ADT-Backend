from apis.FirebaseAuth import verificar_token
from fastapi import Header, Request


def verificar_idioma(language: str | None = Header(default="es")) -> str:
    """
    Verifica si el idioma de la solicitud es válido.
    Args:
        language (str | None): El idioma de la solicitud HTTP.
    Returns:
        str: El idioma de la solicitud, por defecto "es" (español).
    """
    return "es" if language not in ("es", "en") else language


def verificar_autenticado(
    peticion: Request,
    authorization: str = Header(default=""),
    language: str = Header(default="es"),
):
    """
    Verifica si el usuario está autenticado.
    Args:
        pet (Request): La solicitud HTTP.
        authorization (str | None): El token de autorización.
        language (str): El idioma de la solicitud.
    """
    firebase_app = peticion.state.firebase_app
    TEXTOS = peticion.state.textos
    verificar_token(firebase_app, authorization, TEXTOS, language)
