from re import compile

def validar_txt_token(token: str) -> bool:
    """
    Determina si el texto proveído es un token.

    Args:
        token (str): Token a probar.

    Returns:
        bool: Si el texto es un token.
    """
    EXP = compile(r"^(\w|-|_|\.)+$")

    return (EXP.fullmatch(token) is not None) and len(token) >= 817

def validar_uid(uid: str) -> bool:
    """
    Determina si el texto proveído es un UID.

    Args:
        uid (str): UID a probar.

    Returns:
        bool: Si el texto es un UID.
    """
    EXP = compile(r"^\w{28}$")

    return EXP.fullmatch(uid) is not None

def proc_origen(texto: str) -> str:
    """
    Reemplaza todas las coincidencias del comodín * por una expresión regular.

    Args:
        texto (str): Texto a procesar.
    Returns:
        str: Texto procesado.
    """
    texto = texto.replace("*", r"([\w|-|_|.|/|:])*")
    return texto

def validar_origen(texto: str, origenes: list[str]) -> bool:
    """
    Valida si el texto proveído está dentro de la lista de origenes.

    Args:
        texto (str): Texto a procesar.
        origenes (list[str]): Lista de origenes a validar.
    Returns:
        bool: Si el texto es un origen válido.
    """
    for i in origenes:
        EXP = compile(f"^{proc_origen(i)}$")
        if EXP.fullmatch(texto) is not None:
            return True
    return False