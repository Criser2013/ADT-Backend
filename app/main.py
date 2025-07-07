import firebase_admin._utils
import firebase_admin.auth
from dotenv import load_dotenv
import firebase_admin
from firebase_admin.auth import get_user
from datetime import datetime
from utils.Validadores import validar_fecha

# from apis.Firestore import *
from pathlib import Path
from os import getenv
from os.path import join
from typing import Annotated
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from apis.Firestore import verificar_token


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

# CORS
FRONT_URL = getenv("FRONT_URL")

ORIGENES = [FRONT_URL] if FRONT_URL else ["*"]

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


class Diagnostico(BaseModel):
    uid: str


@app.middleware("http")
async def verificar_credenciales(peticion: Diagnostico, call_next):
    if peticion.method == "POST":
        return await verificar_token(peticion, firebase_app, call_next)
    else:
        return await call_next(peticion)


@app.get("/credenciales")
async def obtener_credenciales():
    try:
        return Response(
            str(FIREBASE_CLIENTE), status_code=200, media_type="application/json"
        )
    except:
        return Response("Error al obtener las credenciales", status_code=500)


@app.post("/diagnosticar")
async def diagnosticar(req: Request):
    try:
        """data = await req.json()
        fecha = data.get("fecha")
        if not fecha or not validar_fecha(fecha):
            return Response("Fecha inválida", status_code=400)"""

        # Aquí se puede agregar la lógica de diagnóstico
        # Por ejemplo, consultar Firestore o realizar cálculos

        return Response("Diagnóstico realizado con éxito", status_code=200)
    except Exception as e:
        return Response(f"Error al procesar la solicitud: {str(e)}", status_code=500)


"""from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item"""
