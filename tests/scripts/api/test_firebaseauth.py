from pytest_mock import MockerFixture
from fastapi import Request
import pytest
from app.apis.FirebaseAuth import *
from firebase_admin.auth import ExpiredIdTokenError, CertificateFetchError, ListUsersPage, ExportedUserRecord, UserMetadata, UserNotFoundError
from app.models.Peticiones import UsuarioActualizar

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
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=False)
    RES = await verificar_token("firebase_app", "Bearer token_invalido")

    assert RES == 0

    VALIDADOR.assert_called_once_with("token_invalido")

@pytest.mark.asyncio
async def test_12(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" retorne un error cuando ocurre
    una excepción al procesar la solicitud
    """
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token", return_value=-1)
    RES = await verificar_token("firebase_app", "Bearer token_invalido")

    assert RES == -1

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

@pytest.mark.asyncio
async def test_13(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_token" maneje correctamente los
    errores inesperados al validar el token de Firebase.
    """
    VALIDADOR = mocker.patch("app.apis.FirebaseAuth.validar_txt_token", return_value=True)
    FIREBASE_VAL = mocker.patch("app.apis.FirebaseAuth.validar_token")
    FIREBASE_VAL.side_effect = Exception("Excepción imprevista")

    RES = await verificar_token("firebase_app", "Bearer token_invalido")

    assert RES == -1

    VALIDADOR.assert_called_once_with("token_invalido")
    FIREBASE_VAL.assert_called_once_with("token_invalido", "firebase_app", False)

def test_14(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.verify_id_token")
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

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.verify_id_token")
    FIREBASE.side_effect = CertificateFetchError("Error al obtener el certificado", "No se pudo obtener el certificado.")

    RES = validar_token("token_invalido", "firebase_app", False)

    assert RES == -1
    FIREBASE.assert_called_once_with("token_invalido", "firebase_app", check_revoked=True)

def test_22(mocker: MockerFixture):
    """
    Test para validar que la función "validar_token" retorne los datos del token cuando este
    es válido
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.verify_id_token", return_value={ "uid": "a1234H" })

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
    USUARIO.custom_claims = { "admin": False, "eliminado": False }

    LISTA.users = [USUARIO]
    LISTA.has_next_page = False

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.list_users", return_value=LISTA)

    RES = await ver_datos_usuarios("firebase_app")
    USUARIOS = [{"administrador": False,"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","estado":True,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"}]

    assert RES == (1, USUARIOS)

    FIREBASE.assert_called_once_with(app="firebase_app")

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
    USUARIO.custom_claims = { "admin": False, "eliminado": False }

    LISTA2.users = [USUARIO]
    LISTA2.has_next_page = False

    LISTA.users = [USUARIO]
    LISTA.has_next_page = True
    LISTA.get_next_page.side_effect = lambda: LISTA2

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.list_users", return_value=LISTA)
    USUARIOS = [
        {"administrador": False,"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","estado":True,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"},{"administrador": False,"correo":"usuario@correo.com","uid":"12345","nombre":"usuario","estado":True,"fecha_registro":"26/07/2025 11:56 AM","ultima_conexion":"26/07/2025 11:56 AM"}
    ]
    RES = await ver_datos_usuarios("firebase_app")

    assert RES == (1, USUARIOS)

    FIREBASE.assert_called_once_with(app="firebase_app")

@pytest.mark.asyncio
async def test_28(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuarios" maneje correctamente las excepciones.
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.list_users")
    FIREBASE.side_effect = Exception("Error al obtener los usuarios")
    RES = await ver_datos_usuarios("firebase_app")

    assert RES == (-1, None)

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
    USUARIO.custom_claims = { "admin": False, "eliminado": False }

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user", return_value=USUARIO)

    RES = await ver_datos_usuario("firebase_app", "12345")

    assert RES == (1, {"correo": "usuario@correo.com", "uid": "12345", "nombre": "usuario", "administrador": False, "estado": True, "fecha_registro": "26/07/2025 11:56 AM", "ultima_conexion": "26/07/2025 11:56 AM"})

    FIREBASE.assert_called_once_with("12345", "firebase_app")

@pytest.mark.asyncio
async def test_40(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuario" arroje una excepción al no
    encontrar el usuario.
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user")
    FIREBASE.side_effect = UserNotFoundError("Usuario no encontrado")

    RES = await ver_datos_usuario("firebase_app", "a1234H")

    assert RES == (0, None)

    FIREBASE.assert_called_once_with("a1234H", "firebase_app")

@pytest.mark.asyncio
async def test_41(mocker: MockerFixture):
    """
    Test para validar que la función "ver_datos_usuario" maneje correctamente las excepciones.
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user")
    FIREBASE.side_effect = Exception("Error inesperado")

    RES = await ver_datos_usuario("firebase_app", "a1234H")

    assert RES == (-1, None)

    FIREBASE.assert_called_once_with("a1234H", "firebase_app")

def test_47(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" retorne los datos de un usuario existente.
    """
    USUARIO = mocker.MagicMock(spec=UserRecord)
    USUARIO.uid = "12345"
    USUARIO.disabled = False
    USUARIO.email = "correo@correo.com"
    USUARIO.custom_claims = { "admin": False }

    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user", return_value=USUARIO)

    RES = ver_usuario_firebase("firebase_app", "12345")

    assert RES == (1, USUARIO)

    FIREBASE.assert_called_once_with("12345", "firebase_app")

def test_48(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" no retorne los datos de un
    usuario que no existe.
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user")
    FIREBASE.side_effect = UserNotFoundError("Usuario no encontrado")

    RES = ver_usuario_firebase("firebase_app", "a1234H")

    assert RES == (0, None)

    FIREBASE.assert_called_once_with("a1234H", "firebase_app")

def test_49(mocker: MockerFixture):
    """
    Test para validar que la función "ver_usuario_firebase" maneje correctamente las excepciones
    """
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.get_user")
    FIREBASE.side_effect = Exception("Error inesperado")

    RES = ver_usuario_firebase("firebase_app", "a1234H")

    assert RES == (-1, None)

    FIREBASE.assert_called_once_with("a1234H","firebase_app")

def test_50(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" retorne una JSONResponse indicando que el usuario
    fue actualizado correctamente.
    """
    USUARIO = mocker.MagicMock(spec=UserRecord)
    USUARIO.uid = "1234"
    USUARIO.disabled = False
    USUARIO.email = "correo@correo.com"
    USUARIO.display_name = "usuario"
    USUARIO.custom_claims = { "admin": False }

    METADATOS = mocker.MagicMock(spec=UserMetadata)
    METADATOS.creation_timestamp = 175354900609
    METADATOS.last_refresh_timestamp = 175354900809
    USUARIO.user_metadata = METADATOS

    INST = UsuarioActualizar(desactivar=True, administrador=False, eliminado=False)

    INSTANCIA = {"correo": "correo@correo.com", "uid": "1234", "nombre": "usuario", "administrador": False, "estado": True, "fecha_registro": "23/07/1975 08:41 AM", "ultima_conexion": "23/07/1975 08:41 AM"}
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.update_user", return_value=USUARIO)
    RES = actualizar_estado_usuario("firebase_app", "1234", INST)

    assert RES == (1, INSTANCIA)

    FIREBASE.assert_called_once_with(uid="1234", disabled=True, app="firebase_app", custom_claims={"admin": False, "eliminado": False})

def test_51(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" retorne un error cuando el UID
    proveído no corresponde a un usuario existente.
    """
    INST = UsuarioActualizar(desactivar=False, administrador=False, eliminado=False)
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.update_user")
    FIREBASE.side_effect = UserNotFoundError("Estado inválido")
    RES = actualizar_estado_usuario("firebase_app", "1234", INST)

    assert RES == (0, None)

    FIREBASE.assert_called_once_with(uid="1234", disabled=False, app="firebase_app", custom_claims={"admin": False, "eliminado": False})

def test_52(mocker: MockerFixture):
    """
    Test para validar que la función "actualizar_estado_usuario" maneje correctamente las excepciones
    """
    INST = UsuarioActualizar(desactivar=False, administrador=False, eliminado=False)
    FIREBASE = mocker.patch("app.apis.FirebaseAuth.update_user")
    FIREBASE.side_effect = Exception("Error inesperado")
    RES = actualizar_estado_usuario("firebase_app", "1234", INST)

    assert RES == (-1, "Error inesperado")

    FIREBASE.assert_called_once_with(uid="1234", disabled=False, app="firebase_app", custom_claims={"admin": False, "eliminado": False})