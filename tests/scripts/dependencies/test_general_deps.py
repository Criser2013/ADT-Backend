import pytest
from pytest_mock import MockerFixture
from fastapi import Request
from dependencies.general_dependencies import *


@pytest.mark.parametrize(
    "idioma,respuesta_esperada",
    [("en", "en"), ("fr", "es")],
    ids=["test_89", "test_90"],
)
def test_verificar_idioma(idioma, respuesta_esperada):
    """
    Test para validar que la dependencia "verificar_idioma" retorne el idioma de la petición
    """
    RES = verificar_idioma(idioma)
    assert RES == respuesta_esperada


def test_91(mocker: MockerFixture):
    """
    Test para validar que la dependencia "verificar_autenticado" permita el acceso
    cuando recibe un token válido
    """
    TEXTOS = {
        "es": {
            "errAccesoDenegado": "Acceso denegado",
            "errTokenInvalido": "Token inválido",
        }
    }
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.firebase_app = "FIREBASE_APP"
    PETICION.state.textos = TEXTOS
    FUNC = mocker.patch(
        "dependencies.general_dependencies.verificar_token",
        return_value={"display_name": "usuario", "uid": "1234"},
    )

    verificar_autenticado(PETICION, "Bearer token_valido", "es")
    FUNC.assert_called_once_with("FIREBASE_APP", "Bearer token_valido", TEXTOS, "es")
