from app.utils.Diccionario import ver_si_existe_clave

def test_37():
    """
    Test para validar que las función "ver_si_existe_clave" retorne True si la clave existe en el diccionario.
    """
    DICT = {"clave1": 1, "clave2": 2, "clave3": 3}
    assert ver_si_existe_clave(DICT, "clave1") == True

def test_38():
    """
    Test para validar que las función "ver_si_existe_clave" retorne False si la clave no existe en el diccionario.
    """
    DICT = {"clave1": 1, "clave2": 2, "clave3": 3}
    assert ver_si_existe_clave(DICT, "clave4") == False