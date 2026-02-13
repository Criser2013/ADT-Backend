from firebase_admin import firestore_async
from constants import ROL_ADMIN


async def verificar_rol_usuario(uid: str) -> bool:
    """
    Válida si el uid ingresado es un administrador.

    Args:
        uid (str): UID del usuario.
    Returns:
        bool: El usuario con el uid asociado tiene el rol de administrador.
    """
    DB = firestore_async.client()
    REF = DB.document(f"usuarios/{uid}")
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
        AUX[doc.id] = data["rol"]

    return AUX


async def obtener_rol_usuario(uid: str) -> int:
    """
    Obtiene el rol del usuario con el UID especificado.

    Args:
        uid (str): UID del usuario.
    Returns:
        int: Rol del usuario.
    """
    DB = firestore_async.client()
    REF = DB.document(f"usuarios/{uid}")
    doc = await REF.get(["rol"])

    if doc.exists:
        return doc.to_dict()["rol"]

    return -1  # Usuario no encontrado
