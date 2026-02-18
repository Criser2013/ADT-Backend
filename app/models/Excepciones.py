class AccesoNoAutorizado(Exception):
    """Excepción personalizada para indicar que el acceso no está autorizado."""

    def __init__(self, mensaje: str | dict, codigo: int):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(self.mensaje)