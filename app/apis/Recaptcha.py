from constants import RECAPTCHA_SECRET, RECAPTCHA_API_URL
from requests import post


def manejador_errores(error: str, idioma: str, textos: dict[str, str]) -> str:
    """
    Maneja los errores devueltos por la API de reCAPTCHA.

    Args:
        error (str): El mensaje de error devuelto por la API de reCAPTCHA.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.

    Returns:
        str: Un mensaje de error amigable para el usuario.
    """
    match error:
        case "invalid-input-response":
            return f"{textos[idioma]['errCaptchaTokenErroneo']}"
        case "timeout-or-duplicate":
            return f"{textos[idioma]['errCaptchaTokenInvalido']}"
        case _:
            return error


def verificar_peticion_recaptcha(token: str, idioma: str, textos: dict[str, str]) -> dict:
    """
    Envía una petición al API de ReCAPTCHA para verificar que el token es válido.

    Args:
        token (str): El token de ReCAPTCHA a verificar.
        idioma (str): El idioma para los mensajes de error.
        textos (dict[str, str]): El diccionario de textos para los mensajes de error.

    Returns:
        dict: La respuesta del API de ReCAPTCHA.
    """
    cuerpo = {"secret": RECAPTCHA_SECRET, "response": token}
    res = post(
        RECAPTCHA_API_URL,
        data=cuerpo,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res = res.json()

    for key, value in res.items():
        if key == "error-codes":
            res[key] = [manejador_errores(i, idioma, textos) for i in value]

    return res
