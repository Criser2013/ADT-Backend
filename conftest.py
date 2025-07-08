import sys
import os
import pytest

# Configuración de directorio del proyecto para que las pruebas puedan importar módulos correctamente
@pytest.fixture(scope="session", autouse=True)
def cambiar_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)