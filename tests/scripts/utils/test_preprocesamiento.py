from app.utils.Preprocesamiento import *

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
    Validar que la función preprocesar_instancia retorne la instancia correctamente
    """
    INSTANCIA = {
            "Inmovilidad_de_M_inferiores": [1], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [0],
            "Viaje_prolongado": [0], "Síntomas_disautonomicos": [0], "Edema_de_M_inferiores": [1],
            "Diabetes_Mellitus": [0], "Hipertensión_arterial": [1], "Enfermedad_coronaria": [0],
            "Dolor_toracico": [1], "TEP___TVP_Previo": [0], "Frecuencia_respiratoria": [22],
            "Presión_sistólica": [120], "Presión_diastólica": [80], "Saturación_de_la_sangre": [95], "Frecuencia_cardíaca": [85],
            "WBC": [8000], "HB": [14], "PLT": [300000], "Género": [0], "Edad": [30], "Fumador": [0], "Bebedor": [0], "Malignidad": [1],
            "Disnea": [0], "Tos": [0], "Hemoptisis": [0], "Fiebre": [0], "Crepitaciones": [0], "Sibilancias": [0],
            "Soplos": [0], "Derrame": [0], "Trombofilia": [0], "VIH": [0], "Otra_Enfermedad": [1], "Hematologica": [1], "Cardíaca": [0],
            "Hepatopatía_crónica": [0], "Renal": [0], "Cardíaca": [0], "Neurológica": [0], "Pulmonar": [0], "Endocrina": [0],
            "Gastrointestinal": [0], "Urológica": [0], "Vascular": [0],
        }
    RES = {
            "Inmovilidad_de_M_inferiores": [1], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [0],
            "Viaje_prolongado": [0], "Síntomas_disautonomicos": [0], "Edema_de_M_inferiores": [1],
            "Diabetes_Mellitus": [0], "Hipertensión_arterial": [1], "Enfermedad_coronaria": [0],
            "Dolor_toracico": [1], "TEP___TVP_Previo": [0], "Frecuencia_respiratoria": [2],
            "Presión_sistólica": [4], "Presión_diastólica": [5], "Saturación_de_la_sangre": [10], "Frecuencia_cardíaca": [2],
            "WBC": [2], "HB": [5], "PLT": [4], "Género": [0], "Edad": [1], "Fumador": [0], "Bebedor": [0], "Malignidad": [1],
            "Disnea": [0], "Tos": [0], "Hemoptisis": [0], "Fiebre": [0], "Crepitaciones": [0], "Sibilancias": [0],
            "Soplos": [0], "Derrame": [0], "Trombofilia": [0], "VIH": [0], "Otra_Enfermedad": [1], "Hematologica": [1], "Cardíaca": [0],
            "Hepatopatía_crónica": [0], "Renal": [0], "Cardíaca": [0], "Neurológica": [0], "Pulmonar": [0], "Endocrina": [0],
            "Gastrointestinal": [0], "Urológica": [0], "Vascular": [0],
        }
    
    assert preprocesar_instancia(INSTANCIA) == RES