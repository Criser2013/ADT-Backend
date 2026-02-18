from apis.FirebaseAuth import ver_datos_token
from apis.Firestore import verificar_rol_usuario
from fastapi import Header, Request
from fastapi.responses import JSONResponse
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO, COD_EXITO


async def verificar_usuario_administrador(
    peticion: Request,
    language: str | None = Header(default="es"),
    authorization: str | None = Header(default=""),
) -> tuple[bool, JSONResponse | None]:
    """
    Verifica si el usuario está autenticado y es administrador antes de permitir el acceso a las rutas protegidas.

    Args:
        peticion (Request): La solicitud HTTP entrante.
        language (str | None): El idioma de la solicitud HTTP.
        authorization (str | None): El token de autorización de Firebase.
    Returns:
        tuple: Un tuple que contiene un booleano indicando si el usuario está autenticado y es administrador, y
        en caso de error, un JSONResponse con el mensaje de error y el código de estado correspondiente.
    """
    firebase_app = peticion.state.firebase_app
    TEXTOS = peticion.state.textos
    idioma = language if language in ("es", "en") else "es"
    try:
        RES, DATOS = ver_datos_token(authorization, firebase_app, idioma, TEXTOS)

        if RES in (COD_ERROR_INESPERADO, COD_ERROR_ESPERADO):
            return False, JSONResponse(
                DATOS,
                status_code=403 if RES == COD_ERROR_ESPERADO else 400,
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
