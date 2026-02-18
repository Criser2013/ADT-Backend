from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from apis.FirebaseAuth import *
from utils.Validadores import validar_uid
from urllib.parse import unquote
from dependencies.usuarios_dependencies import verificar_usuario_administrador
from dependencies.general_dependencies import verificar_idioma

router = APIRouter(
    prefix="/usuarios",
    dependencies=[Depends(verificar_usuario_administrador), Depends(verificar_idioma)],
)


@router.get("")
async def ver_usuarios(
    peticion: Request,
    res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(
        verificar_usuario_administrador
    ),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    try:
        TEXTOS = peticion.state.textos
        firebase_app = peticion.state.firebase_app
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        RES = await ver_datos_usuarios(firebase_app)
        if RES is None:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errObtenerDatosUsuarios']}"},
                status_code=400,
                media_type="application/json",
            )
        else:
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
    uid: str,
    res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(
        verificar_usuario_administrador
    ),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    try:
        TEXTOS = peticion.state.textos
        firebase_app = peticion.state.firebase_app
        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        uid = unquote(uid)
        VALIDACION = validar_uid(uid)

        if not VALIDACION:
            raise ValueError(f"{TEXTOS[idioma]['errUIDInvalido']}")

        CODIGO, RES = await ver_datos_usuario(firebase_app, uid)
        if CODIGO == 1:
            return RES
        elif CODIGO == 0:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errUsuarioNoEncontrado']}"},
                status_code=404,
                media_type="application/json",
            )
        else:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errObtenerDatosUsuarios']}: {RES}"},
                status_code=400,
                media_type="application/json",
            )
    except ValueError:
        return JSONResponse(
            {"error": TEXTOS[idioma]["errUIDInvalido"]},
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )


@router.patch("/{uid}")
async def actualizar_usuario(
    peticion: Request,
    uid: str,
    desactivar: bool,
    res_validacion_auth: tuple[bool, JSONResponse | None] = Depends(
        verificar_usuario_administrador
    ),
    idioma: str = Depends(verificar_idioma),
) -> JSONResponse:
    try:
        TEXTOS = peticion.state.textos
        firebase_app = peticion.state.firebase_app

        if not res_validacion_auth[0]:
            return res_validacion_auth[1]

        uid = unquote(uid)
        VALIDACION = validar_uid(uid)

        if not VALIDACION:
            raise ValueError(f"{TEXTOS[idioma]['errUIDInvalido']}")

        DATOS = ver_usuario_firebase(firebase_app, uid)
        if DATOS[0] == 0:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errUsuarioNoEncontrado']}"},
                status_code=404,
                media_type="application/json",
            )
        elif DATOS[0] == -1:
            raise Exception(f"{TEXTOS[idioma]['errObtenerUsuario']}")

        CODIGO, RES = actualizar_estado_usuario(firebase_app, uid, desactivar)

        if CODIGO == 1:
            return RES
        elif CODIGO == 0:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errEstadoInvalido']}"},
                status_code=401,
                media_type="application/json",
            )
        else:
            return JSONResponse(
                {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
                status_code=500,
                media_type="application/json",
            )
    except ValueError:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errUIDInvalido']}"},
            status_code=400,
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            {"error": f"{TEXTOS[idioma]['errTry']} {str(e)}"},
            status_code=500,
            media_type="application/json",
        )
