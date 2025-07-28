from pytest_mock import MockerFixture
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
import app.main
import pytest

@pytest.fixture(autouse=True)
def setup_module(mocker: MockerFixture):
    MOCK_APP = {
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }

    mocker.patch("routers.usuarios_router.firebase_app", MOCK_APP)
    mocker.patch("app.main.CORS_ORIGINS", ["http://localhost:5178",])
    mocker.patch("app.main.ALLOWED_HOSTS", ["localhost",] )
    yield
    mocker.resetall()

def test_33(mocker: MockerFixture):
    """
    Test para validar que el API retorne los datos de los usuarios con una petición
    autenticada.
    """

    DATOS = [{"correo": "usuario@correo.com", "nombre": "usuario", "ultima_conexion": 1000, "rol": 0, "estado": True}]
    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("routers.usuarios_router.verificar_rol_usuario", return_value=True)

    USUARIO = mocker.patch("routers.usuarios_router.ver_datos_usuarios")
    USUARIO.return_value = JSONResponse(
        status_code=200,
        media_type="application/json",
        content={"usuarios": DATOS}
    )

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 200
    assert RES.json() == {"usuarios": DATOS}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")
    USUARIO.assert_called_once()

def test_34(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el token es inválido.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(0, {"error": "Token inválido"}))

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_invalido"}
    )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Token inválido"}

    DATOS_TOKEN.assert_called_once()

def test_35(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si se produjo un error
    al verificar el token
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(-1, {"error": "Error al validar el token"}))

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_invalido"}
    )

    assert RES.status_code == 400
    assert RES.json() == {"error": "Error al validar el token"}

    DATOS_TOKEN.assert_called_once()

def test_36(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el usuario no
    es administrador.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("routers.usuarios_router.verificar_rol_usuario", return_value=False)

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Acceso denegado."}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")

def test_37(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si el usuario no
    es administrador.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error inesperado"}

    DATOS_TOKEN.assert_called_once()

def test_46(mocker: MockerFixture):
    """
    Test para validar que el API retorne los datos de un usuario con una petición
    autenticada.
    """

    DATOS = {"correo": "usuario@correo.com", "nombre": "usuario", "ultima_conexion": 1000, "rol": 0, "estado": True}
    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("routers.usuarios_router.verificar_rol_usuario", return_value=True)

    USUARIO = mocker.patch("routers.usuarios_router.ver_datos_usuario")
    USUARIO.return_value = JSONResponse(
        status_code=200,
        media_type="application/json",
        content=DATOS
    )

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 200
    assert RES.json() == DATOS

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")
    USUARIO.assert_called_once_with({
        "appId": "test_app_id",
        "cred": {"projectId": "test_project_id", "certificated": True},
    }, "usuario@correo.com")

def test_47(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos del usuario si el token es inválido.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(0, {"error": "Token inválido"}))

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_invalido"}
    )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Token inválido"}

    DATOS_TOKEN.assert_called_once()

def test_48(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de un usuario si se produjo un error
    al verificar el token
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(-1, {"error": "Error al validar el token"}))

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_invalido"}
    )

    assert RES.status_code == 400
    assert RES.json() == {"error": "Error al validar el token"}

    DATOS_TOKEN.assert_called_once()

def test_49(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de un usuario si el usuario no
    es administrador.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("routers.usuarios_router.verificar_rol_usuario", return_value=False)

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 403
    assert RES.json() == {"error": "Acceso denegado."}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")

def test_50(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de los usuarios si ocurre una excepción.
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token")
    DATOS_TOKEN.side_effect = Exception("Error inesperado")

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 500
    assert RES.json() == {"error": "Error al procesar la solicitud: Error inesperado"}

    DATOS_TOKEN.assert_called_once()

def test_51(mocker: MockerFixture):
    """
    Test para validar que el API no retorne los datos de un usuario con un
    correo inválido
    """

    DATOS_TOKEN = mocker.patch("routers.usuarios_router.ver_datos_token", return_value=(1, {"email": "usuario@correo.com"}))
    ROL = mocker.patch("routers.usuarios_router.verificar_rol_usuario", return_value=True)
    mocker.patch("routers.usuarios_router.validar_correo", return_value=False)

    CLIENTE = TestClient(app.main.app)

    RES = CLIENTE.get(
        "/admin/usuarios/usuario%40correo%252Ecom",
        headers={"Origin": "http://localhost:5178", "Host": "localhost",
                 "Authorization": "Bearer token_valido"}
    )

    assert RES.status_code == 400
    assert RES.json() == {"error": "Correo inválido"}

    DATOS_TOKEN.assert_called_once()
    ROL.assert_called_once_with("usuario@correo.com")