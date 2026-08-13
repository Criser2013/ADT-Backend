from pydantic import BaseModel
from utils.Fechas import convertir_datetime_str


class Usuario(BaseModel):
    """
    Clase para representar los datos de un usuario de la aplicación.
    """
    correo: str
    uid: str
    nombre: str
    estado: bool
    administrador: bool
    fecha_registro: str
    ultima_conexion: str

    def __init__(
        self,
        correo: str,
        uid: str,
        nombre: str,
        estado: bool,
        administrador: bool,
        fecha_registro: int,
        ultima_conexion: int,
    ):
        """
        Args:
            correo (str): Correo electrónico.
            uid (str): UID de Firebase.
            nombre (str): Nombre de usuario de Google.
            estado (bool): Indicador de si la cuenta está activa (`True`) o no (`False`).
            administrador (bool): Indicador de si el usuario es administrador (`True`, 'False' sino lo es).
            fecha_registro (int): Fecha y hora de registro expresada en milisegundos (timestamp de Firebase).
            ultima_conexion (int): Fecha y hora de último acceso a laaplicación expresada en milisegundos (timestamp de Firebase).
        """
        FECHA_REGISTRO = convertir_datetime_str(fecha_registro)
        ULTIMA_CONEXION = convertir_datetime_str(ultima_conexion)
        super().__init__(
            correo=correo,
            uid=uid,
            nombre=nombre,
            estado=estado,
            administrador=administrador,
            fecha_registro=FECHA_REGISTRO,
            ultima_conexion=ULTIMA_CONEXION,
        )
