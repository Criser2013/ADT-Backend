from constants import RECAPTCHA_SECRET, RECAPTCHA_API_URL
from requests import post

def manejador_errores(error):
    match error:
        case "invalid-input-response":
            return "El token proveído tiene errores."
        case "timeout-or-duplicate":
            return "El token ha expirado o ya fue utilizado."

def verificar_peticion_recaptcha(token):
    """
    Envía una petición al API de ReCAPTCHA para verificar que el token es válido.

    Args:
        token (str): El token de ReCAPTCHA a verificar.

    Returns:
        dict: La respuesta del API de ReCAPTCHA.
    """
    cuerpo = {
        "secret": RECAPTCHA_SECRET,
        "response": token
    }
    res = post(RECAPTCHA_API_URL, data=cuerpo, headers={"Content-Type": "application/x-www-form-urlencoded"})
    res = res.json()

    for key, value in res.items():
        if key == "error-codes":
            res[key] = [manejador_errores(i) for i in value]

    return res