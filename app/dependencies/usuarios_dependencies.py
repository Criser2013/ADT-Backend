from firebase_admin_config import firebase_app
from apis.FirebaseAuth import ver_datos_token
from apis.Firestore import verificar_rol_usuario
from fastapi import Header
from fastapi.responses import JSONResponse
#from utils.Diccionario import ver_si_existe_clave
from constants import TEXTOS


async def verificar_usuario_administrador(
    language: str | None = Header(default="es"),
    token: str | None = Header(default=None),
) -> tuple[bool, JSONResponse | None]:
    """
    Verifica si el usuario está autenticado y es administrador antes de permitir el acceso a las rutas protegidas.

    Args:
        language (str | None): El idioma de la solicitud HTTP.
        token (str | None): El token de autenticación de Firebase.
    Returns:
        tuple: Un tuple que contiene un booleano indicando si el usuario está autenticado y es administrador, y
        en caso de error, un JSONResponse con el mensaje de error y el código de estado correspondiente.
    """
    idioma = language if language in ("es", "en") else "es"
    try:
        RES, DATOS = ver_datos_token(token, firebase_app, idioma)

        if RES in (-1, 0):
            return False, JSONResponse(
                DATOS,
                status_code=403 if RES == 0 else 400,
                media_type="application/json",
            )

        VALIDAR_ROL = await verificar_rol_usuario(DATOS["uid"])

        if not VALIDAR_ROL:
            return False, JSONResponse(
                {"error": f"{TEXTOS[idioma]['errAccesoDenegado']}"},
                status_code=403,
                media_type="application/json",
            )

        return True, None
    except Exception as e:
        return False, JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
