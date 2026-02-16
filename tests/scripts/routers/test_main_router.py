from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from app.main import app
import pytest
from contextlib import asynccontextmanager
from dill import load as dload
from json import load as jload
from onnxruntime import InferenceSession
from pathlib import Path

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
    "reCAPTCHA": "test_recaptcha",
}

MOCK_FIREBASE_APP = {
    "appId": "test_app_id",
    "cred": {"projectId": "test_project_id", "certificated": True},
}

TEXTOS = {
    "es": { "errTry": "Error al procesar la solicitud:"},
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    PATH_BASE = Path(__file__).resolve().parent.parent.parent.parent
    with open(f"{PATH_BASE}/app/bin/explicador.pkl", "rb") as archivo:
        EXPLAINER = dload(archivo)

    MODELO = InferenceSession(
        f"{PATH_BASE}/app/bin/modelo_red_neuronal.onnx",
        providers=["CPUExecutionProvider"],
    )
    yield {
        "explicador": EXPLAINER,
        "textos": TEXTOS,
        "modelo": MODELO,
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": TEST_CREDS,
    }

@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    mocker.patch("app.main.CORS_ORIGINS", ["http://localhost:5178",])
    mocker.patch("app.main.ALLOWED_HOSTS", ["localhost",], )
    mocker.patch("app.main.ORIGENES_AUTORIZADOS", ["*"])
    yield
    mocker.resetall()

def test_16(mocker: MockerFixture):
    """
    Test para validar que el API haga correctamente un diagnóstico de TEP
    """

    INSTANCIA = {
        "edad": 68,
        "sexo": 1,
        "bebedor": 0,
        "fumador": 0,
        "proc_quirurgico_traumatismo": 0,
        "inmovilidad_de_m_inferiores": 0,
        "viaje_prolongado": 0,
        "TEP_TVP_previo": 0,
        "malignidad": 1,
        "disnea": 0,
        "dolor_toracico": 1,
        "tos": 0,
        "hemoptisis": 0,
        "sintomas_disautonomicos": 0,
        "edema_de_m_inferiores": 1,
        "frecuencia_respiratoria": 18,
        "saturacion_de_la_sangre": 91,
        "frecuencia_cardiaca": 112,
        "presion_sistolica": 110,
        "presion_diastolica": 70,
        "fiebre": 0,
        "crepitaciones": 0,
        "sibilancias": 0,
        "soplos": 0,
        "wbc": 6800,
        "hb": 13,
        "plt": 313400,
        "derrame": 0,
        "otra_enfermedad": 1,
        "hematologica": 1,
        "cardiaca": 0,
        "enfermedad_coronaria": 0,
        "diabetes_mellitus": 0,
        "endocrina": 1,
        "gastrointestinal": 1,
        "hepatopatia_cronica": 0,
        "hipertension_arterial": 1,
        "neurologica": 0,
        "pulmonar": 0,
        "renal": 0,
        "trombofilia": 0,
        "urologica": 0,
        "vascular": 0,
        "vih": 0,
    }

    app.router.lifespan_context = mock_inicializar_modelos

    VALIDADOR = mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value=1)

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/diagnosticar",
            headers={"Origin": "http://localhost:5178", "Host": "localhost",
                     "Authorization": "Bearer token_valido"},
            json=INSTANCIA
        )
    JSON = RES.json()

    assert RES.status_code == 200
    assert JSON["prediccion"] == False
    assert round(JSON["probabilidad"],0) == 1.0
    assert len(JSON["lime"]) == 10

    VALIDADOR.assert_called_once_with("token_valido")
    FIREBASE.assert_called_once_with("token_valido", {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }, check_revoked=True)

def test_17(mocker: MockerFixture):
    """
    Test para validar que el API maneje correctamente un error al realizar
    un diagnóstico
    """

    INSTANCIA = {
        "edad": 68,
        "sexo": 1,
        "bebedor": 0,
        "fumador": 0,
        "proc_quirurgico_traumatismo": 0,
        "inmovilidad_de_m_inferiores": 0,
        "viaje_prolongado": 0,
        "TEP_TVP_previo": 0,
        "malignidad": 1,
        "disnea": 0,
        "dolor_toracico": 1,
        "tos": 0,
        "hemoptisis": 0,
        "sintomas_disautonomicos": 0,
        "edema_de_m_inferiores": 1,
        "frecuencia_respiratoria": 18,
        "saturacion_de_la_sangre": 91,
        "frecuencia_cardiaca": 112,
        "presion_sistolica": 110,
        "presion_diastolica": 70,
        "fiebre": 0,
        "crepitaciones": 0,
        "sibilancias": 0,
        "soplos": 0,
        "wbc": 6800,
        "hb": 13,
        "plt": 313400,
        "derrame": 0,
        "otra_enfermedad": 1,
        "hematologica": 1,
        "cardiaca": 0,
        "enfermedad_coronaria": 0,
        "diabetes_mellitus": 0,
        "endocrina": 1,
        "gastrointestinal": 1,
        "hepatopatia_cronica": 0,
        "hipertension_arterial": 1,
        "neurologica": 0,
        "pulmonar": 0,
        "renal": 0,
        "trombofilia": 0,
        "urologica": 0,
        "vascular": 0,
        "vih": 0,
    }

    app.router.lifespan_context = mock_inicializar_modelos
    VALIDADOR = mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value=1)
    DIAGNOSTICO = mocker.patch("models.Diagnostico.Diagnostico.generar_diagnostico")

    DIAGNOSTICO.side_effect = Exception("Error al generar el diagnóstico")

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
                "/diagnosticar",
                headers={"Origin": "http://localhost:5178", "Host": "localhost",
                        "Authorization": "Bearer token_valido"},
                json=INSTANCIA
            )

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error al generar el diagnóstico"}

    VALIDADOR.assert_called_once_with("token_valido")
    FIREBASE.assert_called_once_with("token_valido", {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }, check_revoked=True)
    DIAGNOSTICO.assert_called_once()

def test_73(mocker: MockerFixture):
    """
    Test para validar el endpoint de recaptcha retorne la respuesta correspondiente a
    la verificación de un token.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    FUNC = mocker.patch("routers.main_router.verificar_peticion_recaptcha", return_value={"success": True, "hostname": "0.0.0.0"})

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/recaptcha",
            headers={"Origin": "http://localhost:5178", "Host": "localhost",
                    "Authorization": "Bearer token_valido"},
            json={"token": "token_valido"}
        )

    assert RES.status_code == 200
    assert RES.json() == {"success": True, "hostname": "0.0.0.0"}

    FUNC.assert_called_once_with("token_valido", "es", TEXTOS)

def test_74(mocker: MockerFixture):
    """
    Test para validar que el endpoint para verificar el captcha maneje correctamente
    las excepciones.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    FUNC = mocker.patch("routers.main_router.verificar_peticion_recaptcha", side_effect=Exception("Error de verificación"))

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/recaptcha",
            headers={"Origin": "http://localhost:5178", "Host": "localhost",
                    "Authorization": "Bearer token_valido"},
            json={"token": "token_valido"}
        )

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error de verificación"}

    FUNC.assert_called_once_with("token_valido", "es", TEXTOS)

def test_91():
    """
    Test para validar que el endpoint de healthcheck retorne la respuesta correcta.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get("/healthcheck", headers={"Origin": "http://localhost:5178", "Host": "localhost"})

    assert RES.status_code == 200
    assert RES.json() == {"status": "ok"}