from app.models.Peticiones import TokenRecaptcha
from pydantic import ValidationError
import pytest

def test_66():
    """
    Test para validar que la clase reconoce correctamente una instancia.
    """
    instancia = TokenRecaptcha(**{"token": "a"*829})
    assert instancia.token == "a"*829

def test_67():
    """
    Test para validar que la clase lanza un error con datos inválidos.
    """
    with pytest.raises(ValidationError):
        TokenRecaptcha(**{"token": 123})