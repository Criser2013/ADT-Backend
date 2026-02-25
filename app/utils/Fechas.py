from datetime import datetime, timezone, timedelta

def convertir_hora(hora: int, minuto: int) -> str:
    """
    Convierte una hora y minuto en una cadena de texto con formato HH:MM.

    Args:
        hora (int): La hora a convertir.
        minuto (int): El minuto a convertir.

    Returns:
        str: La hora en formato HH:MM.
    """
    HORA = hora % 12
    AUXHORA = 12 if (HORA == 0) else HORA
    momento = "PM" if hora >= 12 else "AM"


    return f"{AUXHORA:02d}:{minuto:02d} {momento}"

def convertir_datetime_str(tiempo: int) -> str:
    """
    Convierte un objeto datetime a una cadena de texto en formato ISO 8601.

    Args:
        tiempo (int): El tiempo en milisegundos desde la época (1 de enero de 1970).

    Returns:
        str: La fecha en formato ISO 8601.
    """

    fecha = datetime.fromtimestamp(
        tiempo / 1000,
        tz=timezone(timedelta(hours=-5)),
    )
    HORA = convertir_hora(fecha.hour, fecha.minute)
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year} {HORA}"