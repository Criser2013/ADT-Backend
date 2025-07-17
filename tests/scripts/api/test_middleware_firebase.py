from pytest_mock import MockerFixture
from fastapi import Request
import pytest
from app.apis.FirebaseAuth import verificar_token, validar_token
from firebase_admin.auth import ExpiredIdTokenError, CertificateFetchError

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

@pytest.mark.asyncio
async def test_13(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" retorne un error cuando el token
    es inválido
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=False)

    RES = await verificar_token(REQ, "firebase_app", None)

    assert RES.status_code == 403
    assert RES.body.decode("utf-8") == '{"error":"Token inválido"}'

    VALIDADOR.assert_called_once_with("token_invalido")

@pytest.mark.asyncio
async def test_14(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" retorne un error cuando ocurre
    una excepción al procesar la solicitud
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token", return_value=-1)

    RES = await verificar_token(REQ, "firebase_app", None)

    assert RES.status_code == 400
    assert RES.body.decode("utf-8") == '{"error":"Error al validar el token"}'

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app")

@pytest.mark.asyncio
async def test_15(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" maneje correctamente los
    errores inesperados al validar el token de Firebase.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token")
    FIREBASE_VAL.side_effect = Exception("Excepción imprevista")

    RES = await verificar_token(REQ, "firebase_app", None)

    assert RES.status_code == 500
    assert RES.body.decode("utf-8") == '{"error":"Error al procesar la solicitud: Excepción imprevista"}'

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app")

def test_16(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token")
    FIREBASE.side_effect = ExpiredIdTokenError("Token expirado", "EL token está expirado.")

    RES = validar_token("token_invalido", "firebase_app")

    assert RES == 0
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)

def test_17(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token")
    FIREBASE.side_effect = CertificateFetchError("Error al obtener el certificado", "No se pudo obtener el certificado.")

    RES = validar_token("token_invalido", "firebase_app")

    assert RES == -1
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)