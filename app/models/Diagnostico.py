from onnxruntime import InferenceSession
from pathlib import Path
from numpy import ndarray
from constants import EXPLAINER

class Diagnostico:
    """
    Clase que representa una instancia de diagnóstico usando el modelo
    de red neuronal en ONNX.
    """
    def __init__(self, datos: ndarray):
        self.datos = datos
        self.BASE_PATH = Path(__file__).resolve().parent.parent

    def generar_diagnostico(self):
        """
        Genera el diagnóstico de los datos usando el modelo ONNX para normalizarlos
        y luego clasificarlos
        """
        sesion = InferenceSession(f"{self.BASE_PATH}/bin/modelo_red_neuronal.onnx", providers=["CPUExecutionProvider"])
        input_name = sesion.get_inputs()[0].name
        pred = sesion.run(None, {input_name: self.datos})
        RES = pred[0][0]

        return { "prediccion": int(RES) == 1, "probabilidad": float(pred[1][0][RES]) }