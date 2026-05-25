from firebase_admin import initialize_app, App
from firebase_admin.credentials import Certificate
from pathlib import Path
from os.path import join, exists
from os import getenv

def inicializar_firebase() -> App:
    """
    Inicializa la aplicación de Firebase utilizando las credenciales proporcionadas en un archivo JSON.

    Returns:
        firebase_admin.App: Una instancia de la aplicación de Firebase inicializada.
    """
    ALT_PATH = Path(getenv("FIREBASE_ADMIN_CREDS_PATH", ""))

    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = join(BASE_DIR, "firebase_token.json") if (ALT_PATH != "" and (not exists(ALT_PATH))) else ALT_PATH

    # Inicialización del servicio de Firebase
    cred = Certificate(PATH)
    return initialize_app(cred)