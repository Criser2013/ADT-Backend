from fastapi import Request
from app.dependencies.usuarios_dependencies import *
from pytest_mock import MockerFixture
import pytest

@pytest.mark.asyncio
async def test_55(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" retorne los datos si el token es válido
    y el usuario es administrador.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_valido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(1, {"email": "correo@correo.com"}))
    ROL = mocker.patch("app.dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True)

    RES = await verificar_usuario_administrador(PETICION)

    assert RES[0] == True
    assert RES[1] is None

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("correo@correo.com")

@pytest.mark.asyncio
async def test_56(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si el token es inválido.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_invalido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(0, {"error": "Token inválido"}))

    RES = await verificar_usuario_administrador(PETICION)

    assert RES[0] == False
    assert RES[1].status_code == 403
    assert RES[1].body.decode("utf-8") == '{"error":"Token inválido"}'

    DATOS_TOKEN.assert_called_once()

@pytest.mark.asyncio
async def test_57(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si se produjo un error
    al verificar el token
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_invalido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(-1, {"error": "Error al validar el token"}))

    RES = await verificar_usuario_administrador(PETICION)

    assert RES[0] == False
    assert RES[1].status_code == 400
    assert RES[1].body.decode("utf-8") == '{"error":"Error al validar el token"}'

    DATOS_TOKEN.assert_called_once()

@pytest.mark.asyncio
async def test_58(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" no retorne los datos de los usuarios si el usuario no
    es administrador.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_valido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("app.dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=False)

    RES = await verificar_usuario_administrador(PETICION)

    assert RES[0] == False
    assert RES[1].status_code == 403
    assert RES[1].body.decode("utf-8") == '{"error":"Acceso denegado."}'

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")

@pytest.mark.asyncio
async def test_59(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el usuario no
    es administrador.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"authorization": "Bearer token_valido"}

    DATOS_TOKEN = mocker.patch("app.dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")

    RES = await verificar_usuario_administrador(PETICION)

    assert RES[0] == False
    assert RES[1].status_code == 500
    assert RES[1].body.decode("utf-8") == '{"error":"Error al procesar la solicitud: Error inesperado"}'

    DATOS_TOKEN.assert_called_once()