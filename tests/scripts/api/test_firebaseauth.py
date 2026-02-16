from pytest_mock import MockerFixture
from fastapi import Request
import pytest
from app.apis.FirebaseAuth import *
from firebase_admin.auth import ExpiredIdTokenError, CertificateFetchError, ListUsersPage, ExportedUserRecord, UserMetadata

@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    mocker.patch("app.main.CORS_ORIGINS", ["http://localhost:5178",])
    mocker.patch("app.main.ALLOWED_HOSTS", ["localhost",], )
    yield
    mocker.resetall()

@pytest.mark.asyncio
async def test_11(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" retorne un error cuando el token
    es inválido
    """
    REQ = mocker.MagicMock(spec=Request)
    TEXTOS = {"es": {"errTokenInvalido": "Token inválido"}}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=False)

    RES = await verificar_token(REQ, "firebase_app", None, "Bearer token_invalido", TEXTOS, "es")

    assert RES.status_code == 403
    assert RES.body.decode("utf-8") == '{"error":"Token inválido"}'

    VALIDADOR.assert_called_once_with("token_invalido")

@pytest.mark.asyncio
async def test_12(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" retorne un error cuando ocurre
    una excepción al procesar la solicitud
    """
    REQ = mocker.MagicMock(spec=Request)
    TEXTOS = {"es": {"errValidarToken": "Error al validar el token"}}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token", return_value=-1)
    
    RES = await verificar_token(REQ, "firebase_app", None, "Bearer token_invalido", TEXTOS, "es")

    assert RES.status_code == 400
    assert RES.body.decode("utf-8") == '{"error":"Error al validar el token"}'

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

@pytest.mark.asyncio
async def test_13(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" maneje correctamente los
    errores inesperados al validar el token de Firebase.
    """
    REQ = mocker.MagicMock(spec=Request)
    TEXTOS = {"es": {"errTry": "Error al procesar la solicitud:"}}

    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token")
    FIREBASE_VAL.side_effect = Exception("Excepción imprevista")

    RES = await verificar_token(REQ, "firebase_app", None, "Bearer token_invalido", TEXTOS, "es")

    assert RES.status_code == 500
    assert RES.body.decode("utf-8") == '{"error":"Error al procesar la solicitud: Excepción imprevista"}'

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

def test_14(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token")
    FIREBASE.side_effect = ExpiredIdTokenError("Token expirado", "EL token está expirado.")

    RES = validar_token("token_invalido", "firebase_app", False)

    assert RES == 0
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)

def test_15(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token")
    FIREBASE.side_effect = CertificateFetchError("Error al obtener el certificado", "No se pudo obtener el certificado.")

    RES = validar_token("token_invalido", "firebase_app", False)

    assert RES == -1
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)

def test_22(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" retorne los datos del token cuando este
    es válido
    """
    FIREBASE = mocker.patch("firebase_admin.auth.verify_id_token", return_value={ "uid": "a1234H" })

    RES = validar_token("token_valido", "firebase_app", True)

    assert RES == (1, {"uid": "a1234H"})
    FIREBASE.assert_called_once_with("token_valido", "firebase_app", check_revoked=True)

def test_23(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" retorne los datos del token cuando este
    es válido
    """
    TEXTOS = {"es": {"errTry": "Error al procesar la solicitud:"}}
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    TOKEN = mocker.patch("app.apis.FirebaseAuth.validar_token", return_value=(1, {"uid": "a1234H"}))

    RES = ver_datos_token("Bearer token_valido", "firebase_app", "es", TEXTOS)

    assert RES == (1, {"uid": "a1234H"})
    VALIDADOR.assert_called_once_with("token_valido")
    TOKEN.assert_called_once_with("token_valido", "firebase_app", True)

def test_24(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" cuando se provee un token inválido.
    """
    TEXTOS = {"es": {"errTokenInvalido": "Token inválido"}}
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=False)
    TOKEN = mocker.patch("apis.FirebaseAuth.validar_token")

    RES = ver_datos_token("Bearer token_invalido", "firebase_app", "es", TEXTOS)

    assert RES == (0, {"error": "Token inválido"})
    VALIDADOR.assert_called_once_with("token_invalido")
    TOKEN.assert_not_called()

def test_25(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_token" maneje correctamente las
    excepciones.
    """
    TEXTOS = {"es": {"errProcesarToken": "Error al procesar el token"}}
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token")
    VALIDADOR.side_effect = Exception("Error inesperado")

    RES = ver_datos_token("Bearer token_invalido", "firebase_app", "es", TEXTOS)

    assert RES == (-1, {"error": "Error al procesar el token: Error inesperado."})
    VALIDADOR.assert_called_once_with("token_invalido")

@pytest.mark.asyncio
async def test_26(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" retorne los datos de los usuarios.
    """
    LISTA = mocker.MagicMock(spec=ListUsersPage)
    USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
    METADATOS = mocker.MagicMock(spec=UserMetadata)
    METADATOS.creation_timestamp = 1753549006090
    METADATOS.last_refresh_timestamp = 1753549008090

    USUARIO.email = "usuario@correo.com"
    USUARIO.uid = "12345"
    USUARIO.display_name = "usuario"
    USUARIO.user_metadata =  METADATOS
    USUARIO.disabled = False

    LISTA.users = [USUARIO]
    LISTA.has_next_page = False

    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_roles_usuarios")
    FIRESTORE.return_value = { "12345": 0 }

    FIREBASE = mocker.patch("firebase_admin.auth.list_users", return_value=LISTA)

    RES = await ver_datos_usuarios("firebase_app", "es", {})

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"usuarios":[{"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","rol":0,"estado":true,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"}]}'

    FIREBASE.assert_called_once_with(app="firebase_app")
    FIRESTORE.assert_called_once()

@pytest.mark.asyncio
async def test_27(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" retorne los datos de los usuarios
    cuando hay múltiples páginas de usuarios.
    """
    LISTA = mocker.MagicMock(spec=ListUsersPage)
    LISTA2 = mocker.MagicMock(spec=ListUsersPage)
    USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
    METADATOS = mocker.MagicMock(spec=UserMetadata)
    METADATOS.creation_timestamp = 1753549006090
    METADATOS.last_refresh_timestamp = 1753549008090

    USUARIO.email = "usuario@correo.com"
    USUARIO.uid = "12345"
    USUARIO.display_name = "usuario"
    USUARIO.user_metadata =  METADATOS
    USUARIO.disabled = False

    LISTA2.users = [USUARIO]
    LISTA2.has_next_page = False

    LISTA.users = [USUARIO]
    LISTA.has_next_page = True
    LISTA.get_next_page.side_effect = lambda: LISTA2

    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_roles_usuarios")
    FIRESTORE.return_value = { "12345": 0 }

    FIREBASE = mocker.patch("firebase_admin.auth.list_users", return_value=LISTA)

    RES = await ver_datos_usuarios("firebase_app", "es", {})

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"usuarios":[{"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","rol":0,"estado":true,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"},{"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","rol":0,"estado":true,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"}]}'

    FIREBASE.assert_called_once_with(app="firebase_app")

@pytest.mark.asyncio
async def test_28(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" maneje correctamente las excepciones.
    """
    TEXTOS = {"es": {"errObtenerDatosUsuarios": "Error al obtener los datos de los usuarios"}}
    FIREBASE = mocker.patch("firebase_admin.auth.list_users")
    FIREBASE.side_effect = Exception("Error al obtener los usuarios")

    RES = await ver_datos_usuarios("firebase_app", "es", TEXTOS)

    assert RES.status_code == 400
    assert RES.body.decode("utf-8") == '{"error":"Error al obtener los datos de los usuarios: Error al obtener los usuarios"}'

    FIREBASE.assert_called_once_with(app="firebase_app")

@pytest.mark.asyncio
async def test_39(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuario" retorne los datos de un usuario.
    """
    USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
    METADATOS = mocker.MagicMock(spec=UserMetadata)

    METADATOS.creation_timestamp = 1753549006090
    METADATOS.last_refresh_timestamp = 1753549008090

    USUARIO.email = "usuario@correo.com"
    USUARIO.uid = "12345"
    USUARIO.display_name = "usuario"
    USUARIO.user_metadata =  METADATOS
    USUARIO.disabled = False

    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_rol_usuario")
    FIRESTORE.return_value = 0

    FIREBASE = mocker.patch("firebase_admin.auth.get_user", return_value=USUARIO)

    RES = await ver_datos_usuario("firebase_app", "12345", "es", {})

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","rol":0,"estado":true,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"}'

    FIREBASE.assert_called_once_with("12345", "firebase_app")
    FIRESTORE.assert_called_once()

@pytest.mark.asyncio
async def test_40(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuario" arroje una excepción al no
    encontrar el usuario.
    """
    TEXTOS = {"es": {"errUsuarioNoEncontrado": "Usuario no encontrado"}}
    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_rol_usuario")
    FIRESTORE.return_value = -1

    FIREBASE = mocker.patch("firebase_admin.auth.get_user", return_value=None)

    RES = await ver_datos_usuario("firebase_app", "a1234H", "es", TEXTOS)

    assert RES.status_code == 404
    assert RES.body.decode("utf-8") == '{"error":"Usuario no encontrado"}'

    FIRESTORE.assert_called_once_with("a1234H")
    FIREBASE.assert_called_once_with("a1234H", "firebase_app")

@pytest.mark.asyncio
async def test_41(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuario" maneje correctamente las excepciones.
    """
    TEXTOS = {"es": {"errObtenerDatosUsuarios": "Error al obtener los datos de los usuarios"}}
    FIRESTORE = mocker.patch("app.apis.FirebaseAuth.obtener_rol_usuario")
    FIRESTORE.side_effect = Exception("a1234H")

    mocker.patch("firebase_admin.auth.get_user", return_value=None)

    RES = await ver_datos_usuario("firebase_app", "a1234H", "es", TEXTOS)

    assert RES.status_code == 400
    assert RES.body.decode("utf-8") == '{"error":"Error al obtener los datos de los usuarios: a1234H"}'

def test_47(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" retorne los datos de un usuario existente.
    """

    USUARIO = mocker.MagicMock(spec=UserRecord)
    USUARIO.uid = "12345"
    USUARIO.disabled = False
    USUARIO.email = "correo@correo.com"

    FIREBASE = mocker.patch("firebase_admin.auth.get_user", return_value=USUARIO)

    RES = ver_usuario_firebase("firebase_app", "12345")

    assert RES == (1, USUARIO)

    FIREBASE.assert_called_once_with("12345", "firebase_app")

def test_48(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" no retorne los datos de un
    usuario que no existe.
    """
    FIREBASE = mocker.patch("firebase_admin.auth.get_user")
    FIREBASE.side_effect = UserNotFoundError("Usuario no encontrado")

    RES = ver_usuario_firebase("firebase_app", "a1234H")

    assert RES == (0, None)

    FIREBASE.assert_called_once_with("a1234H", "firebase_app")

def test_49(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" maneje correctamente las excepciones
    """
    FIREBASE = mocker.patch("firebase_admin.auth.get_user")
    FIREBASE.side_effect = Exception("Error inesperado")

    RES = ver_usuario_firebase("firebase_app", "a1234H")

    assert RES == (-1, None)

    FIREBASE.assert_called_once_with("a1234H","firebase_app")

def test_50(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" retorne una JSONResponse indicando que el usuario
    fue actualizado correctamente.
    """
    TEXTOS = {"es": {"msgUsuarioActualizado": "Estado del usuario actualizado correctamente"}}
    FIREBASE = mocker.patch("firebase_admin.auth.update_user")

    RES = actualizar_estado_usuario("firebase_app", "1234", False, "es", TEXTOS)

    assert RES.status_code == 200
    assert RES.body.decode("utf-8") == '{"mensaje":"Estado del usuario actualizado correctamente"}'

    FIREBASE.assert_called_once_with(uid="1234", disabled=False, app="firebase_app")

def test_51(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" retorne un error cuando los valores
    de actualización son inválidos
    """
    TEXTOS = {"es": {"errEstadoInvalido": "Estado inválido"}}
    FIREBASE = mocker.patch("firebase_admin.auth.update_user")
    FIREBASE.side_effect = ValueError("Estado inválido")

    RES = actualizar_estado_usuario("firebase_app", "1234", False, "es", TEXTOS)

    assert RES.status_code == 401
    assert RES.body.decode("utf-8") == '{"error":"Estado inválido"}'

    FIREBASE.assert_called_once_with(uid="1234", disabled=False, app="firebase_app")

def test_52(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" maneje correctamente las excepciones
    """
    TEXTOS = {"es": {"errTry": "Error al procesar la solicitud:"}}
    FIREBASE = mocker.patch("firebase_admin.auth.update_user")
    FIREBASE.side_effect = Exception("Error inesperado")

    RES = actualizar_estado_usuario("firebase_app", "1234", False, "es", TEXTOS)

    assert RES.status_code == 500
    assert RES.body.decode("utf-8") == '{"error":"Error al procesar la solicitud: Error inesperado"}'

    FIREBASE.assert_called_once_with(uid="1234", disabled=False, app="firebase_app")