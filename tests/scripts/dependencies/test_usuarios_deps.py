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