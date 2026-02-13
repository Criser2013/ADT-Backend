from fastapi import Header

async def verificar_idioma (language: str | None = Header(default="es")) -> str:
    """
    Verifica si el idioma de la solicitud es válido.

    Args:
        req (Request): La solicitud HTTP que contiene el token de autorización.
    Returns:
        str: El idioma de la solicitud, por defecto "es" (español).
    """
    return "es" if language not in ("es", "en") else language