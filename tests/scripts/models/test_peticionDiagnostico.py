from app.models.PeticionDiagnostico import PeticionDiagnostico
from numpy import array
from pydantic import ValidationError
import pytest

def test_5():
    """
    Test para validar que la función parsee correctamente una instancia.
    """
    #
    DATOS = {
        "edad": 68,
        "sexo": 1,
        "bebedor": 0,
        "fumador": 0,
        "proc_quirurgico_traumatismo": 0,
        "inmovilidad_de_m_inferiores": 0,
        "viaje_prolongado": 0,
        "TEP_TVP_previo": 0,
        "malignidad": 1,
        "disnea": 0,
        "dolor_toracico": 1,
        "tos": 0,
        "hemoptisis": 0,
        "sintomas_disautonomicos": 0,
        "edema_de_m_inferiores": 1,
        "frecuencia_respiratoria": 18,
        "saturacion_de_la_sangre": 91,
        "frecuencia_cardiaca": 112,
        "presion_sistolica": 110,
        "presion_diastolica": 70,
        "fiebre": 0,
        "crepitaciones": 0,
        "sibilancias": 0,
        "soplos": 0,
        "wbc": 6800,
        "hb": 13,
        "plt": 313400,
        "derrame": 0,
        "otra_enfermedad": 1,
        "hematologica": 1,
        "cardiaca": 0,
        "enfermedad_coronaria": 0,
        "diabetes_mellitus": 0,
        "endocrina": 1,
        "gastrointestinal": 1,
        "hepatopatia_cronica": 0,
        "hipertension_arterial": 1,
        "neurologica": 0,
        "pulmonar": 0,
        "renal": 0,
        "trombofilia": 0,
        "urologica": 0,
        "vascular": 0,
        "vih": 0,
    }
    OBJ = PeticionDiagnostico(**DATOS)
    RES = OBJ.obtener_diccionario_instancia()
    assert RES == {
            "Inmovilidad_de_M_inferiores": [0], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [0],
            "Viaje_prolongado": [0], "Síntomas_disautonomicos": [0], "Edema_de_M_inferiores": [1],
            "Diabetes_Mellitus": [0], "Hipertensión_arterial": [1], "Enfermedad_coronaria": [0],
            "Dolor_toracico": [1], "TEP___TVP_Previo": [0], "Frecuencia_respiratoria": [18],
            "Presión_sistólica": [110], "Presión_diastólica": [70], "Saturación_de_la_sangre": [91], "Frecuencia_cardíaca": [112],
            "WBC": [6800], "HB": [13], "PLT": [313400], "Género": [1], "Edad": [68], "Fumador": [0], "Bebedor": [0], "Malignidad": [1],
            "Disnea": [0], "Tos": [0], "Hemoptisis": [0], "Fiebre": [0], "Crepitaciones": [0], "Sibilancias": [0],
            "Soplos": [0], "Derrame": [0], "Trombofilia": [0], "VIH": [0], "Otra_Enfermedad": [1], "Hematologica": [1], "Cardíaca": [0],
            "Hepatopatía_crónica": [0], "Renal": [0], "Cardíaca": [0], "Neurológica": [0], "Pulmonar": [0], "Endocrina": [1],
            "Gastrointestinal": [1], "Urológica": [0], "Vascular": [0],
        }

def test_6():
    """
    Test para validar que la función arroje una excepción con una instancia con valores incorrectos.
    """
    with pytest.raises(ValidationError):
        DATOS = {
                "edad": "4",
                "sexo": True,
                "bebedor": "0",
                "fumador": "0",
                "proc_quirurgico_traumatismo": "0",
                "inmovilidad_de_m_inferiores": [],
                "viaje_prolongado": False,
                "TEP_TVP_previo": False,
                "malignidad": "False",
                "disnea": [0,0,0],
                "dolor_toracico": (1,),
                "tos": False,
                "hemoptisis": [False,],
                "sintomas_disautonomicos": ("ola",),
                "edema_de_m_inferiores": True,
                "frecuencia_respiratoria": True,
                "saturacion_de_la_sangre": "9",
                "frecuencia_cardiaca": "4",
                "presion_sistolica": "4",
                "presion_diastolica": "4",
                "fiebre": "0",
                "crepitaciones": "0",
                "sibilancias": "0",
                "soplos": "0",
                "wbc": "2",
                "hb": "4",
                "plt": "4",
                "derrame": "0",
                "otra_enfermedad": "1",
                "hematologica": "1",
                "cardiaca": "0",
                "enfermedad_coronaria": "0",
                "diabetes_mellitus": "0",
                "endocrina": "1",
                "gastrointestinal": "1",
                "hepatopatia_cronica": "0",
                "hipertension_arterial": "1",
                "neurologica": "0",
                "pulmonar": "0",
                "renal": "0",
                "trombofilia": "0",
                "urologica": "0",
                "vascular": "0",
                "vih": "0",
            }
        PeticionDiagnostico(**DATOS)