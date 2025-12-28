from pydantic import BaseModel
from numpy import array, float32

class PeticionDiagnostico(BaseModel):
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