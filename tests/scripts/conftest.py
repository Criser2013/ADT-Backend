import pytest
from contextlib import asynccontextmanager
from pytest_mock import MockerFixture
from main import app

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
        "errTokenInvalido": "Token inválido",
        "errTokenExpirado": "El token proveído ya ha expirado",
        "errObtenerDatosUsuarios": "Error al obtener los datos de los usuarios",
        "errObtenerUsuario": "Error al obtener el usuario",
        "errActualizarUsuario": "Error al actualizar los datos del usuario.",                "errAsignarRol": "Error al registrar el usuario, reintente nuevamente.",
        "errCaptchaTokenErroneo": "El token proveído tiene errores.",
        "errCaptchaTokenInvalido": "El token ha expirado o ya fue utilizado.",
        "errGenerarDiagnostico": "Error al generar el diagnóstico",
    }
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    yield {
        "explicador": None,
        "textos": MOCK_TEXTOS,
        "modelo": None,
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": MOCK_TEST_CREDS,
    }

@pytest.fixture
def lifespan_mock(mocker: MockerFixture):
    mocker.patch.object(
        app.router,
        "lifespan_context",
        mock_inicializar_modelos,
    )

import pytest
from pytest_mock import MockerFixture

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
    mocker.patch("apis.FirebaseAuth.COD_EXITO", 1)
    mocker.patch("apis.Recaptcha.RECAPTCHA_SECRET", "secret_token")
    mocker.patch("apis.Recaptcha.RECAPTCHA_API_URL", "url")
    yield
    mocker.resetall()