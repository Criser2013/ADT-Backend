from app.utils.Preprocesamiento import *
from numpy import array, float32

def test_83():
    """
    Validar que la función retorne correctamente el número de intervalo 
    al que pertenece un valor cuando este se encuentra acotado en ambos lados
    """
    assert evaluar_intervalo(37, [[30, 50, 1], [60, 70, 2], [70, 100, 3]]) == 1

def test_84():
    """
    Validar que la función retorne correctamente el número de intervalo al
    que pertenece un valor cuando este solo está acotado a su derecha
    """
    assert evaluar_intervalo(12, [[None, 15, 3], [15, 20, 2], [21, None, 1]]) == 3

def test_85():
    """
    Validar que la función retorne correctamente el número de intervalo al
    que pertenece un valor cuando este solo está acotado a su izquierda
    """
    assert evaluar_intervalo(20, [[19, None, 4], [10, 19, 1]]) == 4

def test_86():
    """
    Validar que la función preprocesar_instancias retorne la instancia correctamente
    """
    ARRAY = array([30, 0, 0, 0, 0, 1, 0, 0, 0,
        1, 1, 0, 0, 0, 1, 22, 95, 85,
        120, 80, 0, 0, 0, 0, 8000, 14, 300000,
        1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1])
    RES = array([[ 1,  0,  0,  0,  0,  1,  0,  0,  0,  1,  1,  0,  0,
         0,  1,  2, 10,  2,  4,  5,  0,  0,  0,  0,  2,  5,
         4,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  1]], dtype=float32)
    
    assert (preprocesar_instancias(array([ARRAY], dtype=float32)) == RES).all()