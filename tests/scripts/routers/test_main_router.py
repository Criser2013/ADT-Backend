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

def test_18(mocker: MockerFixture):
    """
    Test para validar que el API haga correctamente un diagnóstico de TEP
    """

    INSTANCIA = {
        "edad": 4,
        "sexo": 1,
        "bebedor": 0,
        "fumador": 0,
        "cirugia_reciente": 0,
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
        "frecuencia_respiratoria": 1,
        "saturacion_de_la_sangre": 9,
        "frecuencia_cardiaca": 4,
        "presion_sistolica": 4,
        "presion_diastolica": 4,
        "fiebre": 0,
        "crepitaciones": 0,
        "sibilancias": 0,
        "soplos": 0,
        "wbc": 2,
        "hb": 4,
        "plt": 4,
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

    VALIDADOR = mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value=1)

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.post(
        "/diagnosticar",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"},
        json=INSTANCIA
    )

    assert RES.status_code == 200
    assert RES.json() == { "prediccion": True, "probabilidad": 1.0 }

    VALIDADOR.assert_called_once_with("token_valido")
    FIREBASE.assert_called_once_with("token_valido", {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }, check_revoked=True)

def test_19(mocker: MockerFixture):
    """
    Test para validar que el API maneje correctamente un error al realizar
    un diagnóstico
    """

    INSTANCIA = {
        "edad": 4,
        "sexo": 1,
        "bebedor": 0,
        "fumador": 0,
        "cirugia_reciente": 0,
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
        "frecuencia_respiratoria": 1,
        "saturacion_de_la_sangre": 9,
        "frecuencia_cardiaca": 4,
        "presion_sistolica": 4,
        "presion_diastolica": 4,
        "fiebre": 0,
        "crepitaciones": 0,
        "sibilancias": 0,
        "soplos": 0,
        "wbc": 2,
        "hb": 4,
        "plt": 4,
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

    VALIDADOR = mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value=1)
    DIAGNOSTICO = mocker.patch("models.Diagnostico.Diagnostico.generar_diagnostico")

    DIAGNOSTICO.side_effect = Exception("Error al generar el diagnóstico")

    CLIENTE = TestClient(app.main.app)

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