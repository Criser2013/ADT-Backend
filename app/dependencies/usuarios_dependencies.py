from firebase_admin_config import firebase_app
from apis.FirebaseAuth import ver_datos_token
from apis.Firestore import verificar_rol_usuario
from fastapi import Request
from fastapi.responses import JSONResponse

async def verificar_usuario_administrador (req: Request) -> tuple[bool, JSONResponse | None]:
    """
    Verifica si el usuario está autenticado y es administrador antes de permitir el acceso a las rutas protegidas.

    Args:
        req (Request): La solicitud HTTP que contiene el token de autorización.
    Returns:
        tuple: Un tuple que contiene un booleano indicando si el usuario está autenticado y es administrador, y
        en caso de error, un JSONResponse con el mensaje de error y el código de estado correspondiente.
    """
    try:
        RES, DATOS = ver_datos_token(req, firebase_app)

        if RES in (-1, 0):
            return False, JSONResponse(
                DATOS,
                status_code=403 if RES == 0 else 400,
                media_type="application/json",
            )

        VALIDAR_ROL = await verificar_rol_usuario(DATOS["email"])

        if not VALIDAR_ROL:
            return False, JSONResponse(
                {"error": "Acceso denegado."},
                status_code=403,
                media_type="application/json",
            )

        return True, None
    except Exception as e:
        return False, JSONResponse(
            {"error": f"Error al procesar la solicitud: {str(e)}"},
            status_code=500,
            media_type="application/json",
        )