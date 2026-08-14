import pytest
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from main import app
from models.Respuestas import InstanciaDiagnosticada
from pytest_mock import MockerFixture

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
    "es": {
        "errGenerarDiagnostico": "Error al generar el diagnóstico",
        "errCaptchaTokenInvalido": "El token ha expirado o ya fue utilizado.",
    }
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    yield {
        "explicador": None,
        "textos": TEXTOS,
        "modelo": None,
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": TEST_CREDS,
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
    mocker.patch("main.ORIGENES_AUTORIZADOS", ["*"])
    yield
    mocker.resetall()


@pytest.mark.parametrize(
    "respuesta_esperada,arroja_excepcion",
    [
        (
            {
                "status_code": 200,
                "prediccion": False,
                "probabilidad": 0,
                "tam_lime": 10,
            },
            False,
        ),
        ({"status_code": 500, "error": TEXTOS["es"]["errGenerarDiagnostico"]}, True),
    ],
    ids=["test_16", "test_17"],
)
def test_endpoint_diagnosticar(
    mocker: MockerFixture, respuesta_esperada, arroja_excepcion
):
    """
    Test para validar que eel endpoint '/diagnosticar' cuando una petición se procesa exitosamente o si ocurre
    un error.
    """
    INSTANCIA = {
        "edad": 68, "sexo": 1, "bebedor": 0, "fumador": 0, "proc_quirurgico_traumatismo": 0,
        "inmovilidad_de_m_inferiores": 0, "viaje_prolongado": 0, "TEP_TVP_previo": 0,
        "malignidad": 1, "disnea": 0, "dolor_toracico": 1, "tos": 0, "hemoptisis": 0,
        "sintomas_disautonomicos": 0, "edema_de_m_inferiores": 1, "frecuencia_respiratoria": 18,
        "saturacion_de_la_sangre": 91, "frecuencia_cardiaca": 112, "presion_sistolica": 110,
        "presion_diastolica": 70, "fiebre": 0, "crepitaciones": 0, "sibilancias": 0,
        "soplos": 0, "wbc": 6800, "hb": 13, "plt": 313400, "derrame": 0, "otra_enfermedad": 1,
        "hematologica": 1, "cardiaca": 0, "enfermedad_coronaria": 0, "diabetes_mellitus": 0,
        "endocrina": 1, "gastrointestinal": 1, "hepatopatia_cronica": 0, "hipertension_arterial": 1,
        "neurologica": 0, "pulmonar": 0, "renal": 0, "trombofilia": 0, "urologica": 0, "vascular": 0,
        "vih": 0,
    }

    app.router.lifespan_context = mock_inicializar_modelos
    VALIDADOR = mocker.patch("apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE = mocker.patch("apis.FirebaseAuth.verify_id_token", return_value=1)
    DIAGNOSTICO = mocker.patch("models.Diagnostico.Diagnostico.generar_diagnostico")
    DIAGNOSTICO.side_effect = (
        Exception("Error al generar el diagnóstico") if arroja_excepcion else None
    )
    DIAGNOSTICO.return_value = (
        None
        if arroja_excepcion
        else InstanciaDiagnosticada(
            prediccion=respuesta_esperada["prediccion"],
            probabilidad=respuesta_esperada["probabilidad"],
            lime=[{"campo": "Edad>=60", "contribucion": 10} for _ in range(10)],
        )
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/diagnosticar",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
            json=INSTANCIA,
        )
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]

    if arroja_excepcion:
        assert JSON["error"] == respuesta_esperada["error"]
    else:
        assert JSON["prediccion"] == respuesta_esperada["prediccion"]
        assert JSON["probabilidad"] == respuesta_esperada["probabilidad"]
        assert len(JSON["lime"]) == 10

    VALIDADOR.assert_called_once_with("token_valido")
    FIREBASE.assert_called_once_with(
        "token_valido", MOCK_FIREBASE_APP, check_revoked=True
    )
    DIAGNOSTICO.assert_called_once()


@pytest.mark.parametrize(
    "respuesta_esperada,mock_verificacion_token",
    [
        (
            {"status_code": 200, "success": True, "hostname": "0.0.0.0"},
            {"success": True, "hostname": "0.0.0.0"},
        ),
        (
            {
                "status_code": 401,
                "success": False,
                "hostname": "0.0.0.0",
                "error-codes": [TEXTOS["es"]["errCaptchaTokenInvalido"]],
            },
            {
                "success": False,
                "hostname": "0.0.0.0",
                "error-codes": [TEXTOS["es"]["errCaptchaTokenInvalido"]],
            },
        ),
    ],
    ids=["test_73", "test_74"],
)
def test_endpoint_recaptcha(
    mocker: MockerFixture, respuesta_esperada, mock_verificacion_token
):
    """
    Test para validar el endpoint de recaptcha retorne la respuesta correspondiente a
    la verificación de un token.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    FUNC = mocker.patch(
        "routers.main_router.verificar_peticion_recaptcha",
        return_value=mock_verificacion_token,
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            "/recaptcha",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
            json={"token": "token_valido" * 80},
        )
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]
    assert JSON["success"] == respuesta_esperada["success"]
    assert JSON["hostname"] == respuesta_esperada["hostname"]
    assert JSON["success"] or (JSON["error-codes"] == respuesta_esperada["error-codes"])

    FUNC.assert_called_once_with("token_valido" * 80, "es", TEXTOS)


def test_33():
    """
    Test para validar que el endpoint de healthcheck retorne la respuesta correcta.
    """
    app.router.lifespan_context = mock_inicializar_modelos
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/healthcheck",
            headers={"Origin": "http://localhost:5178", "Host": "localhost"},
        )
        assert RES.status_code == 200
        assert RES.json() == {"status": "ok"}


def test_34(mocker: MockerFixture):
    """
    Test para validar que el endpoint de registro de usuarios funcione correctamente
    """
    UID = "uid"
    app.router.lifespan_context = mock_inicializar_modelos
    mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value=True)
    FIREBASE = mocker.patch(
        "routers.main_router.registrar_usuario_firebase", return_value=1
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            f"/registrar",
            headers={"Origin": "http://localhost:5178", "Host": "localhost"},
            params={"uid": UID},
        )
        assert RES.status_code == 200
        assert RES.json() == {"resultado": "ok"}

    FIREBASE.assert_called_once_with(MOCK_FIREBASE_APP, UID, TEXTOS, "es")
