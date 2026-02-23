from pydantic import BaseModel, model_validator
from utils.Validadores import validar_txt_token

class TokenRecaptcha(BaseModel):
    """
    Clase que representa una petición para validar un token de reCAPTCHA.
    """
    token: str

    @model_validator(mode="after")
    def validar_token(self):
        if not validar_txt_token(self.token):
            raise ValueError("El token de reCAPTCHA no es válido")
        return self


class InstanciaDiagnostico(BaseModel):
    """
    Clase que representa una petición de diagnóstico con los datos necesarios.
    Esta clase solo valida que los datos sean del tipo correcto y los valores
    requeridos para el diagnostico estén presentes.
    """
    edad: int
    sexo: int
    bebedor: int
    fumador: int
    proc_quirurgico_traumatismo: int
    inmovilidad_de_m_inferiores: int
    viaje_prolongado: int
    TEP_TVP_previo: int
    malignidad: int
    disnea: int
    dolor_toracico: int
    tos: int
    hemoptisis: int
    sintomas_disautonomicos: int
    edema_de_m_inferiores: int
    frecuencia_respiratoria: int
    saturacion_de_la_sangre: float
    frecuencia_cardiaca: int
    presion_sistolica: int
    presion_diastolica: int
    fiebre: int
    crepitaciones: int
    sibilancias: int
    soplos: int
    wbc: float
    hb: float
    plt: float
    derrame: int
    otra_enfermedad: int
    hematologica: int
    cardiaca: int
    enfermedad_coronaria: int
    diabetes_mellitus: int
    endocrina: int
    gastrointestinal: int
    hepatopatia_cronica: int
    hipertension_arterial: int
    neurologica: int
    pulmonar: int
    renal: int
    trombofilia: int
    urologica: int
    vascular: int
    vih: int

    @model_validator(mode="after")
    def validar_datos(self):
        numericas = {"edad": self.edad, "wbc": self.wbc, "hb": self.hb, "plt": self.plt, "frecuencia_respiratoria": self.frecuencia_respiratoria, 
                     "saturacion_de_la_sangre": self.saturacion_de_la_sangre, "frecuencia_cardiaca": self.frecuencia_cardiaca,
                     "presion_sistolica": self.presion_sistolica, "presion_diastolica": self.presion_diastolica}
        booleanas = {"sexo": self.sexo, "bebedor": self.bebedor, "fumador": self.fumador, "proc_quirurgico_traumatismo": self.proc_quirurgico_traumatismo,
                     "inmovilidad_de_m_inferiores": self.inmovilidad_de_m_inferiores, "viaje_prolongado": self.viaje_prolongado, "TEP_TVP_previo": self.TEP_TVP_previo,
                     "malignidad": self.malignidad, "disnea": self.disnea, "dolor_toracico": self.dolor_toracico, "tos": self.tos, "hemoptisis": self.hemoptisis,
                     "sintomas_disautonomicos": self.sintomas_disautonomicos, "edema_de_m_inferiores": self.edema_de_m_inferiores, "fiebre": self.fiebre,
                     "crepitaciones": self.crepitaciones, "sibilancias": self.sibilancias, "soplos": self.soplos, "derrame": self.derrame,
                     "otra_enfermedad": self.otra_enfermedad, "hematologica": self.hematologica, "cardiaca": self.cardiaca,
                     "enfermedad_coronaria": self.enfermedad_coronaria, "diabetes_mellitus": self.diabetes_mellitus, "endocrina": self.endocrina,
                     "gastrointestinal": self.gastrointestinal, "hepatopatia_cronica":self.hepatopatia_cronica,"hipertension_arterial": self.hipertension_arterial,
                     "neurologica" :self.neurologica,"pulmonar" :self.pulmonar,"renal" :self.renal,"trombofilia" :self.trombofilia,"urologica" :self.urologica,
                     "vascular": self.vascular, "vih": self.vih}

        for i in booleanas.keys():
            if booleanas[i] not in (0, 1):
                raise ValueError(f"El valor {i} no es válido para un campo booleano")
        for i in numericas.keys():
            if numericas[i] < 0:
                raise ValueError(f"El valor {i} no puede ser negativo")
        return self

    def obtener_diccionario_instancia(self):
        """
            Convierte la instancia de la petición de diagnóstico en diccionario

            Returns:
                dict: Diccionario con los valores de la instancia
        """
        return {
            "Inmovilidad_de_M_inferiores": [self.inmovilidad_de_m_inferiores], "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [self.proc_quirurgico_traumatismo],
            "Viaje_prolongado": [self.viaje_prolongado], "Síntomas_disautonomicos": [self.sintomas_disautonomicos], "Edema_de_M_inferiores": [self.edema_de_m_inferiores],
            "Dolor_toracico": [self.dolor_toracico], "TEP___TVP_Previo": [self.TEP_TVP_previo], "Frecuencia_respiratoria": [self.frecuencia_respiratoria],
            "Presión_sistólica": [self.presion_sistolica], "Presión_diastólica": [self.presion_diastolica], "Saturación_de_la_sangre": [self.saturacion_de_la_sangre], "Frecuencia_cardíaca": [self.frecuencia_cardiaca],
            "WBC": [self.wbc], "HB": [self.hb], "PLT": [self.plt], "Género": [self.sexo], "Edad": [self.edad], "Fumador": [self.fumador], "Bebedor": [self.bebedor], "Malignidad": [self.malignidad],
            "Disnea": [self.disnea], "Tos": [self.tos], "Hemoptisis": [self.hemoptisis], "Fiebre": [self.fiebre], "Crepitaciones": [self.crepitaciones], "Sibilancias": [self.sibilancias],
            "Soplos": [self.soplos], "Derrame": [self.derrame], "Otra_Enfermedad": [self.otra_enfermedad], "Diabetes_Mellitus": [self.diabetes_mellitus],
            "Hipertensión_arterial": [self.hipertension_arterial], "Enfermedad_coronaria": [self.enfermedad_coronaria], "Trombofilia": [self.trombofilia], "VIH": [self.vih],
            "Hepatopatía_crónica": [self.hepatopatia_cronica], "Renal": [self.renal], "Cardíaca": [self.cardiaca], "Neurológica": [self.neurologica], "Pulmonar": [self.pulmonar], "Endocrina": [self.endocrina],
            "Gastrointestinal": [self.gastrointestinal], "Hematologica": [self.hematologica], "Urológica": [self.urologica], "Vascular": [self.vascular],
        }