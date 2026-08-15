import pytest
from constants import cargar_credenciales_cliente_firebase, inicializar_modelos_ml
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from firebase_admin import App
from firebase_admin.auth import UserNotFoundError
from firebase_admin.credentials import Certificate
from firebase_admin.exceptions import FirebaseError
from firebase_admin_config import inicializar_firebase
from main import app
from pytest import MonkeyPatch
from pytest_mock import MockerFixture


# Constantes de prueba
MOCK_TEST_CREDS = {
    "apiKey": "test_api_key",
    "authDomain": "test_auth_domain",
    "projectId": "test_project_id",
    "storageBucket": "test_storage_bucket",
    "messagingSenderId": "test_messaging_sender_id",
    "appId": "test_app_id",
    "measurementId": "test_measurement_id",
    "driveScopes": [
        "https://www.googleapis.com/auth/drive",
    ],
    "reCAPTCHA": "test_captcha",
}

MOCK_FIREBASE_APP = {
    "appId": "test_app_id",
    "cred": {"projectId": "test_project_id", "certificated": True},
}

MOCK_TEXTOS = {
    "es": {
        "errTry": "Error de prueba:",
        "errOrigenNoAutorizado": "Origen no autorizado",
        "errHeaderOrigin": "Encabezado 'Origin' no especificado",
        "errUIDInvalido": "UID inválido",
        "errUsuarioNoEncontrado": "Usuario no encontrado",
        "errAccesoDenegado": "Acceso denegado.",
        "errValidarToken": "Error al validar el token",
    }
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    yield {
        "explicador": None,  # Mock del explicador
        "textos": MOCK_TEXTOS,
        "modelo": None,  # Mock del modelo
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": MOCK_TEST_CREDS,
    }


@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    mocker.patch(
        "main.CORS_ORIGINS",
        [
            "http://localhost:5178",
        ],
    )
    mocker.patch(
        "main.ALLOWED_HOSTS",
        [
            "localhost",
        ],
    )
    mocker.patch("main.ORIGENES_AUTORIZADOS", ["http://localhost:5178"])
    yield
    mocker.resetall()


@pytest.mark.parametrize(
    "host,respuesta_esperada,es_satisfactoria",
    [
        ("localhost", {"status_code": 200}, True),
        ("google", {"status_code": 400, "contenido": "Invalid host header"}, False),
    ],
    ids=["test_8", "test_no_asignado"],
)
def test_middleware_trusted_host(host, respuesta_esperada, es_satisfactoria):
    """
    Test para validar que el funcionamiento del middleware 'TrustedHost'
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/credenciales",
            headers={"Origin": "http://localhost:5178", "Host": host},
        )
        TXT = RES.text

    assert RES.status_code == respuesta_esperada["status_code"]
    assert es_satisfactoria or (TXT == respuesta_esperada["contenido"])


@pytest.mark.parametrize(
    "headers,respuesta_esperada,arroja_error",
    [
        (
            {"Origin": "http://localhost:5178", "Host": "localhost"},
            {"status_code": 200, "credenciales": MOCK_TEST_CREDS},
            False,
        ),
        (
            {"Host": "localhost"},
            {"status_code": 400, "error": MOCK_TEXTOS["es"]["errHeaderOrigin"]},
            True,
        ),
        (
            {"Origin": "http://localhost:5145", "Host": "localhost"},
            {"status_code": 403, "error": MOCK_TEXTOS["es"]["errOrigenNoAutorizado"]},
            True,
        ),
    ],
    ids=["test_9", "test_10", "test_80"],
)
def test_middleware_verificar_origen_autorizado(
    mocker: MockerFixture, headers, respuesta_esperada, arroja_error
):
    """
    Test para validar que el middleware que revisa el header 'Origin' para solo dejar pasar
    peticiones de origenes autorizadas.
    """
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get("/credenciales", headers=headers)
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]
    assert (not arroja_error) or (JSON["error"] == respuesta_esperada["error"])
    assert arroja_error or (JSON == respuesta_esperada["credenciales"])


def test_65(mocker: MockerFixture):
    """
    Test para validar que la función que inicializa Firebase sea llamada
    """
    APP = mocker.MagicMock(spec=App)
    CERT = mocker.MagicMock(spec=Certificate)
    FUNC = mocker.patch("firebase_admin_config.initialize_app", return_value=APP)
    mocker.patch("firebase_admin_config.Certificate", return_value=CERT)
    RES = inicializar_firebase()
    assert RES == APP
    FUNC.assert_called_once_with(CERT)


def test_106(monkeypatch: MonkeyPatch):
    """
    Test para validar que la función cargue correctamente las credenciales desde
    las variables de entorno
    """
    monkeypatch.setenv("CLIENTE_FIREBASE_API_KEY", "test_api_key")
    monkeypatch.setenv("CLIENTE_FIREBASE_AUTH_DOMAIN", "test_auth_domain")
    monkeypatch.setenv("CLIENTE_FIREBASE_PROJECT_ID", "test_project_id")
    monkeypatch.setenv("CLIENTE_FIREBASE_STORAGE_BUCKET", "test_storage_bucket")
    monkeypatch.setenv(
        "CLIENTE_FIREBASE_MESSAGING_SENDER_ID", "test_messaging_sender_id"
    )
    monkeypatch.setenv("CLIENTE_FIREBASE_APP_ID", "test_app_id")
    monkeypatch.setenv("CLIENTE_FIREBASE_MEASUREMENT_ID", "test_measurement_id")
    monkeypatch.setenv("CLIENTE_DRIVE_SCOPES", "https://www.googleapis.com/auth/drive,")
    monkeypatch.setenv("CLIENTE_CAPTCHA", "test_captcha")

    RES = cargar_credenciales_cliente_firebase()
    assert RES == MOCK_TEST_CREDS


def test_107(mocker: MockerFixture):
    mocker.patch("constants.dload", return_value="explicador_mock")
    mocker.patch("constants.jload", return_value=MOCK_TEXTOS)
    mocker.patch(
        "constants.InferenceSession",
        side_effect=lambda path_or_bytes, providers: "modelo_mock",
    )

    RES = inicializar_modelos_ml()
    assert RES["explicador"] == "explicador_mock"
    assert RES["textos"] == MOCK_TEXTOS
    assert RES["modelo"] == "modelo_mock"


def test_manejador_uid_invalido(mocker: MockerFixture):
    """
    Test para validar que el manejador de excepciones 'manejar_uid_invalido' funcione correctamente.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": True}),
    )
    mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value=False)

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )
        JSON = RES.json()

    assert RES.status_code == 400
    assert JSON == {"error": MOCK_TEXTOS["es"]["errUIDInvalido"]}


def test_manejador_usuario_inexistente(mocker: MockerFixture):
    """
    Test para validar que el manejador de excepciones 'manejar_usuario_inexistente' funcione correctamente.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": True}),
    )
    mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value=True)
    mocker.patch(
        "apis.FirebaseAuth.get_user", side_effect=UserNotFoundError("error", "error")
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )
        JSON = RES.json()

    assert RES.status_code == 404
    assert JSON == {"error": MOCK_TEXTOS["es"]["errUsuarioNoEncontrado"]}


def test_manejador_acceso_no_autorizado(mocker: MockerFixture):
    """
    Test para validar que el manejador de excepciones 'manejar_acceso_no_autorizado' funcione correctamente.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": False}),
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )
        JSON = RES.json()

    assert RES.status_code == 403
    assert JSON == {"error": MOCK_TEXTOS["es"]["errAccesoDenegado"]}


def test_manejador_error_interno(mocker: MockerFixture):
    """
    Test para validar que el manejador de excepciones 'manejar_error_interno' funcione correctamente.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    mocker.patch(
        "apis.FirebaseAuth.verify_id_token",
        side_effect=FirebaseError("error", "error"),
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )
        JSON = RES.json()

    assert RES.status_code == 500
    assert JSON == {"error": MOCK_TEXTOS["es"]["errValidarToken"]}
