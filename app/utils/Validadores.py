from re import compile
from datetime import datetime, timedelta

def validar_telefono(numero: str) -> bool:
    """
    Determina si el número de teléfono ingresado es realmente un
    número celular.

    Args:
        numero (str): Número de teléfono a probar.

    Returns:
        bool: Si el número es un número de teléfono.
    """
    EXP = compile("^[0-9]{10}$")

    return EXP.fullmatch(numero) is not None

def validar_sms(mensaje: str) -> bool:
    """
    Valida que el mensaje ingresado sea menor o igual a 160 carácteres.

    Args:
        mensaje (str): Mensaje.

    Returns:
        bool: Si el mensaje cumple con la restricción.
    """
    return len(mensaje) <= 160

def validar_fecha(fecha: datetime) -> bool:
    """
    Valida si la fecha ingresada no es anterior a 1 día de la fecha actual.

    Args:
        fecha (datetime): Fecha.

    Returns:
        bool: Si la fecha no es anterior a 1 día de la fecha actual.
    """
    AYER = datetime.now() - timedelta(days=1)
    
    return fecha > AYER