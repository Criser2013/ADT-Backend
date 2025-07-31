from pathlib import Path
import sys

def configurar_path():
    PATH = Path(__file__).resolve()
    PROJECT_DIR = PATH.parent

    sys.path.insert(0, f"{PROJECT_DIR}/app")

configurar_path()