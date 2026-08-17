import pytest
from fastapi.testclient import TestClient
from main import app
from models.Excepciones import AccesoNoAutorizado
from models.Respuestas import InstanciaDiagnosticada
from pytest_mock import MockerFixture
from tests.scripts.conftest import MOCK_FIREBASE_APP, MOCK_TEXTOS


@pytest.mark.parametrize(
    "respuesta_esperada,peticion_autorizada,arroja_excepcion",
    [
        (
            {
                "status_code": 200,
                "prediccion": False,
                "probabilidad": 0,
                "tam_lime": 10,
            },
            True,
            False
        ),
        ({"status_code": 500, "error": MOCK_TEXTOS["es"]["errGenerarDiagnostico"]}, True, True),
        ({"status_code": 403, "error": MOCK_TEXTOS["es"]["errTokenExpirado"]}, False, False)
    ],
    ids=["test_16", "test_17", "test_no_asignado"],
)
def test_endpoint_diagnosticar(
    lifespan_mock, mocker: MockerFixture, respuesta_esperada, peticion_autorizada, arroja_excepcion
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

    FIREBASE = mocker.patch("dependencies.general_dependencies.verificar_token")

    if peticion_autorizada:
        FIREBASE.return_value = {"uid": "a1234H", "admin": False}
    else:
        FIREBASE.side_effect = AccesoNoAutorizado(MOCK_TEXTOS["es"]["errTokenExpirado"])

    DIAGNOSTICO = mocker.patch("models.Diagnostico.Diagnostico.generar_diagnostico")
    DIAGNOSTICO.side_effect = (
        Exception("Error al generar el diagnóstico") if arroja_excepcion else None
    )
    DIAGNOSTICO.return_value = (
        None
        if arroja_excepcion or (not peticion_autorizada)
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

    if arroja_excepcion or (not peticion_autorizada):
        assert JSON["error"] == respuesta_esperada["error"]
    else:
        assert JSON["prediccion"] == respuesta_esperada["prediccion"]
        assert JSON["probabilidad"] == respuesta_esperada["probabilidad"]
        assert len(JSON["lime"]) == 10

    FIREBASE.assert_called_once_with(
        MOCK_FIREBASE_APP, "Bearer token_valido", MOCK_TEXTOS, "es"
    )

    if peticion_autorizada:
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
                "error-codes": [MOCK_TEXTOS["es"]["errCaptchaTokenInvalido"]],
            },
            {
                "success": False,
                "hostname": "0.0.0.0",
                "error-codes": [MOCK_TEXTOS["es"]["errCaptchaTokenInvalido"]],
            },
        ),
    ],
    ids=["test_73", "test_74"],
)
def test_endpoint_recaptcha(
    lifespan_mock, mocker: MockerFixture, respuesta_esperada, mock_verificacion_token
):
    """
    Test para validar el endpoint de recaptcha retorne la respuesta correspondiente a
    la verificación de un token.
    """
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

    FUNC.assert_called_once_with("token_valido" * 80, "es", MOCK_TEXTOS)


def test_33(lifespan_mock):
    """
    Test para validar que el endpoint de healthcheck retorne la respuesta correcta.
    """
    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/healthcheck",
            headers={"Origin": "http://localhost:5178", "Host": "localhost"},
        )
        assert RES.status_code == 200
        assert RES.json() == {"status": "ok"}


@pytest.mark.parametrize("respuesta_esperada,peticion_autorizada",[
    ({"status_code": 200, "resultado": "ok"}, True),
    ({"status_code": 403, "error": MOCK_TEXTOS["es"]["errTokenExpirado"]}, False)
], ids=["test_34","test_no_asignado"])
def test_endpoint_registrar(lifespan_mock, mocker: MockerFixture, respuesta_esperada, peticion_autorizada):
    """
    Test para validar que el endpoint de registro de usuarios funcione correctamente
    """
    UID = "uid"
    TOKEN = mocker.patch("dependencies.general_dependencies.verificar_token")
    FIREBASE = mocker.patch(
            "routers.main_router.registrar_usuario_firebase", return_value=1
        )
    mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value=True)

    if peticion_autorizada:
        TOKEN.return_value = {"uid": "a1234H", "admin": False}
    else:
        TOKEN.side_effect = AccesoNoAutorizado(MOCK_TEXTOS["es"]["errTokenExpirado"])

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.post(
            f"/registrar",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
            params={"uid": UID},
        )
        JSON = RES.json()
        CLAVE = "resultado" if peticion_autorizada else "error"
        assert RES.status_code == respuesta_esperada["status_code"]
        assert JSON[CLAVE] == respuesta_esperada[CLAVE]

    if peticion_autorizada:
        FIREBASE.assert_called_once_with(MOCK_FIREBASE_APP, UID, MOCK_TEXTOS, "es")

    TOKEN.assert_called_once_with(MOCK_FIREBASE_APP, "Bearer token_valido", MOCK_TEXTOS, "es")