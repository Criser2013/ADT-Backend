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