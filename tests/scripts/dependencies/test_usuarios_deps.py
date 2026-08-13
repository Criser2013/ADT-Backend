from fastapi import Request
from dependencies.usuarios_dependencies import *
from pytest_mock import MockerFixture
import pytest


@pytest.mark.parametrize(
    "token,mock_token,arroja_excepcion",
    [
        ("Bearer token_valido", {"uid": "a1234H", "admin": True}, False),
        ("Bearer token_invalido", {"uid": "a1234H", "admin": False}, True),
    ],
    ids=["test_53", "test_54"],
)
def test_verificar_usuario_administrador(
    mocker: MockerFixture, token, mock_token, arroja_excepcion
):
    """
    Test para validar que la dependencia "verificar_usuario_administrador" retorne los datos si el token es válido
    y el usuario es administrador.
    """
    TEXTOS = {
        "es": {
            "errAccesoDenegado": "Acceso denegado",
            "errTokenInvalido": "Token inválido",
        }
    }
    PETICION = mocker.MagicMock(spec=Request)
    PETICION.state.textos = TEXTOS
    PETICION.state.firebase_app = "firebase_app"
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=mock_token,
    )

    if arroja_excepcion:
        with pytest.raises(AccesoNoAutorizado) as exc_info:
            verificar_usuario_administrador(PETICION, token, "es")
            assert exc_info.value.mensaje == "Acceso denegado."
    else:
        verificar_usuario_administrador(PETICION, token, "es")

    DATOS_TOKEN.assert_called_once_with("firebase_app", token, TEXTOS, "es")


@pytest.mark.parametrize(
    "uid,respuesta_esperada,mock_validador,arroja_excepcion",
    [("a1234H", "a1234H", True, False), ("a1235-o", "UID inválido", False, True)],
    ids=["test_57", "test_44"],
)
def test_validador_uid(
    mocker: MockerFixture, uid, respuesta_esperada, mock_validador, arroja_excepcion
):
    """
    Test para validar que la dependencia "validador_uid" retorne el uid si es válido.
    """
    VALIDAR_UID = mocker.patch(
        "dependencies.usuarios_dependencies.validar_uid",
        return_value=mock_validador,
    )

    if arroja_excepcion:
        with pytest.raises(UIDInvalido):
            validador_uid(uid)
    else:
        RES = validador_uid(uid)
        assert RES == respuesta_esperada

    VALIDAR_UID.assert_called_once_with(uid)
