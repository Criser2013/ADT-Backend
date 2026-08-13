from apis.FirebaseAuth import *
from dependencies.general_dependencies import verificar_idioma
from dependencies.usuarios_dependencies import *
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.Peticiones import DatosUsuario
from models.Respuestas import Usuario

router = APIRouter(
    prefix="/usuarios", dependencies=[Depends(verificar_usuario_administrador)]
)


@router.patch("/{uid}")
def actualizar_usuario(
    peticion: Request,
    instancia_usuario: DatosUsuario,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> Usuario:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    return actualizar_datos_usuario(firebase_app, uid, instancia_usuario, TEXTOS, idioma)


@router.get("/{uid}")
def ver_usuario(
    peticion: Request,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> Usuario:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    return ver_datos_usuario(firebase_app, uid, TEXTOS, idioma)


@router.get("")
def ver_usuarios(
    peticion: Request, idioma: str = Depends(verificar_idioma)
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    RES = ver_datos_usuarios(firebase_app, TEXTOS, idioma)
    return JSONResponse(
        {"usuarios": RES}, status_code=200, media_type="application/json"
    )
