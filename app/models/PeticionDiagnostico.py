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
    cirugia_reciente:int
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
    saturacion_de_la_sangre: int
    frecuencia_cardiaca: int
    presion_sistolica: int
    presion_diastolica: int
    fiebre: int
    crepitaciones: int
    sibilancias: int
    soplos: int
    wbc: int
    hb: int
    plt: int
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

    def obtener_array_instancia(self):
        """
            Convierte la instancia de la petición de diagnóstico en un array de numpy

            Returns:
                numpy.array: Array con los valores de la instancia
        """
        return array([[
            self.edad, self.sexo, self.bebedor, self.fumador,
            self.cirugia_reciente, self.inmovilidad_de_m_inferiores,
            self.viaje_prolongado, self.TEP_TVP_previo, self.malignidad,
            self.disnea, self.dolor_toracico, self.tos,
            self.hemoptisis, self.sintomas_disautonomicos,
            self.edema_de_m_inferiores, self.frecuencia_respiratoria,
            self.saturacion_de_la_sangre, self.frecuencia_cardiaca,
            self.presion_sistolica, self.presion_diastolica,
            self.fiebre, self.crepitaciones, self.sibilancias,
            self.soplos, self.wbc, self.hb, self.plt,
            self.derrame, self.otra_enfermedad, self.hematologica,
            self.cardiaca, self.enfermedad_coronaria, self.diabetes_mellitus,
            self.endocrina, self.gastrointestinal, self.hepatopatia_cronica,
            self.hipertension_arterial, self.neurologica, self.pulmonar,
            self.renal, self.trombofilia, self.urologica, self.vascular,
            self.vih
        ],]).astype(float32).reshape(1, -1)