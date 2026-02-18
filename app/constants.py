from os import getenv
from utils.Dominios import obtener_lista_dominios

ROL_ADMIN = 1001
COD_EXITO = 1
COD_ERROR_ESPERADO = 0
COD_ERROR_INESPERADO = -1
CORS_ORIGINS = obtener_lista_dominios(getenv("CORS_ORIGINS", "http://localhost:5173,"))
ORIGENES_AUTORIZADOS = obtener_lista_dominios(getenv("ORIGENES_AUTORIZADOS", "http://localhost:5173,"))
ACTIVAR_DOCS = getenv("ACTIVAR_DOCS", "false").lower() == "true"
ALLOWED_HOSTS = obtener_lista_dominios(getenv("ALLOWED_HOSTS", "localhost,"))
RECAPTCHA_SECRET = getenv("CAPTCHA_SECRET")
RECAPTCHA_API_URL = getenv("API_RECAPTCHA_URL", "https://www.google.com/recaptcha/api/siteverify")