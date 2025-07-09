from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
import app.main
import pytest

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
    }

@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    MOCK_APP = {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }
    
    mocker.patch("app.main.firebase_app", MOCK_APP)
    mocker.patch("app.main.CORS_ORIGINS", ["http://localhost:5178",])
    mocker.patch("app.main.ALLOWED_HOSTS", ["localhost",], )
    mocker.patch("app.routers.main_router.CREDS_FIREBASE_CLIENTE", TEST_CREDS)
    yield
    mocker.resetall()

def test_10():
    """
    Test para validar que el API rechace las peticiones de hosts no autorizados
    """

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/credenciales",
        headers={"Origin": "http://localhost:5178", "Host": "google"},
    )

    assert RES.status_code == 400
    assert RES.content.decode() == "Invalid host header"

def test_11(mocker: MockerFixture):
    """
    Test para validar que el middleware que revisa las credenciales de Firebase
    deje pasar un token válido con una petición POST proveniente de un host autorizado
    """

    CLIENTE = TestClient(app.main.app)

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value=1)

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
    
    VALIDADOR.assert_called_once_with("token_valido")
    FIREBASE.assert_called_once_with("token_valido", {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }, check_revoked=True)

def test_12(mocker: MockerFixture):
    """
    Test para validar que el API retorne correctamente las credenciales de Firebase
    y no aplique el middleware de verificación de credenciales
    cuando se hace una petición GET a la ruta /credenciales
    """

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.verificar_token")

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/credenciales",
        headers={"Origin": "http://localhost:5178", "Host": "localhost"},
    )
    # print(RES.content.decode("utf-8"))

    assert RES.status_code == 200
    assert RES.json() == TEST_CREDS

    VALIDADOR.assert_not_called()