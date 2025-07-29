from firebase_admin import firestore_async
from constants import ROL_ADMIN


async def verificar_rol_usuario(correo: str) -> bool:
    """
    Válida si el correo ingresado es un administrador.

    Args:
        correo (str): Correo del usuario.
    Returns:
        bool: El usuario con el correo asociado tiene el rol de administrador.
    """
    DB = firestore_async.client()
    REF = DB.document(f"usuarios/{correo}")
    rol = await REF.get(["rol"])
    rol = rol.to_dict()

    return rol["rol"] == ROL_ADMIN

async def obtener_roles_usuarios() -> list[dict]:
    """
    Obtiene los datos de los usuarios en la base de datos.

    Returns:
        list[dict]: Lista de diccionarios con los roles de los usuarios.
    """
    DB = firestore_async.client()
    REF = DB.collection("usuarios")
    docs = await REF.get()
    AUX = {}

    for doc in docs:
        data = doc.to_dict()
        AUX[data["correo"]] = data["rol"]

    return AUX

async def obtener_rol_usuario(correo: str) -> int:
    """
    Obtiene el rol del usuario con el correo especificado.

    Args:
        correo (str): Correo del usuario.
    Returns:
        int: Rol del usuario.
    """
    DB = firestore_async.client()
    REF = DB.document(f"usuarios/{correo}")
    doc = await REF.get(["rol"])

    if doc.exists:
        return doc.to_dict()["rol"]
    
    return -1  # Usuario no encontrado