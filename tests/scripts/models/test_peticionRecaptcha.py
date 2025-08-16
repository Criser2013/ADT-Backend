from app.models.PeticionRecaptcha import PeticionRecaptcha
from pydantic import ValidationError
import pytest

def test_66():
    """
    Test para validar que la clase reconoce correctamente una instancia.
    """
    instancia = PeticionRecaptcha(**{"token": "test_token"})
    assert instancia.token == "test_token"

def test_67():
    """
    Test para validar que la clase lanza un error con datos inválidos.
    """
    with pytest.raises(ValidationError):
        PeticionRecaptcha(**{"token": 123})