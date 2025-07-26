from pytest_mock import MockerFixture
from fastapi import Request
import pytest
from app.apis.FirebaseAuth import *
from firebase_admin.auth import ExpiredIdTokenError, CertificateFetchError, ListUsersPage, ExportedUserRecord, UserMetadata

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
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

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
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

def test_16(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token")
    FIREBASE.side_effect = ExpiredIdTokenError("Token expirado", "EL token está expirado.")

    RES = validar_token("token_invalido", "firebase_app", False)

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

    RES = validar_token("token_invalido", "firebase_app", False)

    assert RES == -1
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)

def test_24(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" retorne los datos del token cuando este
    es válido
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_valido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value={ "email": "usuario@correo.com" })

    RES = validar_token("token_valido", "firebase_app", True)

    assert RES == (1, {"email": "usuario@correo.com"})
    FIREBASE.assert_called_once_with("token_valido", "firebase_app", check_revoked=True)

def test_25(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" retorne los datos del token cuando este
    es válido
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_valido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    TOKEN = mocker.patch("app.apis.FirebaseAuth.validar_token", return_value=(1, {"email": "usuario@correo.com"}))

    RES = ver_datos_token(REQ, "firebase_app")

    assert RES == (1, {"email": "usuario@correo.com"})
    VALIDADOR.assert_called_once_with("token_valido")
    TOKEN.assert_called_once_with("token_valido", "firebase_app", True)

def test_26(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" cuando se provee un token inválido.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=False)
    TOKEN = mocker.patch("apis.FirebaseAuth.validar_token")

    RES = ver_datos_token(REQ, "firebase_app")

    assert RES == (0, {"error": "Token inválido"})
    VALIDADOR.assert_called_once_with("token_invalido")
    TOKEN.assert_not_called()

def test_27(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" maneje correctamente las
    excepciones.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token")
    VALIDADOR.side_effect = Exception("Error inesperado")

    RES = ver_datos_token(REQ, "firebase_app")

    assert RES == (-1, {"error": "Error al procesar el token: Error inesperado."})
    VALIDADOR.assert_called_once_with("token_invalido")

@pytest.mark.asyncio
async def test_28(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" retorne los datos de los usuarios.
    """
    LISTA = mocker.MagicMock(spec=ListUsersPage)
    USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
    METADATOS = mocker.MagicMock(spec=UserMetadata)

    METADATOS.last_sign_in_timestamp = 1753549008090

    USUARIO.email = "usuario@correo.com"
    USUARIO.display_name = "usuario"
    USUARIO.user_metadata =  METADATOS

    LISTA.users = [USUARIO]
    LISTA.has_next_page = False

    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_roles_usuarios")
    FIRESTORE.return_value = { "usuario@correo.com": 0 }

    FIREBASE = mocker.patch("firebase_admin.auth.list_users", return_value=LISTA)

    RES = await ver_datos_usuarios("firebase_app")

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"usuarios":[{"correo":"usuario@correo.com","nombre":"usuario","rol":0,"ultima_conexion":"26/07/2025 11:56 AM"}]}'

    FIREBASE.assert_called_once_with(app="firebase_app")
    FIRESTORE.assert_called_once()

@pytest.mark.asyncio
async def test_29(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" retorne los datos de los usuarios
    cuando hay múltiples páginas de usuarios.
    """
    LISTA = mocker.MagicMock(spec=ListUsersPage)
    LISTA2 = mocker.MagicMock(spec=ListUsersPage)
    USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
    METADATOS = mocker.MagicMock(spec=UserMetadata)

    METADATOS.last_sign_in_timestamp = 1753549008090

    USUARIO.email = "usuario@correo.com"
    USUARIO.display_name = "usuario"
    USUARIO.user_metadata =  METADATOS

    LISTA2.users = [USUARIO]
    LISTA2.has_next_page = False

    LISTA.users = [USUARIO]
    LISTA.has_next_page = True
    LISTA.get_next_page.side_effect = lambda: LISTA2

    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_roles_usuarios")
    FIRESTORE.return_value = { "usuario@correo.com": 0 }

    FIREBASE = mocker.patch("firebase_admin.auth.list_users", return_value=LISTA)

    RES = await ver_datos_usuarios("firebase_app")

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"usuarios":[{"correo":"usuario@correo.com","nombre":"usuario","rol":0,"ultima_conexion":"26/07/2025 11:56 AM"},{"correo":"usuario@correo.com","nombre":"usuario","rol":0,"ultima_conexion":"26/07/2025 11:56 AM"}]}'

    FIREBASE.assert_called_once_with(app="firebase_app")

@pytest.mark.asyncio
async def test_30(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" maneje correctamente las excepciones.
    """
    FIREBASE = mocker.patch("firebase_admin.auth.list_users")
    FIREBASE.side_effect = Exception("Error al obtener los usuarios")

    RES = await ver_datos_usuarios("firebase_app")

    assert RES.status_code == 400
    assert RES.body.decode("utf-8") == '{"error":"Error al obtener los datos de los usuarios: Error al obtener los usuarios"}'

    FIREBASE.assert_called_once_with(app="firebase_app")