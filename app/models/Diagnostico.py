import numpy as np
import pickle
import onnxruntime as rt
from pathlib import Path

class Diagnostico():
    """
    Clase que representa una instancia de diagnóstico usando el modelo
    de red neuronal en ONNX.
    """
    def __init__(self, datos):
        self.datos = datos
        self.datos_normalizados = np.array([])
        self.scaler = None
        self.BASE_PATH = Path(__file__).resolve().parent.parent

        self.cargar_scaler()

    def cargar_scaler(self):
        """
            Carga el normalizador con el que fue entrenado el modelo desde un archivo pickle
        """
        with open(f"{self.BASE_PATH}/bin/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

    def normalizar_datos(self):
        """
            Normaliza los datos
        """
        self.datos_normalizados = self.scaler.transform([self.datos,])[0].astype(np.float32).reshape(1, -1)

    def generar_diagnostico(self):
        """
            Genera el diagnóstico de los datos normalizados usando el modelo ONNX
        """
        self.normalizar_datos()

        sesion = rt.InferenceSession(f"{self.BASE_PATH}/bin/modelo_red_neuronal.onnx", providers=["CPUExecutionProvider"])
        input_name = sesion.get_inputs()[0].name

        pred = sesion.run(None, {input_name: self.datos_normalizados})[0]

        return { "prediccion": pred[0] == 1 }