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
    RES = OBJ.obtener_array_instancia()
    assert RES.all() == array([
        68,1,0,0,0,0,0,0,1,0,1,0,0,0,1,18,91,112,110,70,0,0,0,0,6800,13,313400,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ]).all()

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