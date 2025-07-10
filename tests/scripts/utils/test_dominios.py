from app.utils.Dominios import obtener_lista_dominios

def test_1():
    """
        Test para validar que la función retorne la lista de dominios correctamente.
    """
    DOMINIOS = "dominio1.com, dominio2.com, dominio3.com"
    RES = obtener_lista_dominios(DOMINIOS)
    assert RES == ["dominio1.com", "dominio2.com", "dominio3.com"]

def test_2():
    """
        Test para validar que la función retorne una lista vacía cuando no hay dominios.
    """
    RES = obtener_lista_dominios("")
    assert RES == []