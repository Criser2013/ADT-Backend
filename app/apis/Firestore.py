from firebase_admin import firestore_async
from constants import ROL_ADMIN
from utils.Validadores import validar_correo


async def verificar_rol_usuario(correo: str) -> bool:
    """
    Válida si el correo ingresado es un administrador.

    Args:
        correo (str): Correo del usuario.
    Returns:
        bool: El usuario con el correo asociado tiene el rol de administrador.
    """
    VALIDACION = validar_correo(correo)
    if not VALIDACION:
        return False

    DB = firestore_async.client()
    REF = DB.document(f"usuarios/{correo}")
    rol = await REF.get(["rol"])
    rol = rol.to_dict()

    return rol["rol"] == ROL_ADMIN