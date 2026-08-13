import pytest
from app.utils.Diccionario import ver_si_existe_clave

DICCIONARIO = {"clave1": 1, "clave2": 2, "clave3": 3}

@pytest.mark.parametrize("diccionario,clave,respuesta_esperada",[
    (DICCIONARIO, "clave1", True),
    (DICCIONARIO, "clave4", False)
], ids=["test_35", "test_36"])
def test_ver_si_existe_clave(diccionario, clave, respuesta_esperada):
    """
    Test para validar que las función "ver_si_existe_clave" retorne True si la clave existe en el diccionario.
    """
    assert ver_si_existe_clave(diccionario, clave) == respuesta_esperada