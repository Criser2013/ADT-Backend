from apis.FirebaseAuth import *
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO, COD_EXITO
from dependencies.general_dependencies import verificar_idioma
from dependencies.usuarios_dependencies import *
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models.Excepciones import UsuarioInexistente, ErrorInterno
from models.Peticiones import UsuarioActualizar

router = APIRouter(
    prefix="/usuarios", dependencies=[Depends(verificar_usuario_administrador)]
)


@router.patch("/{uid}")
async def actualizar_usuario(
    peticion: Request,
    instancia_usuario: UsuarioActualizar,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    CODIGO, RES = actualizar_estado_usuario(firebase_app, uid, instancia_usuario)

    if CODIGO == COD_ERROR_ESPERADO:
        raise UsuarioInexistente({"error": TEXTOS[idioma]["errUsuarioNoEncontrado"]})
    elif CODIGO == COD_ERROR_INESPERADO:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']}"},
            status_code=500,
            media_type="application/json",
        )
    else:
        return JSONResponse(RES, status_code=200, media_type="application/json")


@router.get("/{uid}")
async def ver_usuario(
    peticion: Request,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    CODIGO, RES = await ver_datos_usuario(firebase_app, uid)

    if CODIGO == COD_ERROR_ESPERADO:
        raise UsuarioInexistente({"error": TEXTOS[idioma]["errUsuarioNoEncontrado"]})
    elif CODIGO == COD_ERROR_INESPERADO:
        raise ErrorInterno({"error": TEXTOS[idioma]["errObtenerDatosUsuarios"]})
    else:
        return JSONResponse(RES, status_code=200, media_type="application/json")


@router.get("")
async def ver_usuarios(
    peticion: Request, idioma: str = Depends(verificar_idioma)
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app
    COD, RES = await ver_datos_usuarios(firebase_app)

    if COD != COD_EXITO:
        raise ErrorInterno({"error": TEXTOS[idioma]["errObtenerDatosUsuarios"]})

    return JSONResponse(
        {"usuarios": RES}, status_code=200, media_type="application/json"
    )
