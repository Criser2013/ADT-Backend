import pytest
from app.utils.Fechas import *


@pytest.mark.parametrize(
    "hora,minuto,resultado_esperado",
    [(0, 30, "12:30 AM"), (12, 30, "12:30 PM"), (14, 59, "02:59 PM")],
    ids=["test_18", "test_19", "test_20"],
)
def test_convertir_hora(hora, minuto, resultado_esperado):
    """
    Test para validar que la función convierte correctamente una hora y minuto
    en formato HH:MM de 12 horas.
    """
    resultado = convertir_hora(hora, minuto)
    assert resultado == resultado_esperado

def test_21():
    """
    Test para validar que la función convierte correctamente un objeto datetime
    a una cadena de texto en formato 'DD/MM/YYYY HH:mm A'.
    """
    fecha = 1759674600 * 1000
    resultado = convertir_datetime_str(fecha)
    assert resultado == "05/10/2025 09:30 AM"
