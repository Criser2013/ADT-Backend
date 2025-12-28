from app.models.Diagnostico import Diagnostico
from onnxruntime import InferenceSession
from numpy import array, float32
from pathlib import Path
import pytest

@pytest.mark.asyncio
async def test_7():
    """
    Test para validar que la clase cargue el modelo y genere un diagnóstico
    correctamente.
    """
    INSTANCIA = {
            "Inmovilidad_de_M_inferiores": [0], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [0],
            "Viaje_prolongado": [0], "Síntomas_disautonomicos": [0], "Edema_de_M_inferiores": [1],
            "Diabetes_Mellitus": [0], "Hipertensión_arterial": [1], "Enfermedad_coronaria": [0],
            "Dolor_toracico": [1], "TEP___TVP_Previo": [0], "Frecuencia_respiratoria": [18],
            "Presión_sistólica": [110], "Presión_diastólica": [70], "Saturación_de_la_sangre": [91], "Frecuencia_cardíaca": [112],
            "WBC": [6800], "HB": [13], "PLT": [313400], "Género": [1], "Edad": [68], "Fumador": [0], "Bebedor": [0], "Malignidad": [1],
            "Disnea": [0], "Tos": [0], "Hemoptisis": [0], "Fiebre": [0], "Crepitaciones": [0], "Sibilancias": [0],
            "Soplos": [0], "Derrame": [0], "Trombofilia": [0], "VIH": [0], "Otra_Enfermedad": [1],
            "Hepatopatía_crónica": [0], "Renal": [0], "Cardíaca": [0], "Neurológica": [0], "Pulmonar": [0], "Endocrina": [0],
            "Gastrointestinal": [0], "Hematologica": [0], "Urológica": [0], "Vascular": [0],
        }
    OBJ = Diagnostico(INSTANCIA)
    RES = await OBJ.generar_diagnostico()

    assert RES["prediccion"] == True
    assert round(RES["probabilidad"],0) == 1.0

def test_87():
    """
    Test para validar que la función genere correctamente las probabilidades
    de pertenencia a una clase cuando se requiere clasificar varias instancias
    """
    INSTANCIA = array([68, 1, 0, 0, 0, 0, 0, 0, 1,
            0, 1, 0, 0, 0, 1, 18, 91, 112, 110,
            70, 0, 0, 0, 0, 6800, 13, 313400, 0,
            1, 1, 0, 0, 0, 1, 1, 0, 1,
            0, 0, 0, 0, 0, 0, 0], dtype=float32)
    INSTANCIA1 = array(
        [60, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1,
         0, 19, 90, 128, 129, 93, 0, 0, 0, 0, 12300,
         13.8, 211100, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0], dtype=float32)

    OBJ = Diagnostico(INSTANCIA)
    sesion = InferenceSession(
            f"{Path(__file__).resolve().parent.parent.parent.parent}/app/bin/modelo_red_neuronal.onnx",
            providers=["CPUExecutionProvider"],
        )
    RES = OBJ.obtener_probabilidades_predicciones(array([INSTANCIA, INSTANCIA1]).reshape(2, -1), sesion)

    assert round(RES[0][1], 0) == 0
    assert round(RES[1][1], 0) == 1

def test_88():
    """
    Test para validar que la función genere correctamente las explicaciones
    de las predicciones.
    """
    INSTANCIA = {
            "Inmovilidad_de_M_inferiores": [1], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [0],
            "Viaje_prolongado": [0], "Síntomas_disautonomicos": [0], "Edema_de_M_inferiores": [1],
            "Diabetes_Mellitus": [0], "Hipertensión_arterial": [0], "Enfermedad_coronaria": [0],
            "Dolor_toracico": [1], "TEP___TVP_Previo": [0], "Frecuencia_respiratoria": [22],
            "Presión_sistólica": [120], "Presión_diastólica": [80], "Saturación_de_la_sangre": [95], "Frecuencia_cardíaca": [85],
            "WBC": [8000], "HB": [14], "PLT": [300000], "Género": [0], "Edad": [30], "Fumador": [0], "Bebedor": [0], "Malignidad": [0],
            "Disnea": [1], "Tos": [0], "Hemoptisis": [0], "Fiebre": [0], "Crepitaciones": [0], "Sibilancias": [0],
            "Soplos": [0], "Derrame": [1], "Trombofilia": [0], "VIH": [1], "Otra_Enfermedad": [1],
            "Hepatopatía_crónica": [0], "Renal": [0], "Cardíaca": [0], "Neurológica": [0], "Pulmonar": [0], "Endocrina": [0],
            "Gastrointestinal": [0], "Hematologica": [0], "Urológica": [0], "Vascular": [0],
        }
    OBJ = Diagnostico(INSTANCIA)
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