import pytest
from models.Respuestas import *
from pydantic import ValidationError
from pytest_mock import MockerFixture


def test_64(mocker: MockerFixture):
    """
    Test para validar el modelo de pydantic "Usuario".
    """
    MOCK = mocker.patch(
        "models.Respuestas.convertir_datetime_str", return_value="13/03/2026 12:00 AM"
    )
    INSTANCIA = Usuario(
        correo="correo@correo.com",
        uid="1234",
        nombre="usuario",
        estado=False,
        administrador=False,
        fecha_registro=1,
        ultima_conexion=2,
    )
    assert INSTANCIA.correo == "correo@correo.com"
    assert INSTANCIA.uid == "1234"
    assert INSTANCIA.nombre == "usuario"
    assert INSTANCIA.administrador == False
    assert INSTANCIA.estado == False
    assert INSTANCIA.fecha_registro == "13/03/2026 12:00 AM"
    assert INSTANCIA.ultima_conexion == "13/03/2026 12:00 AM"
    MOCK.assert_has_calls((mocker.call(1), mocker.call(2)))


@pytest.mark.parametrize(
    "datos,arroja_excepcion",
    [
        (
            {
                "prediccion": True,
                "probabilidad": 0.9,
                "lime": [{"campo": "Edad>=60", "contribucion": 29}],
            },
            False,
        ),
        (
            {
                "prediccion": "prueba",
                "probabilidad": 0.9,
                "lime": [{"campo": "Edad>=60", "contribucion": 29}],
            },
            True,
        ),
        (
            {
                "prediccion": True,
                "probabilidad": -0.9,
                "lime": [{"campo": "Edad>=60", "contribucion": 29}],
            },
            True,
        ),
        (
            {
                "prediccion": True,
                "probabilidad": 1.9,
                "lime": [{"campo": "Edad>=60", "contribucion": 29}],
            },
            True,
        ),
    ],
    ids=["test_23", "test_24", "test_25", "test_28"],
)
def test_instancia_diagnosticada(datos, arroja_excepcion):
    if arroja_excepcion:
        with pytest.raises(ValidationError):
            InstanciaDiagnosticada(**datos)
    else:
        RES = InstanciaDiagnosticada(**datos)
        assert RES.prediccion == datos["prediccion"]
        assert RES.probabilidad == datos["probabilidad"]
        assert RES.lime == datos["lime"]
