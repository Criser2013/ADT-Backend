from app.models.Diagnostico import Diagnostico
from onnxruntime import InferenceSession
from numpy import array, float32
from pathlib import Path

def test_7():
    """
    Test para validar que la clase cargue el modelo y genere un diagnóstico
    correctamente.
    """
    INSTANCIA = array([[
        68,1,0,0,0,0,0,0,1,0,1,0,0,0,1,18,91,112,110,70,0,0,0,0,6800,13,313400,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ],]).astype(float32)
    OBJ = Diagnostico(INSTANCIA)
    RES = OBJ.generar_diagnostico()

    assert RES["prediccion"] == True
    assert round(RES["probabilidad"],0) == 1.0

def test_87():
    """
    Test para validar que la función genere correctamente las probabilidades
    de pertenencia a una clase cuando se requiere clasificar varias instancias
    """
    INSTANCIA = array([30, 0, 0, 0, 0, 1, 0, 0, 0,
        1, 1, 0, 0, 0, 1, 22, 95, 85,
        120, 80, 0, 0, 0, 0, 8000, 14, 300000,
        1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1], dtype=float32)
    OBJ = Diagnostico(INSTANCIA)
    sesion = InferenceSession(
            f"{Path(__file__).resolve().parent.parent.parent.parent}/app/bin/modelo_red_neuronal.onnx",
            providers=["CPUExecutionProvider"],
        )
    RES = OBJ.obtener_probabilidades_predicciones(array([INSTANCIA, INSTANCIA]).reshape(2, -1), sesion)

    assert round(RES[0][1], 0) == 1
    assert round(RES[1][1], 0) == 1

def test_88():
    """
    Test para validar que la función genere correctamente las explicaciones
    de las predicciones.
    """
    INSTANCIA = array([30, 0, 0, 0, 0, 1, 0, 0, 0,
        1, 1, 0, 0, 0, 1, 22, 95, 85,
        120, 80, 0, 0, 0, 0, 8000, 14, 300000,
        1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1], dtype=float32)
    OBJ = Diagnostico(array([INSTANCIA]).reshape(1,-1))
    sesion = InferenceSession(
            f"{Path(__file__).resolve().parent.parent.parent.parent}/app/bin/modelo_red_neuronal.onnx",
            providers=["CPUExecutionProvider"],
        )
    OBJ.generar_explicacion(sesion)

    assert OBJ.explicacion is not None
    assert len(OBJ.explicacion) == 10

    for i in OBJ.explicacion:
        assert "campo" in i.keys()
        assert "contribucion" in i.keys()