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

def validar_correo(correo: str) -> bool:
    """
    Determina si el texto proveído es un correo.

    Args:
        correo (str): Correo a probar.

    Returns:
        bool: Si el texto es un correo.
    """
    EXP = compile("^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$")

    return EXP.fullmatch(correo) is not None