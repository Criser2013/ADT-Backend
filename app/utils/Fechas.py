from datetime import datetime

def convertir_hora(hora: int, minuto: int) -> str:
    """
    Convierte una hora y minuto en una cadena de texto con formato HH:MM.

    Args:
        hora (int): La hora a convertir.
        minuto (int): El minuto a convertir.

    Returns:
        str: La hora en formato HH:MM.
    """
    AUXHORA = 12 if (hora == 0 or hora == 12) else (hora % 12)
    momento = "PM" if hora >= 12 else "AM"


    return f"{AUXHORA:02d}:{minuto:02d} {momento}"

def convertir_datetime_str(fecha: datetime) -> str:
    """
    Convierte un objeto datetime a una cadena de texto en formato ISO 8601.

    Args:
        fecha (datetime): El objeto datetime a convertir.

    Returns:
        str: La fecha en formato ISO 8601.
    """
    HORA = convertir_hora(fecha.hour, fecha.minute)
    return f"{fecha.day}/{fecha.month}/{fecha.year} {HORA}"