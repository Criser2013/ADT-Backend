import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from app.firebase_admin_config import inicializar_firebase
from firebase_admin import App
from firebase_admin.credentials import Certificate
from app.main import app
from contextlib import asynccontextmanager
from app.constants import cargar_credenciales_cliente_firebase, inicializar_modelos_ml

# Constantes de prueba
TEST_CREDS = {
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
    "es": {"errTry": "Error de prueba:"},
    "en": {"errTry": "Test error:"},
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    yield {
        "explicador": None,  # Mock del explicador
        "textos": MOCK_TEXTOS,
        "modelo": None,  # Mock del modelo
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": TEST_CREDS,
    }


@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    mocker.patch("app.main.CORS_ORIGINS", ["http://localhost:5178",])
    mocker.patch("app.main.ALLOWED_HOSTS", ["localhost",])
    mocker.patch("app.main.ORIGENES_AUTORIZADOS", ["*"])
    yield
    mocker.resetall()

def test_8():
    """
    Test para validar que el API rechace las peticiones de hosts no autorizados
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/credenciales",
            headers={"Origin": "http://localhost:5178", "Host": "google"},
        )

    assert RES.status_code == 400
    assert RES.content.decode() == "Invalid host header"

def test_9(mocker: MockerFixture):
    """
    Test para validar que el middleware que revisa las credenciales de Firebase
    deje pasar un token válido con una petición POST proveniente de un host autorizado
    """
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/credenciales",
            headers={
                "Authorization": "Bearer token_valido",
                "Origin": "http://localhost:5178",
                "Host": "localhost"
            },
        )

    assert RES.status_code == 405
    assert RES.json() == { "detail": "Method Not Allowed" }

@pytest.mark.asyncio
async def test_10(mocker: MockerFixture):
    """
    Test para validar que el API retorne correctamente las credenciales de Firebase
    y no aplique el middleware de verificación de credenciales
    cuando se hace una petición GET a la ruta /credenciales
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        VALIDADOR = mocker.patch("apis.FirebaseAuth.verificar_token")

        RES = CLIENTE.get(
                    "/credenciales",
                    headers={"Origin": "http://localhost:5178", "Host": "localhost"},
                )

    assert RES.status_code == 200
    assert RES.json() == TEST_CREDS

    VALIDADOR.assert_not_called()

def test_80():
    """
    Test para validar que el middleware retorne el mensaje adecuado cuando no se ha colocado
    el header 'origin'
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/credenciales"
        )

    assert RES.status_code == 400
    assert RES.content.decode() == "Encabezado 'origin' inválido"

def test_81(mocker: MockerFixture):
    """
    Test para validar que el middleware rechace la petición cuando viene de un origen no
    autorizado
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch("app.main.ORIGENES_AUTORIZADOS", ["https://dominio.subdominio1.*.com"])

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/credenciales",
            headers={ "origin": "https://dominio.subdominio2.hola.com"}
        )

    assert RES.status_code == 403
    assert RES.content.decode() == "Origen no autorizado"

def test_82(mocker: MockerFixture):
    """
    Test para validar que el middleware acepte una petición de un origen autorizado
    """
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch("app.main.ORIGENES_AUTORIZADOS", ["https://dominio.subdominio1.*.com"])

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/credenciales",
            headers={ "origin": "https://dominio.subdominio1.hola.com", "Host": "localhost"}
        )

    assert RES.status_code == 200
    assert RES.json() == TEST_CREDS

def test_65(mocker: MockerFixture):
    """
    Test para validar que la función que inicializa Firebase sea llamada
    """
    APP = mocker.MagicMock(spec=App)
    CERT = mocker.MagicMock(spec=Certificate)

    FUNC = mocker.patch("app.firebase_admin_config.initialize_app", return_value=APP)
    mocker.patch("app.firebase_admin_config.Certificate", return_value=CERT)
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
    monkeypatch.setenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID", "test_messaging_sender_id")
    monkeypatch.setenv("CLIENTE_FIREBASE_APP_ID", "test_app_id")
    monkeypatch.setenv("CLIENTE_FIREBASE_MEASUREMENT_ID", "test_measurement_id")
    monkeypatch.setenv("CLIENTE_DRIVE_SCOPES", "https://www.googleapis.com/auth/drive,")
    monkeypatch.setenv("CLIENTE_CAPTCHA", "test_captcha")

    RES = cargar_credenciales_cliente_firebase()

    assert RES == TEST_CREDS

def test_107(mocker: MockerFixture):

    def mock_sesion(x, providers):
        return "modelo_mock"

    mocker.mock_open(read_data="datos")
    mocker.patch("app.constants.dload", return_value="explicador_mock")
    mocker.patch("app.constants.jload", return_value=MOCK_TEXTOS)
    mocker.patch("app.constants.InferenceSession", side_effect=mock_sesion)

    RES = inicializar_modelos_ml()

    assert RES["explicador"] == "explicador_mock"
    assert RES["textos"] == MOCK_TEXTOS
    assert RES["modelo"] == "modelo_mock"
