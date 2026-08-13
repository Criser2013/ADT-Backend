import pytest
from utils.Dominios import obtener_lista_dominios


@pytest.mark.parametrize(
    "dominios,respuesta_esperada",
    [
        (
            "dominio1.com, dominio2.com, dominio3.com",
            ["dominio1.com", "dominio2.com", "dominio3.com"],
        ),
        ("", []),
    ],
    ids=["test_1", "test_2"],
)
def test_obtener_lista_dominios(dominios, respuesta_esperada):
    """
    Test para validar que la función retorne la lista de dominios correctamente.
    """
    RES = obtener_lista_dominios(dominios)
    assert RES == respuesta_esperada
