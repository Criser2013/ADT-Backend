from apis.FirebaseAuth import ver_datos_token
from apis.Firestore import verificar_rol_usuario
from fastapi import Header, Request, Depends
from fastapi.responses import JSONResponse
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO
from models.Excepciones import AccesoNoAutorizado
from dependencies.general_dependencies import verificar_idioma


async def verificar_usuario_administrador(
    peticion: Request,
    authorization: str | None = Header(default=""),
    idioma: str = Depends(verificar_idioma)
) -> tuple[bool, JSONResponse | None]:
    """
    Verifica si el usuario está autenticado y es administrador antes de permitir el acceso a las rutas protegidas.

    Args:
        peticion (Request): La solicitud HTTP entrante.
        authorization (str | None): El token de autorización de Firebase.
        idioma (str): El idioma preferido del usuario, obtenido a través de la dependencia `verificar_idioma`.
    """
    firebase_app = peticion.state.firebase_app
    TEXTOS = peticion.state.textos

    RES, DATOS = ver_datos_token(authorization, firebase_app, idioma, TEXTOS)

    if RES in (COD_ERROR_INESPERADO, COD_ERROR_ESPERADO):
        raise AccesoNoAutorizado(DATOS, 403)

    VALIDAR_ROL = await verificar_rol_usuario(DATOS["uid"])

    if not VALIDAR_ROL:
        raise AccesoNoAutorizado(TEXTOS[idioma]['errAccesoDenegado'], 403)