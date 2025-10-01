from utils.Diccionario import ver_si_existe_clave
from fastapi import Request

async def verificar_idioma (req: Request) -> str:
    """
    Verifica si el idioma de la solicitud es válido.

    Args:
        req (Request): La solicitud HTTP que contiene el token de autorización.
    Returns:
        str: El idioma de la solicitud, por defecto "es" (español).
    """
    EXISTE = ver_si_existe_clave(req.headers, "language")
    idioma = "es"
    if EXISTE:
        idioma = "es" if req.headers["language"] not in ("es", "en") else req.headers["language"]
    return idioma