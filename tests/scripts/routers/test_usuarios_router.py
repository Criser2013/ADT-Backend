from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from firebase_admin.auth import UserRecord
from app.main import app
import pytest
from contextlib import asynccontextmanager

# Constantes de prueba
TEST_CREDS = {
    "apiKey": "test_api_key",
    "authDomain": "test_auth_domain",
    "projectId": "test_project_id",
    "storageBucket": "test_storage_bucket",
    "messagingSenderId": "test_messaging_sender_id",
    "appId": "test_app_id",
    "measurementId": "test_measurement_id",
    "driveScopes": [
        "https://www.googleapis.com/auth/drive",
    ],
}

MOCK_FIREBASE_APP = {
    "appId": "test_app_id",
    "cred": {"projectId": "test_project_id", "certificated": True},
}

MOCK_TEXTOS = {
    "es": {
        "errTry": "Error al procesar la solicitud:",
        "errAccesoDenegado": "Acceso denegado.",
        "errTokenInvalido": "Token inválido",
        "errUIDInvalido": "UID inválido",
        "errObtenerUsuario": "Error al obtener el usuario",
        "errUsuarioNoEncontrado": "Usuario no encontrado",
    }
}


@asynccontextmanager
async def mock_inicializar_modelos(app):
    yield {
        "explicador": None,  # Mock del explicador
        "textos": MOCK_TEXTOS,
        "modelo": None,  # Mock del modelo
        "firebase_app": MOCK_FIREBASE_APP,
        "credenciales": TEST_CREDS,
    }


@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    mocker.patch(
        "app.main.CORS_ORIGINS",
        [
            "http://localhost:5178",
        ],
    )
    mocker.patch(
        "app.main.ALLOWED_HOSTS",
        [
            "localhost",
        ],
    )
    mocker.patch("app.main.ORIGENES_AUTORIZADOS", ["*"])
    yield
    mocker.resetall()


def test_31(mocker: MockerFixture):
    """
    Test para validar que el API retorne los datos de los usuarios con una petición
    autenticada.
    """
    DATOS = [
        {
            "correo": "usuario@correo.com",
            "uid": "a1234H",
            "nombre": "usuario",
            "ultima_conexion": 1000,
            "rol": 0,
            "estado": True,
        }
    ]
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )

    USUARIO = mocker.patch("routers.usuarios_router.ver_datos_usuarios")
    USUARIO.return_value = (1, DATOS)
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 200
    assert RES.json() == {"usuarios": DATOS}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")
    USUARIO.assert_called_once()


def test_32(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el usuario no
    es administrador.
    """
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=False
    )

    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Acceso denegado."}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")


def test_42(mocker: MockerFixture):
    """
    Test para validar que el API retorne los datos de un usuario con una petición
    autenticada.
    """
    UID = mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value="a1234H")
    DATOS = {
        "correo": "usuario@correo.com",
        "uid": "a1234H",
        "nombre": "usuario",
        "ultima_conexion": 1000,
        "rol": 0,
        "estado": True,
    }
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    mocker.patch("routers.usuarios_router.validar_uid", return_value=True)

    app.router.lifespan_context = mock_inicializar_modelos

    USUARIO = mocker.patch("routers.usuarios_router.ver_datos_usuario")
    USUARIO.return_value = (1, DATOS)

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
                "Language": "es",
            },
        )

    assert RES.status_code == 200
    assert RES.json() == DATOS

    UID.assert_called_once_with("a1234H")
    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")
    USUARIO.assert_called_once_with(MOCK_FIREBASE_APP, "a1234H")


def test_43(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos del usuario si el token es inválido.
    """
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(0, {"error": "Token inválido"}),
    )
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_invalido",
            },
        )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Token inválido"}

    DATOS_TOKEN.assert_called_once()

def test_45(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de un usuario con un
    UID inválido
    """
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    mocker.patch("routers.usuarios_router.validar_uid", return_value=False)
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 400
    assert RES.json() == {"error": "UID inválido"}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")


def test_46(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de un usuario si se lanza un ValueError.
    """
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    MOCK = mocker.patch("routers.usuarios_router.validar_uid")
    MOCK.side_effect = ValueError("UID inválido")
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 400
    assert RES.json() == {"error": "UID inválido"}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")


def test_60(mocker: MockerFixture):
    """
    Test para validar que el API actualice el estado de un usuario correctamente.
    """
    MOCK_USUARIO = {
        "correo" : "correo@correo.com", "uid" : "a1234H",
        "nombre": "correo", "estado": False,
        "fecha_registro": "12/12/2025 4:00 PM",
        "ultima_conexion": "12/12/2025 4:00 PM",
    }
    UID = mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value="a1234H")
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )

    USUARIO = mocker.MagicMock(spec=UserRecord)
    USUARIO.uid = "a1234H"

    FIRESTORE = mocker.patch("routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (1, USUARIO)

    ACT = mocker.patch(
        "routers.usuarios_router.actualizar_estado_usuario",
    )
    ACT.return_value = (1, MOCK_USUARIO)

    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H?desactivar=false",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 200
    assert RES.json() == MOCK_USUARIO

    DATOS_TOKEN.assert_called_once()
    UID.assert_called_once_with("a1234H")
    ROL.assert_called_once_with("a1234H")
    FIRESTORE.assert_called_once_with(MOCK_FIREBASE_APP, "a1234H")


def test_61(mocker: MockerFixture):
    """
    Test para validar que el API no actualice el estado del usuario si el token es inválido.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (0, {"error": "Token inválido"})

    FUNC = mocker.patch("routers.usuarios_router.actualizar_estado_usuario")
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H?desactivar=true",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_invalido",
            },
        )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Token inválido"}

    DATOS_TOKEN.assert_called_once()
    FUNC.assert_not_called()


def test_62(mocker: MockerFixture):
    """
    Test para validar que el API retorne un error al intentar actualizar el estado de un
    usuario inexistente.
    """
    UID = mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value="a1234H")
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (1, {"uid": "a1234H"})

    FIRESTORE = mocker.patch("routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (0, None)

    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    FUNC = mocker.patch("routers.usuarios_router.actualizar_estado_usuario")
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H?desactivar=true",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 404
    assert RES.json() == {"error": "Usuario no encontrado"}

    ROL.assert_called_once()
    UID.assert_called_once_with("a1234H")
    DATOS_TOKEN.assert_called_once()
    FUNC.assert_not_called()


def test_63(mocker: MockerFixture):
    """
    Test para validar que el API no actualice los datos de un usuario si ocurre una excepción.
    """
    UID = mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value="a1234H")
    TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token", return_value=(1, {"uid": "a1234H"}))
    ROL = mocker.patch("dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True)

    FIRESTORE = mocker.patch("app.routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (-1, None)

    FUNC = mocker.patch("app.routers.usuarios_router.actualizar_estado_usuario")
    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H?desactivar=true",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 400
    assert RES.json() == {
        "error": "Error al obtener el usuario"
    }

    ROL.assert_called_once()
    FUNC.assert_not_called()
    UID.assert_called_once()
    TOKEN.assert_called_once()


def test_64(mocker: MockerFixture):
    """
    Test para validar que no actualice los datos de un usuario si se lanza un ValueError.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (1, {"uid": "a1234H"})

    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    mocker.patch("dependencies.usuarios_dependencies.validar_uid", return_value=False)
    FUNC = mocker.patch("app.routers.usuarios_router.actualizar_estado_usuario")

    app.router.lifespan_context = mock_inicializar_modelos

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H?desactivar=true",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )

    assert RES.status_code == 400
    assert RES.json() == {"error": "UID inválido"}

    FUNC.assert_not_called()
    ROL.assert_called_once_with("a1234H")

# test_65,44,57 - libre