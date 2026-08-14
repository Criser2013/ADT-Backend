import pytest
from models.Diagnostico import Diagnostico
from models.Respuestas import InstanciaDiagnosticada
from onnxruntime import InferenceSession
from numpy import array, float32
from pathlib import Path
from dill import load as dload
from pytest_mock import MockerFixture
from onnxruntime import InferenceSession
from pathlib import Path


@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    global EXPLAINER, MODELO, INSTANCIA_PRUEBA

    PATH_BASE = f"{Path(__file__).resolve().parent.parent.parent.parent}/app"
    with open(f"{PATH_BASE}/bin/explicador.pkl", "rb") as archivo:
        EXPLAINER = dload(archivo)

    MODELO = InferenceSession(
        f"{PATH_BASE}/bin/modelo_red_neuronal.onnx",
        providers=["CPUExecutionProvider"],
    )
    INSTANCIA_PRUEBA = {
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
    yield
    del INSTANCIA_PRUEBA
    del MODELO
    del EXPLAINER
    mocker.resetall()

def test_7():
    """
    Test para validar que la clase cargue el modelo y genere un diagnóstico
    correctamente.
    """
    OBJ = Diagnostico(INSTANCIA_PRUEBA.copy(), MODELO, EXPLAINER)
    RES = OBJ.generar_diagnostico()

    assert isinstance(RES, InstanciaDiagnosticada)
    assert RES.prediccion == True
    assert round(RES.probabilidad,0) == 1.0
    assert len(RES.lime) == 10


def test_87():
    """
    Test para validar que la función genere correctamente las probabilidades
    de pertenencia a una clase cuando se requiere clasificar varias instancias
    """
    INSTANCIA = array([
        68, 1, 0, 0, 0, 0, 0, 0, 1,
        0, 1, 0, 0, 0, 1, 18, 91, 112, 110,
        70, 0, 0, 0, 0, 6800, 13, 313400, 0,
        1, 1, 0, 0, 0, 1, 1, 0, 1,
        0, 0, 0, 0, 0, 0, 0
        ], dtype=float32)
    INSTANCIA1 = array(
        [60, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1,
         0, 19, 90, 128, 129, 93, 0, 0, 0, 0, 12300,
         13.8, 211100, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0
        ], dtype=float32)

    OBJ = Diagnostico({}, MODELO, EXPLAINER)
    RES = OBJ.obtener_probabilidades_predicciones(array([INSTANCIA, INSTANCIA1]).reshape(2, -1))

    assert round(RES[0][1], 0) == 0
    assert round(RES[1][1], 0) == 1


def test_88():
    """
    Test para validar que la función genere correctamente las explicaciones
    de las predicciones.
    """
    OBJ = Diagnostico(INSTANCIA_PRUEBA.copy(), MODELO, EXPLAINER)
    OBJ.generar_explicacion()

    assert OBJ.explicacion is not None
    assert len(OBJ.explicacion) == 10

    for i in OBJ.explicacion:
        assert "campo" in i.keys()
        assert "contribucion" in i.keys()

def test_obtener_array_datos():
    """
    Validar que el método 'obtener_array_datos' retorne un arreglo de numpy con los datos de la instancia.
    """
    OBJ = Diagnostico(INSTANCIA_PRUEBA.copy(), MODELO, EXPLAINER)
    RES_ESPERADA = array([
        0,0,0,0,1,0,1,0,1,0,18,110,70,91,112,6800,13,
        313400,1,68,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,
        0,0,0,0,0,0,0
        ], dtype=float32)
    RES = OBJ.obtener_array_datos()
    assert RES.all() == RES_ESPERADA.all()

def test_convertir_a_diccionario():
    """
    Validar que el método 'convertir_a_diccionario' retorne el diccionario correcto según el arreglo de datos.
    """
    OBJ = Diagnostico(INSTANCIA_PRUEBA.copy(), MODELO, EXPLAINER)
    orden = (
                "Edad",
                "Género",
                "Bebedor",
                "Fumador",
                "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias",
                "Inmovilidad_de_M_inferiores",
                "Viaje_prolongado",
                "TEP___TVP_Previo",
                "Malignidad",
                "Disnea",
                "Dolor_toracico",
                "Tos",
                "Hemoptisis",
                "Síntomas_disautonomicos",
                "Edema_de_M_inferiores",
                "Frecuencia_respiratoria",
                "Saturación_de_la_sangre",
                "Frecuencia_cardíaca",
                "Presión_sistólica",
                "Presión_diastólica",
                "Fiebre",
                "Crepitaciones",
                "Sibilancias",
                "Soplos",
                "WBC",
                "HB",
                "PLT",
                "Derrame",
                "Otra_Enfermedad",
                "Hematologica",
                "Cardíaca",
                "Enfermedad_coronaria",
                "Diabetes_Mellitus",
                "Endocrina",
                "Gastrointestinal",
                "Hepatopatía_crónica",
                "Hipertensión_arterial",
                "Neurológica",
                "Pulmonar",
                "Renal",
                "Trombofilia",
                "Urológica",
                "Vascular",
                "VIH",
            )

    valores = [INSTANCIA_PRUEBA[k][0] for k in orden]
    RES = OBJ.convertir_a_diccionario(array([valores], dtype=float32))

    for i in INSTANCIA_PRUEBA.keys():
        assert int(RES[i][0]) == INSTANCIA_PRUEBA[i][0]