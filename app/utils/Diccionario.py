from typing import Any

def ver_si_existe_clave(diccionario: dict | Any, clave: str) -> bool:
    """
    Verifica si una clave existe en un diccionario.
    Args:
        diccionario (dict|Header): El diccionario en el que buscar la clave.
        clave (str): La clave a verificar.
    Returns:
        bool: `True` si la clave existe, `False` en caso contrario.
    """
    return clave in diccionario.keys()