from fastapi import Request
from app.dependencies.usuarios_dependencies import *
from pytest_mock import MockerFixture
import pytest

@pytest.mark.asyncio
async def test_53(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" retorne los datos si el token es válido
    y el usuario es administrador.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_valido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(1, {"uid": "a1234H"}))
    ROL = mocker.patch("app.dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True)

    await verificar_usuario_administrador(PETICION, "", "es")

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")

@pytest.mark.asyncio
async def test_54(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si el token es inválido.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_invalido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(0, {"error": "Token inválido"}))

    with pytest.raises(AccesoNoAutorizado) as exc_info:
        await verificar_usuario_administrador(PETICION, "", "es")
        assert exc_info.value.detail == {"error": "Token inválido."}
        assert exc_info.value.status_code == 403

    DATOS_TOKEN.assert_called_once()

@pytest.mark.asyncio
async def test_55(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si se produjo un error
    al verificar el token
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_invalido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(-1, {"error": "Error al validar el token"}))

    with pytest.raises(AccesoNoAutorizado) as exc_info:
        await verificar_usuario_administrador(PETICION, "", "es")
        assert exc_info.value.detail == {"error": "Error al validar el token"}
        assert exc_info.value.status_code == 403

    DATOS_TOKEN.assert_called_once()

@pytest.mark.asyncio
async def test_56(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si el usuario no
    es administrador.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_valido"}
    PETICION.state.textos = { "es":  { "errAccesoDenegado": "Acceso denegado." } }

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(1, {"uid": "a1234H"}))
    ROL = mocker.patch("app.dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=False)

    with pytest.raises(AccesoNoAutorizado) as exc_info:
        await verificar_usuario_administrador(PETICION, "", "es")
        assert exc_info.value.detail == {"error": "Acceso denegado."}
        assert exc_info.value.status_code == 403

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")

@pytest.mark.asyncio
async def test_57(mocker: MockerFixture):
    """
    Test para validar que la dependencia "validador_uid" retorne el uid si es válido.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.textos = {}
    VALIDAR_UID = mocker.patch("app.dependencies.usuarios_dependencies.validar_uid", return_value=True)

    RES = await validador_uid(PETICION, "a1234H", "es")

    assert RES == "a1234H"
    VALIDAR_UID.assert_called_once_with("a1234H")

@pytest.mark.asyncio
async def test_44(mocker: MockerFixture):
    """
    Test para validar que la dependencia "validador_uid" arroje una excepción si el uid es inválido.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.textos = { "es":  { "errUIDInvalido": "UID inválido." } }

    VALIDAR_UID = mocker.patch("app.dependencies.usuarios_dependencies.validar_uid", return_value=False)

    with pytest.raises(UIDInvalido) as exc_info:
        await validador_uid(PETICION, "a1234H", "es")
        assert exc_info.value.detail == {"error": "UID inválido."}

    VALIDAR_UID.assert_called_once_with("a1234H")