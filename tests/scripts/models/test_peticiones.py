import pytest
from models.Peticiones import *
from pydantic import ValidationError


DATOS_INSTANCIA_1 = {
    "edad": 68, "sexo": 1, "bebedor": 0, "fumador": 0, "proc_quirurgico_traumatismo": 0,
    "inmovilidad_de_m_inferiores": 0, "viaje_prolongado": 0, "TEP_TVP_previo": 0,
    "malignidad": 1, "disnea": 0, "dolor_toracico": 1, "tos": 0, "hemoptisis": 0,
    "sintomas_disautonomicos": 0, "edema_de_m_inferiores": 1, "frecuencia_respiratoria": 18,
    "saturacion_de_la_sangre": 91, "frecuencia_cardiaca": 112, "presion_sistolica": 110,
    "presion_diastolica": 70, "fiebre": 0, "crepitaciones": 0, "sibilancias": 0, "soplos": 0,
    "wbc": 6800, "hb": 13, "plt": 313400, "derrame": 0, "otra_enfermedad": 1, "hematologica": 1,
    "cardiaca": 0, "enfermedad_coronaria": 0, "diabetes_mellitus": 0, "endocrina": 1,
    "gastrointestinal": 1, "hepatopatia_cronica": 0, "hipertension_arterial": 1, "neurologica": 0,
    "pulmonar": 0, "renal": 0, "trombofilia": 0, "urologica": 0, "vascular": 0, "vih": 0,
}

DATOS_INSTANCIA_2 = {
    "edad": -68, "sexo": 1, "bebedor": 0, "fumador": 0, "proc_quirurgico_traumatismo": 0,
    "inmovilidad_de_m_inferiores": 0, "viaje_prolongado": 0, "TEP_TVP_previo": 0,
    "malignidad": 1, "disnea": 0, "dolor_toracico": 1, "tos": 0, "hemoptisis": 0,
    "sintomas_disautonomicos": 0, "edema_de_m_inferiores": 1, "frecuencia_respiratoria": 18,
    "saturacion_de_la_sangre": 91, "frecuencia_cardiaca": 112, "presion_sistolica": 110,
    "presion_diastolica": 70, "fiebre": 0, "crepitaciones": 0, "sibilancias": 0, "soplos": 0,
    "wbc": 6800, "hb": 13, "plt": 313400, "derrame": 0, "otra_enfermedad": 1, "hematologica": 1,
    "cardiaca": 0, "enfermedad_coronaria": 0, "diabetes_mellitus": 0, "endocrina": 1,
    "gastrointestinal": 1, "hepatopatia_cronica": 0, "hipertension_arterial": 1, "neurologica": 0,
    "pulmonar": 0, "renal": 0, "trombofilia": 0, "urologica": 0, "vascular": 0, "vih": 0,
}

DATOS_INSTANCIA_3 = {
    "edad": 68, "sexo": 2, "bebedor": 0, "fumador": 0, "proc_quirurgico_traumatismo": 0,
    "inmovilidad_de_m_inferiores": 0, "viaje_prolongado": 0, "TEP_TVP_previo": 0,
    "malignidad": 1, "disnea": 0, "dolor_toracico": 1, "tos": 0, "hemoptisis": 0,
    "sintomas_disautonomicos": 0, "edema_de_m_inferiores": 1, "frecuencia_respiratoria": 18,
    "saturacion_de_la_sangre": 91, "frecuencia_cardiaca": 112, "presion_sistolica": 110,
    "presion_diastolica": 70, "fiebre": 0, "crepitaciones": 0, "sibilancias": 0, "soplos": 0,
    "wbc": 6800, "hb": 13, "plt": 313400, "derrame": 0, "otra_enfermedad": 1, "hematologica": 1,
    "cardiaca": 0, "enfermedad_coronaria": 0, "diabetes_mellitus": 0, "endocrina": 1,
    "gastrointestinal": 1, "hepatopatia_cronica": 0, "hipertension_arterial": 1, "neurologica": 0,
    "pulmonar": 0, "renal": 0, "trombofilia": 0, "urologica": 0, "vascular": 0, "vih": 0,
}

RES_ESPERADA = {
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

@pytest.mark.parametrize(
    "datos,respuesta_esperada,arroja_excepcion",
    (
        (DATOS_INSTANCIA_1.copy(), RES_ESPERADA.copy(), False),
        (DATOS_INSTANCIA_2.copy(), None, True),
        (DATOS_INSTANCIA_3.copy(), None, True),
    ),
    ids=["test_5", "test_6", "test_55"],
)
def test_instancia_diagnostico(datos, respuesta_esperada, arroja_excepcion):
    """
    Test para validar que la clase valide correctamente una instancia de diagnóstico.
    """
    if arroja_excepcion:
        with pytest.raises(ValidationError):
            InstanciaDiagnostico(**datos)
    else:
        OBJ = InstanciaDiagnostico(**datos)
        RES = OBJ.obtener_diccionario_instancia()
        assert RES == respuesta_esperada


@pytest.mark.parametrize(
    "token,respuesta_esperada,arroja_excepcion",
    [("a" * 829, "a" * 829, False), (123, None, True), ("token_invalido", None, True)],
    ids=["test_66", "test_67", "test_62"],
)
def test_token_captcha(token, respuesta_esperada, arroja_excepcion):
    """
    Test para validar que la clase valida correctamente un token de Recaptcha
    """
    if arroja_excepcion:
        with pytest.raises(ValidationError):
            TokenRecaptcha(token=token)
    else:
        instancia = TokenRecaptcha(token=token)
        assert instancia.token == respuesta_esperada


@pytest.mark.parametrize(
    "datos,arroja_excepcion",
    [
        ({"desactivar": False, "administrador": True, "eliminado": False}, False),
        ({"desactivar": 2, "administrador": "True"}, True),
    ],
    ids=["test_29", "test_30"],
)
def test_datos_usuario(datos, arroja_excepcion):
    """
    Test para validar que la clase valida correctamente los datos de un usuario a actualizar
    """
    if arroja_excepcion:
        with pytest.raises(ValidationError):
            DatosUsuario(**datos)
    else:
        instancia = DatosUsuario(**datos)
        assert instancia.desactivar == datos["desactivar"]
        assert instancia.administrador == datos["administrador"]
