from onnxruntime import InferenceSession
from pathlib import Path
from numpy import ndarray, zeros, float32, array
from utils.Preprocesamiento import preprocesar_instancias
from constants import EXPLAINER


class Diagnostico:
    """
    Clase que representa una instancia de diagnóstico usando el modelo
    de red neuronal en ONNX.
    """

    def __init__(self, datos: ndarray):
        self.datos = datos
        self.BASE_PATH = Path(__file__).resolve().parent.parent

    def obtener_probabilidades_predicciones(
        self, instancias: ndarray, sesion: InferenceSession
    ) -> ndarray:
        """
        Hace la clasificación de varias instancias empleando el modelo

        Args:
            instancias (ndarray): Las instancias a clasificar.
            sesion (InferenceSession): La sesión de inferencia de ONNX.

        Returns:
            ndarray: Las probabilidades de pertenecer a una clase u otra según el modelo.
        """
        input_name = sesion.get_inputs()[0].name
        instancias = preprocesar_instancias(instancias)
        RES = sesion.run(None, {input_name: instancias})
        ARRAY = zeros((len(instancias), 2), dtype=float32)

        for i in range(instancias.shape[0]):
            ARRAY[i] = array([RES[1][i][0], RES[1][i][1]])

        return ARRAY

    def generar_explicacion(self, sesion):
        """
        Genera una explicación para la predicción de la instancia usando LIME (5000 muestras y máximo 10 atributos).

        Args:
            sesion (InferenceSession): La sesión de inferencia de ONNX.
        """
        explicacion = EXPLAINER.explain_instance(
            self.datos[0],
            lambda x: self.obtener_probabilidades_predicciones(x, sesion),
            num_features=10,
        )
        SALIDA = []
        explicacion = explicacion.as_list()

        for i in explicacion:
            CAMPO = i[0].split("=")
            SALIDA.append(
                {
                    "campo": CAMPO[0],
                    "contribucion": round(i[1] * 100, 2),
                }
            )

        self.explicacion = SALIDA

    def generar_diagnostico(self):
        """
        Genera el diagnóstico de los datos usando el modelo ONNX para normalizarlos
        y luego clasificarlos
        """
        sesion = InferenceSession(
            f"{self.BASE_PATH}/bin/modelo_red_neuronal.onnx",
            providers=["CPUExecutionProvider"],
        )
        input_name = sesion.get_inputs()[0].name
        preprocesados = preprocesar_instancias(self.datos)
        pred = sesion.run(None, {input_name: preprocesados })
        self.generar_explicacion(sesion)
        RES = pred[0][0]

        return {
            "prediccion": int(RES) == 1,
            "probabilidad": float(pred[1][0][RES]),
            "lime": self.explicacion,
        }
