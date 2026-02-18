from onnxruntime import InferenceSession
from lime.lime_tabular import LimeTabularExplainer
from pathlib import Path
from numpy import ndarray, zeros, float32, array
from utils.Preprocesamiento import preprocesar_instancia


class Diagnostico:
    """
    Clase que representa una instancia de diagnóstico usando el modelo
    de red neuronal en ONNX.
    """
    def __init__(self, datos: dict, modelo: InferenceSession, explicador: LimeTabularExplainer):
        self.datos = datos
        self.modelo = modelo
        self.explicador = explicador
        self.BASE_PATH = Path(__file__).resolve().parent.parent

    def obtener_array_datos(self) -> ndarray:
        """
        Convierte los datos del diagnóstico en un array de numpy.

        Returns:
            ndarray: Los datos convertidos en un array de numpy.
        """
        return array([self.datos["Edad"][0], self.datos["Género"][0], self.datos["Bebedor"][0], self.datos["Fumador"][0],
            self.datos["Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias"][0], self.datos["Inmovilidad_de_M_inferiores"][0],
            self.datos["Viaje_prolongado"][0], self.datos["TEP___TVP_Previo"][0], self.datos["Malignidad"][0],
            self.datos["Disnea"][0], self.datos["Dolor_toracico"][0], self.datos["Tos"][0],
            self.datos["Hemoptisis"][0], self.datos["Síntomas_disautonomicos"][0],
            self.datos["Edema_de_M_inferiores"][0], self.datos["Frecuencia_respiratoria"][0],
            self.datos["Saturación_de_la_sangre"][0], self.datos["Frecuencia_cardíaca"][0],
            self.datos["Presión_sistólica"][0], self.datos["Presión_diastólica"][0],
            self.datos["Fiebre"][0], self.datos["Crepitaciones"][0], self.datos["Sibilancias"][0],
            self.datos["Soplos"][0], self.datos["WBC"][0], self.datos["HB"][0], self.datos["PLT"][0],
            self.datos["Derrame"][0], self.datos["Otra_Enfermedad"][0], self.datos["Hematologica"][0],
            self.datos["Cardíaca"][0], self.datos["Enfermedad_coronaria"][0], self.datos["Diabetes_Mellitus"][0],
            self.datos["Endocrina"][0], self.datos["Gastrointestinal"][0], self.datos["Hepatopatía_crónica"][0],
            self.datos["Hipertensión_arterial"][0], self.datos["Neurológica"][0], self.datos["Pulmonar"][0],
            self.datos["Renal"][0], self.datos["Trombofilia"][0], self.datos["Urológica"][0], self.datos["Vascular"][0],
            self.datos["VIH"][0]], dtype=float32)

    def convertir_a_diccionario(self, array_datos: ndarray) -> dict:
        """
        Convierte un array de numpy en un diccionario con los datos del diagnóstico.

        Args:
            array_datos (ndarray): El array de datos a convertir.

        Returns:
            dict: El diccionario con los datos del diagnóstico.
        """
        claves = {
            "Edad": [], "Género": [], "Bebedor": [], "Fumador": [],
            "Procedimiento_Quirurgicos___Traumatismo_Grave_en_los_últimos_15_dias": [], "Inmovilidad_de_M_inferiores": [],
            "Viaje_prolongado": [], "TEP___TVP_Previo": [], "Malignidad": [],
            "Disnea": [], "Dolor_toracico": [], "Tos": [],
            "Hemoptisis": [], "Síntomas_disautonomicos": [],
            "Edema_de_M_inferiores": [], "Frecuencia_respiratoria": [],
            "Saturación_de_la_sangre": [], "Frecuencia_cardíaca": [],
            "Presión_sistólica": [], "Presión_diastólica": [],
            "Fiebre": [], "Crepitaciones": [], "Sibilancias": [],
            "Soplos": [], "WBC": [], "HB": [], "PLT": [],
            "Derrame": [], "Otra_Enfermedad": [], "Hematologica": [],
            "Cardíaca": [], "Enfermedad_coronaria": [], "Diabetes_Mellitus": [],
            "Endocrina": [], "Gastrointestinal": [], "Hepatopatía_crónica": [],
            "Hipertensión_arterial": [], "Neurológica": [], "Pulmonar": [],
            "Renal": [], "Trombofilia": [], "Urológica": [], "Vascular": [],
            "VIH": []
        }
        
        for i in array_datos:
            for j, clave in enumerate(claves.keys()):
                claves[clave].append(i[j])

        return claves

    def obtener_probabilidades_predicciones(
        self, instancias: ndarray
    ) -> ndarray:
        """
        Hace la clasificación de varias instancias empleando el modelo

        Args:
            instancias (ndarray): Las instancias a clasificar.

        Returns:
            ndarray: Las probabilidades de pertenecer a una clase u otra según el modelo.
        """
        input_name = [i.name for i in self.modelo.get_inputs()]
        instancias = self.convertir_a_diccionario(instancias)
        instancias = preprocesar_instancia(instancias)
        RES = self.modelo.run(None, {i: array(instancias[i], dtype=float32).reshape(-1, 1) for i in input_name})
        ARRAY = zeros((len(instancias["Edad"]), 2), dtype=float32)

        for i in range(len(instancias["Edad"])):
            ARRAY[i] = array([RES[1][i][0], RES[1][i][1]])

        return ARRAY

    def generar_explicacion(self):
        """
        Genera una explicación para la predicción de la instancia usando LIME (5000 muestras y máximo 10 atributos).
        """
        explicacion = self.explicador.explain_instance(
            self.obtener_array_datos(),
            lambda x: self.obtener_probabilidades_predicciones(x),
            num_features=10, num_samples=2000
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

    def generar_diagnostico(self):
        """
        Genera el diagnóstico de los datos usando el modelo ONNX para normalizarlos
        y luego clasificarlos
        """
        input_name = [i.name for i in self.modelo.get_inputs()]
        preprocesados = preprocesar_instancia(self.datos)
        pred = self.modelo.run(None, {i: array(preprocesados[i], dtype=float32).reshape(-1, 1) for i in input_name})
        self.generar_explicacion()
        RES = pred[0][0]

        return {
            "prediccion": int(RES) == 1,
            "probabilidad": float(pred[1][0][RES]),
            "lime": self.explicacion,
        }
