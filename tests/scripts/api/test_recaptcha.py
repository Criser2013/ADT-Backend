from app.apis.Recaptcha import manejador_errores, verificar_peticion_recaptcha
from pytest_mock import MockerFixture
from requests import Response

def test_68():
    """
    Test para validar que la función "manejador_errores" devuelve el mensaje de error correcto
    cuando el token es erroneo.
    """
    RES = manejador_errores("invalid-input-response")
    assert RES == "El token proveído tiene errores."

def test_69():
    """
    Test para validar que la función "manejador_errores" devuelve el mensaje de error correcto
    cuando el token ya expiró o no es válido.
    """
    RES = manejador_errores("timeout-or-duplicate")
    assert RES == "El token ha expirado o ya fue utilizado."

def test_70():
    """
    Test para validar que la función "manejador_errores" no devuelve ningún mensaje cuando el
    error no es conocido.
    """
    RES = manejador_errores("invalid-input-secret")
    assert RES == "invalid-input-secret"

def test_71(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_peticion_recaptcha" no procesa los errores sino
    han habido.
    """

    RESPUESTA = mocker.MagicMock(spec=Response)
    RESPUESTA.json.return_value = {"success": True, "hostname": "host.com"}

    MOCK = mocker.patch("app.apis.Recaptcha.post")
    MOCK.return_value = RESPUESTA

    FUNC = mocker.patch("app.apis.Recaptcha.manejador_errores")
    RES = verificar_peticion_recaptcha("token_valido")

    assert RES == {"success": True, "hostname": "host.com" }
    FUNC.assert_not_called()

def test_72(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_peticion_recaptcha" no procese los errores.
    """

    RESPUESTA = mocker.MagicMock(spec=Response)
    RESPUESTA.json.return_value = {"success": False, "error-codes": ["invalid-input-response", "timeout-or-duplicate"]}

    MOCK = mocker.patch("app.apis.Recaptcha.post")
    MOCK.return_value = RESPUESTA

    RES = verificar_peticion_recaptcha("token_invalido")

    assert RES == {"success": False, "error-codes": ["El token proveído tiene errores.", "El token ha expirado o ya fue utilizado."] }