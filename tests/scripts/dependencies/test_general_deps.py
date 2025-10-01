import pytest
from fastapi import Request
from pytest_mock import MockerFixture
from app.dependencies.general_dependencies import verificar_idioma

@pytest.mark.asyncio
async def test_89(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_idioma" retorne el idioma de la petición
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"language": "en"}

    VALIDACION = mocker.patch("app.dependencies.general_dependencies.ver_si_existe_clave", return_value=True)
    RES = await verificar_idioma(PETICION)

    assert RES == "en"
    VALIDACION.assert_called_once_with(PETICION.headers, "language")

@pytest.mark.asyncio
async def test_90(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_idioma" retorne el idioma "es" cuando se recibe
    un idioma inválido.
    """
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.headers = {"language": "fr"}

    VALIDACION = mocker.patch("app.dependencies.general_dependencies.ver_si_existe_clave", return_value=True)
    RES = await verificar_idioma(PETICION)

    assert RES == "es"
    VALIDACION.assert_called_once_with(PETICION.headers, "language")