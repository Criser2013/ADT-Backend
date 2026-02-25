class AccesoNoAutorizado(Exception):
    """Excepción personalizada para indicar que el acceso no está autorizado."""

    def __init__(self, mensaje: str | dict, codigo: int):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(self.mensaje)

class UIDInvalido(Exception):
    """Excepción personalizada para indicar que el UID es inválido."""

    def __init__(self, mensaje: str | dict):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class UsuarioInexistente(Exception):
    """Excepción personalizada para indicar que el usuario no existe."""

    def __init__(self, mensaje: str | dict):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ErrorInterno(Exception):
    """Excepción personalizada para indicar que ocurrió un error interno."""

    def __init__(self, mensaje: str | dict):
        self.mensaje = mensaje
        super().__init__(self.mensaje)