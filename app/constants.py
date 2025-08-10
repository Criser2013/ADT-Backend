from dotenv import load_dotenv
from os import getenv
from utils.Dominios import obtener_lista_dominios

load_dotenv()

ROL_ADMIN = 1001
CORS_ORIGINS = obtener_lista_dominios(getenv("CORS_ORIGINS", "http://localhost:5178,"))
ALLOWED_HOSTS = obtener_lista_dominios(getenv("ALLOWED_HOSTS", "localhost,"))
CREDS_FIREBASE_CLIENTE = {
    "apiKey": getenv("CLIENTE_FIREBASE_API_KEY"),
    "authDomain": getenv("CLIENTE_FIREBASE_AUTH_DOMAIN"),
    "projectId": getenv("CLIENTE_FIREBASE_PROJECT_ID"),
    "storageBucket": getenv("CLIENTE_FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": getenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID"),
    "appId": getenv("CLIENTE_FIREBASE_APP_ID"),
    "measurementId": getenv("CLIENTE_FIREBASE_MEASUREMENT_ID"),
    "driveScopes": obtener_lista_dominios(getenv("CLIENTE_DRIVE_SCOPES","")),
    "reCAPTCHA": getenv("CLIENTE_CAPTCHA")
}