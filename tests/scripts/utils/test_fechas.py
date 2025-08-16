from datetime import datetime
from app.utils.Fechas import *

def test_18():
    """
    Test para validar que la función convierte correctamente una hora y minuto
    en formato HH:MM de 12 horas cuando son las 12 AM.
    """
    hora = 0
    minuto = 30
    resultado = convertir_hora(hora, minuto)
    assert resultado == "12:30 AM"

def test_19():
    """
    Test para validar que la función convierte correctamente una hora y minuto
    en formato HH:MM de 12 horas cuando son las 12 del mediodía (12 PM).
    """
    hora = 12
    minuto = 30
    resultado = convertir_hora(hora, minuto)
    assert resultado == "12:30 PM"

def test_20():
    """
    Test para validar que la función convierte correctamente una hora y minuto
    en formato HH:MM de 12 horas cuando la hora no es divisible entre 12.
    """
    hora = 14
    minuto = 59
    resultado = convertir_hora(hora, minuto)
    assert resultado == "02:59 PM"

def test_21():
    """
    Test para validar que la función convierte correctamente un objeto datetime
    a una cadena de texto en formato ISO 8601.
    """
    fecha = 1759674600 * 1000
    resultado = convertir_datetime_str(fecha)
    assert resultado == "05/10/2025 09:30 AM"