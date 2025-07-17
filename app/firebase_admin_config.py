import firebase_admin
from pathlib import Path
from os.path import join, exists
from dotenv import load_dotenv
from os import getenv

load_dotenv()

ALT_PATH = Path(getenv("FIREBASE_ADMIN_CREDS_PATH", ""))

BASE_DIR = Path(__file__).resolve().parent.parent
PATH = join(BASE_DIR, "firebase_token.json") if (ALT_PATH != "" and (not exists(ALT_PATH))) else ALT_PATH

# Inicialización del servicio de Firebase
cred = firebase_admin.credentials.Certificate(PATH)
firebase_app = firebase_admin.initialize_app(cred)
