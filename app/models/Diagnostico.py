from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
import numpy as np
import onnx
import onnxruntime as rt

class Diagnostico(BaseModel):
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

    def __init__(self, **data):
        super().__init__(**data)
        self.datos_normalizados = np.array([], dtype=np.float32)
        self.scaler = StandardScaler()        

    def normalizar_datos(self):
        """
        Normaliza los datos
        """
        ARR = np.array([
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
        ], dtype=np.float32)

        self.datos_normalizados = self.scaler.fit_transform(ARR)

    def generar_diagnostico(self):
        sesion = rt.InferenceSession("model_red_neuronal.onnx", providers=["CPUExecutionProvider"])
        input_name = sesion.get_inputs()[0].name

        pred = sesion.run(None, {input_name: self.datos_normalizados})[0]

        return { "prediccion": pred[0] == 1 }