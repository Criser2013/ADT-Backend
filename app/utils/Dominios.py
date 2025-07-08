def obtener_lista_dominios(texto: str) -> list[str]:
    """
        Obtiene una lista de dominios a partir de un texto separado por comas.
        
        Args:
            texto (str): Texto que contiene los dominios separados por comas.
        Returns:
            list[str]: Lista de dominios sin espacios en blanco.
    """
    return [dominio.strip() for dominio in texto.split(",") if dominio.strip()]