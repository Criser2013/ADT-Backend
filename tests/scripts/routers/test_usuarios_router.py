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
    USUARIO.return_value = JSONResponse(
        status_code=200, media_type="application/json", content={"usuarios": DATOS}
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


def test_33(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el usuario no
    es administrador.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")

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

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error inesperado"}

    DATOS_TOKEN.assert_called_once()


def test_42(mocker: MockerFixture):
    """
    Test para validar que el API retorne los datos de un usuario con una petición
    autenticada.
    """
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
    USUARIO.return_value = JSONResponse(
        status_code=200, media_type="application/json", content=DATOS
    )

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

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")
    USUARIO.assert_called_once_with(
        {
            "appId": "test_app_id",
            "cred": {"projectId": "test_project_id", "certificated": True},
        },
        "a1234H",
        "es",
        MOCK_TEXTOS,
    )


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


def test_44(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si ocurre una excepción.
    """

    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")
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

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error inesperado"}

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
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.ver_datos_token",
        return_value=(1, {"uid": "a1234H"}),
    )
    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    mocker.patch("routers.usuarios_router.validar_uid", return_value=True)

    USUARIO = mocker.MagicMock(spec=UserRecord)
    USUARIO.uid = "a1234H"

    FIRESTORE = mocker.patch("routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (1, USUARIO)

    ACT = mocker.patch(
        "routers.usuarios_router.actualizar_estado_usuario",
    )
    ACT.return_value = JSONResponse(
        {"mensaje": "Estado del usuario actualizado correctamente"},
        status_code=200,
        media_type="application/json",
    )

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
    assert RES.json() == {"mensaje": "Estado del usuario actualizado correctamente"}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("a1234H")
    FIRESTORE.assert_called_once_with(
        {
            "appId": "test_app_id",
            "cred": {"projectId": "test_project_id", "certificated": True},
        },
        "a1234H",
    )


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
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (1, {"uid": "a1234H"})

    FIRESTORE = mocker.patch("routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (0, None)

    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    FUNC = mocker.patch("routers.usuarios_router.actualizar_estado_usuario")

    mocker.patch("routers.usuarios_router.validar_uid", return_value=True)
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
    DATOS_TOKEN.assert_called_once()
    FUNC.assert_not_called()


def test_63(mocker: MockerFixture):
    """
    Test para validar que el API no actualice los datos de un usuario si ocurre una excepción.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (1, {"uid": "a1234H"})

    FIRESTORE = mocker.patch("routers.usuarios_router.ver_usuario_firebase")
    FIRESTORE.return_value = (-1, None)

    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )

    FUNC = mocker.patch("routers.usuarios_router.actualizar_estado_usuario")
    mocker.patch("routers.usuarios_router.validar_uid", return_value=True)
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

    assert RES.status_code == 500
    assert RES.json() == {
        "error": "Error al procesar la solicitud: Error al obtener el usuario"
    }

    FUNC.assert_not_called()
    ROL.assert_called_once()


def test_64(mocker: MockerFixture):
    """
    Test para validar que actualice los datos de un usuario si se lanza un ValueError.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.return_value = (1, {"uid": "a1234H"})

    ROL = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_rol_usuario", return_value=True
    )
    mocker.patch("routers.usuarios_router.validar_uid", return_value=False)
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


def test_65(mocker: MockerFixture):
    """
    Test para validar que actualice los datos de un usuario si se lanza un ValueError.
    """
    DATOS_TOKEN = mocker.patch("dependencies.usuarios_dependencies.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")

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

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error inesperado"}

    FUNC.assert_not_called()
