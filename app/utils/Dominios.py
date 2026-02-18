def obtener_lista_dominios(texto: str) -> list[str]:
    """
    Obtiene una lista de dominios a partir de un texto separado por comas.
        
    Args:
        texto (str): Texto que contiene los dominios separados por comas.
    Returns:
        list[str]: Lista de dominios sin espacios en blanco.
    """
    RES = [dominio.strip() for dominio in texto.split(",")]
    NUM_VACIOS = RES.count("")

    if NUM_VACIOS > 0:
        for i in range(NUM_VACIOS):
            RES.remove("")

    return RES