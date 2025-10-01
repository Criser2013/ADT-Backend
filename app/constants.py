from dotenv import load_dotenv
from os import getenv
from dill import load as dload
from json import load as jload
from pathlib import Path
from utils.Dominios import obtener_lista_dominios

load_dotenv()

with open(f"{Path(__file__).resolve().parent}/bin/explicador.pkl", "rb") as archivo:
    EXPLAINER = dload(archivo)

with open(f"{Path(__file__).resolve().parent}/bin/textos.json") as archivo:
    TEXTOS = jload(archivo)

ROL_ADMIN = 1001
CORS_ORIGINS = obtener_lista_dominios(getenv("CORS_ORIGINS", "http://localhost:5173,"))
ORIGENES_AUTORIZADOS = obtener_lista_dominios(getenv("ORIGENES_AUTORIZADOS", "http://localhost:5173,"))
ACTIVAR_DOCS = getenv("ACTIVAR_DOCS", "false").lower() == "true"
ALLOWED_HOSTS = obtener_lista_dominios(getenv("ALLOWED_HOSTS", "localhost,"))
RECAPTCHA_SECRET = getenv("CAPTCHA_SECRET")
RECAPTCHA_API_URL = getenv("API_RECAPTCHA_URL", "https://www.google.com/recaptcha/api/siteverify")
CREDS_FIREBASE_CLIENTE = {
    "apiKey": getenv("CLIENTE_FIREBASE_API_KEY"),
    "authDomain": getenv("CLIENTE_FIREBASE_AUTH_DOMAIN"),
    "projectId": getenv("CLIENTE_FIREBASE_PROJECT_ID"),
    "storageBucket": getenv("CLIENTE_FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": getenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID"),
    "appId": getenv("CLIENTE_FIREBASE_APP_ID"),
    "measurementId": getenv("CLIENTE_FIREBASE_MEASUREMENT_ID"),
    "driveScopes": obtener_lista_dominios(getenv("CLIENTE_DRIVE_SCOPES","")),
    "reCAPTCHA": getenv("CLIENTE_CAPTCHA"),
}