from pydantic import BaseModel

class PeticionRecaptcha(BaseModel):
    """
    Clase que representa una petición para validar un token de reCAPTCHA.
    """
    token: str