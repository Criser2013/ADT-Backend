from numpy import array, float32, ndarray

def evaluar_intervalo(val: int | float, intervalos: tuple[tuple]) -> int:
    """
    Evalúa en qué intervalo se encuentra un valor dado.

    Args:
        val (int|float): El valor a evaluar.
        intervalos (tuple[tuple]): Una lista de intervalos, donde cada intervalo es una tupla
                                    (inicio, fin, etiqueta).

    Returns:
        int: La etiqueta del intervalo en el que se encuentra el valor, o -1 si no se encuentra en ningún intervalo.
    """
    for i in intervalos:
        if (i[0] is not None) and (i[1] is not None):
            if (val >= i[0]) and (val < i[1]):
                return i[2]
        elif (i[0] is not None) and (i[1] is None):
            if val >= i[0]:
                return i[2]
        elif (i[0] is None) and (i[1] is not None):
            if val < i[1]:
                return i[2]
    return -1


def preprocesar_instancias(
    instancias: ndarray[ndarray[float32]],
) -> ndarray[ndarray[float32]]:
    """
    Preprocesa los atributos numéricos de las instancias.

    Args:
        instancias (ndarray[ndarray[float32]]): Las instancias a preprocesar.

    Returns:
        ndarray[ndarray[float32]]: Las instancias preprocesadas.
    """
    TAM = len(instancias)
    CLAVES = (
        # Edad
        (0, ((0, 20, 0), (20, 41, 1), (41, 61, 2), (61, 81, 3), (81, None, 4))),
        # Frecuencia respiratoria
        (15,
            ((15, 20, 1), (20, 25, 2), (25, 30, 3), (30, 35, 4), (35, 40, 5),
                (40, 45, 6), (45, 50, 7), (50, 55, 8), (55, 60, 9), (None, 15, 10),
                (60, None, 11)),
        ),
        # Saturación de la sangre (SO2)
        (16,
            ((50, 55, 1), (55, 60, 2), (60, 65, 3), (65, 70, 4), (70, 75, 5),
                (75, 80, 6), (80, 85, 7), (85, 90, 8), (90, 95, 9), (95, 100, 10),
                (None, 50, 11), (100, None, 12)),
        ),
        # Frecuencia cardiaca
        (17,
            ((50, 70, 1), (70, 90, 2), (90, 110, 3), (110, 130, 4), (130, 150, 5),
                (150, 170, 6), (170, 190, 7), (190, 210, 8), (None, 50, 9), (210, None, 10)),
        ),
        # Presión sistólica
        (18,
            ((50, 70, 1), (70, 90, 2), (90, 110, 3), (110, 130, 4), (130, 150, 5),
                (150, 170, 6), (170, 190, 7), (190, 210, 8), (None, 50, 9), (210, None, 10)),
        ),
        # Presión diastólica
        (19,
            ((40, 50, 1), (50, 60, 2), (60, 70, 3), (70, 80, 4), (80, 90, 5),
             (90, 100, 6), (100, 110, 7), (110, 120, 8), (None, 40, 9), (120, None, 10)),
        ),
        ( # Globulos blancos (WBC)
            24,
            ((2000, 4000, 1), (4000, 10000, 2), (10000, 15000, 3), (15000, 20000, 4),
                (20000, 30000, 5), (30000, 35000, 6), (None, 2000, 7), (35000, None, 7)),
        ),
        ( # Hemoglobina (HB)
            25,
            (
                (6, 8, 1), (8, 10, 2), (10, 12, 3), (12, 14, 4), (14, 16, 5), (16, 18, 6),
                (18, 20, 7), (20, 22, 8), (None, 6, 9), (22, None, 10)),
        ),
        ( # Plaquetas (PLT)
            26,
            ((10000, 50000, 1), (50000, 100000, 2), (100000, 150000, 3), (150000, 400000, 4),
                (400000, 500000, 5), (500000, 600000, 6), (600000, 700000, 7), (None, 10000, 9),
                (700000, None, 10)),
        ),
    )

    for i in range(TAM):
        for j in CLAVES:
            instancias[i][j[0]] = evaluar_intervalo(instancias[i][j[0]], j[1])

    return array(instancias).astype(float32).reshape(TAM, -1)
