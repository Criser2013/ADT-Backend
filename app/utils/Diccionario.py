def ver_si_existe_clave(diccionario: dict, clave: str) -> bool:
    """
    Verifica si una clave existe en un diccionario.
    Args:
        diccionario (dict): El diccionario en el que buscar la clave.
        clave (str): La clave a verificar.
    Returns:
        bool: True si la clave existe, False en caso contrario.
    """
    try:
        diccionario[clave]
        return True
    except KeyError:
        return False