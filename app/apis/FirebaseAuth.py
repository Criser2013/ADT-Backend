import firebase_admin.auth
from firebase_admin.auth import *
from fastapi import Response, Request

def validar_token(token: str, firebase_app) -> int:
    """
        Verifica si el token de Firebase es válido.
        Args:
            token (str): El token de Firebase a verificar.
            firebase_app: La instancia de la aplicación Firebase.
        Returns:
            int: 1 si el token es válido, 0 en caso contrario y -1 si hay un error de validación.
    """
    try:
        firebase_admin.auth.verify_id_token(token, firebase_app, check_revoked=True)
        return 1
    except (ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError):
        return 0
    except (ValueError, CertificateFetchError, InvalidIdTokenError):
        return -1

async def verificar_token(peticion: Request, firebase_app, call_next):
    """
        Verifica el token de Firebase en la solicitud.
        Args:
            peticion (Diagnostico): La solicitud que contiene el token.
            firebase_app: La instancia de la aplicación Firebase.
            call_next: La función para pasar al siguiente middleware o ruta.
        Returns:
            Response: La respuesta de la solicitud, o un error si el token es inválido.
    """
    try:
        token = peticion.headers["authorization"].split("Bearer ")[1]
        res_validacion = validar_token(token, firebase_app)
        match res_validacion:
            case 1:
                return await call_next(peticion)
            case 0:
                return Response({ "error": "Token inválido" }, status_code=403, media_type="application/json")
            case -1:
                return Response({ "error": "Error al validar el token" }, status_code=400, media_type="application/json")
    except:
        return Response({ "error": "Error al procesar la solicitud" }, status_code=500, media_type="application/json")