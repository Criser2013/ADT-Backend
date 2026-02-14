import pytest
from pytest_mock import MockerFixture
from app.dependencies.general_dependencies import verificar_idioma

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