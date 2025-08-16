from app.models.Diagnostico import Diagnostico
from numpy import array, float32

def test_7():
    """
    Test para validar que la clase cargue el modelo y genere un diagnóstico
    correctamente.
    """
    INSTANCIA =array([[
        4,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,9,4,4,4,0,0,0,0,2,4,4,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ],]).astype(float32).reshape(1, -1)
    OBJ = Diagnostico(INSTANCIA)
    RES = OBJ.generar_diagnostico()

    assert RES["prediccion"] == True
    assert round(RES["probabilidad"],0) == 1.0
