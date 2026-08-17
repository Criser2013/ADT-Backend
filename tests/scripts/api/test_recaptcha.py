import pytest
from apis.Recaptcha import manejador_errores, verificar_peticion_recaptcha
from pytest_mock import MockerFixture
from requests import Response
from tests.scripts.conftest import MOCK_TEXTOS


@pytest.mark.parametrize(
    "error,respuesta_esperada",
    [
        ("invalid-input-response", MOCK_TEXTOS["es"]["errCaptchaTokenErroneo"]),
        ("timeout-or-duplicate", MOCK_TEXTOS["es"]["errCaptchaTokenInvalido"]),
        ("invalid-input-secret", "invalid-input-secret"),
    ],
    ids=["test_68", "test_69", "test_70"],
)
def test_manejador_errores(error, respuesta_esperada):
    """
    Test para validar que la función "manejador_errores" devuelve el mensaje de error correcto
    cuando el token es erroneo.
    """
    RES = manejador_errores(error, "es", MOCK_TEXTOS)
    assert RES == respuesta_esperada


@pytest.mark.parametrize(
    "token,respuesta_esperada,mock_peticion",
    [
        (
            "token_valido",
            {"success": True, "hostname": "host.com"},
            {"success": True, "hostname": "host.com"},
        ),
        (
            "token_invalido",
            {
                "success": False,
                "hostname": "host.com",
                "error-codes": [
                    MOCK_TEXTOS["es"]["errCaptchaTokenErroneo"],
                    MOCK_TEXTOS["es"]["errCaptchaTokenInvalido"],
                ],
            },
            {
                "success": False,
                "hostname": "host.com",
                "error-codes": ["invalid-input-response", "timeout-or-duplicate"],
            },
        ),
    ],
    ids=["test_71","test_72"]
)
def test_verificar_peticion_recaptcha(mocker: MockerFixture, token, respuesta_esperada, mock_peticion):
    """
    Test para validar que la función "verificar_peticion_recaptcha" no procesa los errores sino
    han habido.
    """
    RESPUESTA = mocker.MagicMock(spec=Response)
    RESPUESTA.json.return_value = mock_peticion
    RECAPTCHA = mocker.patch("apis.Recaptcha.post", return_value=RESPUESTA)
    RES = verificar_peticion_recaptcha(token, "es", MOCK_TEXTOS)

    assert RES["success"] == respuesta_esperada["success"]
    assert RES["hostname"] == respuesta_esperada["hostname"]

    if not respuesta_esperada["success"]:
        assert RES["error-codes"] == respuesta_esperada["error-codes"]

    RECAPTCHA.assert_called_once_with(
        "url",
        data={"secret": "secret_token", "response": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
