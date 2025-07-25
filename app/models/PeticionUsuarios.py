from pydantic import BaseModel

class PeticionUsuarios(BaseModel):
    correo: str