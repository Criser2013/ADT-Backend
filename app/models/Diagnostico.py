from numpy import ndarray, zeros, float32, array
from lime.lime_tabular import LimeTabularExplainer
from models.Respuestas import InstanciaDiagnosticada
from onnxruntime import InferenceSession
from utils.Preprocesamiento import preprocesar_instancia


class Diagnostico:
    """
    Clase que representa una instancia de diagnóstico usando el modelo
    de red neuronal en ONNX.
    """

    def __init__(
        self, datos: dict, modelo: InferenceSession, explicador: LimeTabularExplainer
    ):
        self.datos = datos
        self._modelo = modelo
        self._explicador = explicador

    def obtener_array_datos(self) -> ndarray:
        """
        Convierte los datos del diagnóstico en un array de numpy.

        Returns:
            ndarray: Los datos convertidos en un array de numpy.
        """
        AUX = []
        for i in self.datos.keys():
            AUX.append(self.datos[i][0])
        return array(AUX, dtype=float32)

    def convertir_a_diccionario(self, array_datos: ndarray) -> dict:
        """
        Convierte un array de numpy en un diccionario con los datos del diagnóstico.

        Args:
            array_datos (ndarray): El array de datos a convertir.

        Returns:
            dict: El diccionario con los datos del diagnóstico.
        """
        campos = (
            "Edad",
            "Género",
            "Bebedor",
            "Fumador",
            "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias",
            "Inmovilidad_de_M_inferiores",
            "Viaje_prolongado",
            "TEP___TVP_Previo",
            "Malignidad",
            "Disnea",
            "Dolor_toracico",
            "Tos",
            "Hemoptisis",
            "Síntomas_disautonomicos",
            "Edema_de_M_inferiores",
            "Frecuencia_respiratoria",
            "Saturación_de_la_sangre",
            "Frecuencia_cardíaca",
            "Presión_sistólica",
            "Presión_diastólica",
            "Fiebre",
            "Crepitaciones",
            "Sibilancias",
            "Soplos",
            "WBC",
            "HB",
            "PLT",
            "Derrame",
            "Otra_Enfermedad",
            "Hematologica",
            "Cardíaca",
            "Enfermedad_coronaria",
            "Diabetes_Mellitus",
            "Endocrina",
            "Gastrointestinal",
            "Hepatopatía_crónica",
            "Hipertensión_arterial",
            "Neurológica",
            "Pulmonar",
            "Renal",
            "Trombofilia",
            "Urológica",
            "Vascular",
            "VIH",
        )
        claves = {i: [] for i in campos}

        for i in array_datos:
            for j, clave in enumerate(claves.keys()):
                claves[clave].append(i[j])
        return claves

    def obtener_probabilidades_predicciones(self, instancias: ndarray) -> ndarray:
        """
        Hace la clasificación de varias instancias empleando el modelo

        Args:
            instancias (ndarray): Las instancias a clasificar.
        Returns:
            ndarray: Las probabilidades de pertenecer a una clase u otra según el modelo.
        """
        input_name = [i.name for i in self._modelo.get_inputs()]
        dict_instancias = self.convertir_a_diccionario(instancias)
        dict_preprocesadas = preprocesar_instancia(dict_instancias)
        NUM_INSTANCIAS = len(instancias)
        RES = self._modelo.run(
            None,
            {
                i: array(dict_preprocesadas[i], dtype=float32).reshape(-1, 1)
                for i in input_name
            },
        )
        ARRAY = zeros((NUM_INSTANCIAS, 2), dtype=float32)
        PROBS = RES[1]

        for i in range(NUM_INSTANCIAS):
            ARRAY[i] = array([PROBS[i][0], PROBS[i][1]])

        return ARRAY

    def generar_explicacion(self):
        """
        Genera una explicación para la predicción de la instancia usando LIME (5000 muestras y máximo 10 atributos).
        """
        explicacion = self._explicador.explain_instance(
            self.obtener_array_datos(),
            self.obtener_probabilidades_predicciones,
            num_features=10,
            num_samples=2000,
        )
        SALIDA = []
        explicacion = explicacion.as_list()

        for i in explicacion:
            SALIDA.append(
                {
                    "campo": i[0],
                    "contribucion": round(i[1] * 100, 2),
                }
            )

        self.explicacion = SALIDA

    def generar_diagnostico(self) -> InstanciaDiagnosticada:
        """
        Genera el diagnóstico de los datos usando el modelo ONNX para normalizarlos
        y luego clasificarlos

        Returns:
            InstanciaDiagnosticada: Clasificación de la instancia del diagnóstico según el modelo.
        """
        input_name = [i.name for i in self._modelo.get_inputs()]
        preprocesados = preprocesar_instancia(self.datos)
        pred = self._modelo.run(
            None,
            {
                i: array(preprocesados[i], dtype=float32).reshape(-1, 1)
                for i in input_name
            },
        )
        RES = pred[0][0]
        self.generar_explicacion()
        return InstanciaDiagnosticada(
            prediccion=int(RES) == 1,
            probabilidad=float(pred[1][0][1]),
            lime=self.explicacion,
        )
