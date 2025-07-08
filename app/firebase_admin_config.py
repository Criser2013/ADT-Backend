import firebase_admin
from pathlib import Path
from os.path import join

BASE_DIR = Path(__file__).resolve().parent

# Inicialización del servicio de Firebase
cred = firebase_admin.credentials.Certificate(join(BASE_DIR, "../firebase_token.json"))
firebase_app = firebase_admin.initialize_app(cred)
