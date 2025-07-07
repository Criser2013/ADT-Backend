from dotenv import load_dotenv
import firebase_admin
from pathlib import Path
from os import getenv
from os.path import join
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Inicialización del servicio de Firebase
cred = firebase_admin.credentials.Certificate(join(BASE_DIR, "../firebase_token.json"))
firebase_app = firebase_admin.initialize_app(cred)

# Credenciales de Firebase para el cliente
FIREBASE_CLIENTE = {
    "apiKey": getenv("CLIENTE_FIREBASE_API_KEY"),
    "authDomain": getenv("CLIENTE_FIREBASE_AUTH_DOMAIN"),
    "projectId": getenv("CLIENTE_FIREBASE_PROJECT_ID"),
    "storageBucket": getenv("CLIENTE_FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": getenv("CLIENTE_FIREBASE_MESSAGING_SENDER_ID"),
    "appId": getenv("CLIENTE_FIREBASE_APP_ID"),
    "measurementId": getenv("CLIENTE_FIREBASE_MEASUREMENT_ID"),
    "driveScopes": getenv("CLIENTE_DRIVE_SCOPES"),
}

app = FastAPI()

# CORS
FRONT_URL = getenv("FRONT_URL")
ORIGENES = [FRONT_URL] if FRONT_URL else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)