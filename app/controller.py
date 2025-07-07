from main import firebase_app, app, FIREBASE_CLIENTE
from models import Diagnostico
from fastapi import Request, Response
from apis.FirebaseAuth import verificar_token

@app.middleware("http")
async def verificar_credenciales(peticion: Diagnostico, call_next):
    """
        Middleware para verificar las credenciales de Firebase en cada solicitud de diagnóstico.
        Args:
            peticion (Diagnostico): La solicitud que contiene el token.
            call_next: La función para pasar al siguiente middleware o ruta.
    """
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