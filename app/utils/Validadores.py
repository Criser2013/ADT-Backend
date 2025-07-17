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