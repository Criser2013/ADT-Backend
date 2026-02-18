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
    INF = float("inf")
    for i in intervalos:
        MIN, MAX, TAG = i
        if (MIN != -INF) and (MAX != INF):
            if (val >= MIN) and (val < MAX):
                return TAG
        elif (MIN != -INF) and (MAX == INF):
            if val >= MIN:
                return TAG
        elif (MIN == -INF) and (MAX != INF):
            if val < MAX:
                return TAG
    return -1


def preprocesar_instancia(
    instancia: dict[str, list[int | float]]
) -> dict[str, list[int | float]]:
    """
    Preprocesa los atributos numéricos de la instancia.

    Args:
        instancia (dict[str, list[int | float]]): La instancia a preprocesar.

    Returns:
        dict[str, list[int | float]]: La instancia preprocesada.
    """
    CLAVES = (
        # Edad
        ("Edad", ((0, 20, 0), (20, 41, 1), (41, 61, 2), (61, 81, 3), (81, float("inf"), 4))),
        # Frecuencia respiratoria
        ("Frecuencia_respiratoria",
            ((15, 20, 1), (20, 25, 2), (25, 30, 3), (30, 35, 4), (35, 40, 5),
                (40, 45, 6), (45, 50, 7), (50, 55, 8), (55, 60, 9), (-float("inf"), 15, 10),
                (60, float("inf"), 11)),
        ),
        # Saturación de la sangre (SO2)
        ("Saturación_de_la_sangre",
            ((50, 55, 1), (55, 60, 2), (60, 65, 3), (65, 70, 4), (70, 75, 5),
                (75, 80, 6), (80, 85, 7), (85, 90, 8), (90, 95, 9), (95, 100, 10),
                (-float("inf"), 50, 11), (100, float("inf"), 12)),
        ),
        # Frecuencia cardiaca
        ("Frecuencia_cardíaca",
            ((50, 70, 1), (70, 90, 2), (90, 110, 3), (110, 130, 4), (130, 150, 5),
                (150, 170, 6), (170, 190, 7), (190, 210, 8), (-float("inf"), 50, 9), (210, float("inf"), 10)),
        ),
        # Presión sistólica
        ("Presión_sistólica",
            ((50, 70, 1), (70, 90, 2), (90, 110, 3), (110, 130, 4), (130, 150, 5),
                (150, 170, 6), (170, 190, 7), (190, 210, 8), (-float("inf"), 50, 9), (210, float("inf"), 10)),
        ),
        # Presión diastólica
        ("Presión_diastólica",
            ((40, 50, 1), (50, 60, 2), (60, 70, 3), (70, 80, 4), (80, 90, 5),
             (90, 100, 6), (100, 110, 7), (110, 120, 8), (-float("inf"), 40, 9), (120, float("inf"), 10)),
        ),
        ( # Globulos blancos (WBC)
            "WBC",
            ((2000, 4000, 1), (4000, 10000, 2), (10000, 15000, 3), (15000, 20000, 4),
                (20000, 30000, 5), (30000, 35000, 6), (-float("inf"), 2000, 7), (35000, float("inf"), 8)),
        ),
        ( # Hemoglobina (HB)
            "HB",
            (
                (6, 8, 1), (8, 10, 2), (10, 12, 3), (12, 14, 4), (14, 16, 5), (16, 18, 6),
                (18, 20, 7), (20, 22, 8), (-float("inf"), 6, 9), (22, float("inf"), 10)),
        ),
        ( # Plaquetas (PLT)
            "PLT",
            ((10000, 50000, 1), (50000, 100000, 2), (100000, 150000, 3), (150000, 400000, 4),
                (400000, 500000, 5), (500000, 600000, 6), (600000, 700000, 7), (-float("inf"), 10000, 9),
                (700000, float("inf"), 10)),
        ),
    )

    for i in CLAVES:
        instancia[i[0]] = [evaluar_intervalo(j, i[1]) for j in instancia[i[0]]]
    return instancia