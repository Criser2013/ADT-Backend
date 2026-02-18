from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import *
from dependencies.usuarios_dependencies import *
from dependencies.general_dependencies import verificar_idioma
from constants import COD_ERROR_ESPERADO, COD_ERROR_INESPERADO, COD_EXITO
from models.Excepciones import UsuarioInexistente, ErrorInterno

router = APIRouter(
    prefix="/usuarios", dependencies=[Depends(verificar_usuario_administrador)]
)


@router.get("")
async def ver_usuarios(
    peticion: Request, idioma: str = Depends(verificar_idioma)
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app

    try:
        COD, RES = await ver_datos_usuarios(firebase_app)

        if COD != COD_EXITO:
            raise ErrorInterno({"error": TEXTOS[idioma]["errObtenerDatosUsuarios"]})

        return RES
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.get("/{uid}")
async def ver_usuario(
    peticion: Request,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app

    try:
        CODIGO, RES = await ver_datos_usuario(firebase_app, uid)

        if CODIGO == COD_ERROR_ESPERADO:
            raise UsuarioInexistente(
                {"error": TEXTOS[idioma]["errUsuarioNoEncontrado"]}
            )
        elif CODIGO == COD_ERROR_INESPERADO:
            raise ErrorInterno({"error": TEXTOS[idioma]["errObtenerDatosUsuario"]})

        return RES
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.patch("/{uid}")
async def actualizar_usuario(
    peticion: Request,
    desactivar: bool,
    uid: str = Depends(validador_uid),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    TEXTOS = peticion.state.textos
    firebase_app = peticion.state.firebase_app

    try:
        COD, RES = ver_usuario_firebase(firebase_app, uid)

        if COD == COD_ERROR_ESPERADO:
            raise UsuarioInexistente(
                {"error": TEXTOS[idioma]["errUsuarioNoEncontrado"]}
            )
        elif COD == COD_ERROR_INESPERADO:
            raise Exception(f"{TEXTOS[idioma]['errObtenerUsuario']}")

        CODIGO, RES = actualizar_estado_usuario(firebase_app, uid, desactivar)

        if CODIGO != COD_EXITO:
            TEXTO = "errEstadoInvalido" if CODIGO == COD_ERROR_ESPERADO else "errTry"
            COD = 401 if CODIGO == COD_ERROR_ESPERADO else 500
            return JSONResponse(
                {"error": f"{TEXTOS[idioma][TEXTO]}"},
                status_code=COD,
                media_type="application/json",
            )

        return RES
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
