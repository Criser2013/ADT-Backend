import pytest
from pytest_mock import MockerFixture
from fastapi import Request
from app.dependencies.general_dependencies import *

@pytest.mark.asyncio
async def test_89():
    """
    Test para validar que la dependencia "verificar_idioma" retorne el idioma de la petición
    """
    RES = await verificar_idioma("en")

    assert RES == "en"

@pytest.mark.asyncio
async def test_90():
    """
    Test para validar que la dependencia "verificar_idioma" retorne el idioma "es" cuando se recibe
    un idioma inválido.
    """
    RES = await verificar_idioma("fr")

    assert RES == "es"

@pytest.mark.asyncio
async def test_91(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_autenticado" permita el acceso
    cuando recibe un token válido
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.firebase_app = "FIREBASE_APP"
    PETICION.state.textos = {"es": {"errAccesoDenegado": "Acceso denegado", "errTokenInvalido": "Token inválido"}}
    FUNC = mocker.patch("app.dependencies.general_dependencies.verificar_token", return_value=COD_EXITO)

    await verificar_autenticado(PETICION, "Bearer token_valido", "es")

    FUNC.assert_called_once_with("FIREBASE_APP", "Bearer token_valido")

@pytest.mark.asyncio
async def test_92(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_autenticado" lance una excepción
    con el mensaje adecuado cuando recibe un token inválido
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.firebase_app = "FIREBASE_APP"
    PETICION.state.textos = {"es": {"errAccesoDenegado": "Acceso denegado", "errTokenInvalido": "Token inválido"}}
    FUNC = mocker.patch("app.dependencies.general_dependencies.verificar_token", return_value=COD_ERROR_ESPERADO)

    with pytest.raises(AccesoNoAutorizado) as EXC:
        await verificar_autenticado(PETICION, "Bearer token_invalido", "es")
        assert EXC.mensaje == {"error": "Acceso denegado"}

    FUNC.assert_called_once_with("FIREBASE_APP", "Bearer token_invalido")

@pytest.mark.asyncio
async def test_93(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_autenticado" lance una excepción
    con el mensaje adecuado cuando recibe un token inválido
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.firebase_app = "FIREBASE_APP"
    PETICION.state.textos = {"es": {"errAccesoDenegado": "Acceso denegado", "errTokenInvalido": "Token inválido"}}
    FUNC = mocker.patch("app.dependencies.general_dependencies.verificar_token", return_value=COD_ERROR_ESPERADO)

    with pytest.raises(AccesoNoAutorizado) as EXC:
        await verificar_autenticado(PETICION, "Bearer token_invalido", "es")
        assert EXC.mensaje == {"error": "Token inválido"}

    FUNC.assert_called_once_with("FIREBASE_APP", "Bearer token_invalido")