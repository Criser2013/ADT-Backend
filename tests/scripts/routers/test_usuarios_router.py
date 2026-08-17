import pytest
from fastapi.testclient import TestClient
from main import app
from models.Respuestas import Usuario
from models.Peticiones import DatosUsuario
from pytest_mock import MockerFixture
from tests.scripts.conftest import MOCK_FIREBASE_APP, MOCK_TEXTOS

DATOS = [
    {
        "correo": "usuario@correo.com",
        "uid": "a1234H",
        "nombre": "usuario",
        "fecha_registro": "24/04/2026 12:30 AM",
        "ultima_conexion": "24/04/2026 12:30 AM",
        "administrador": False,
        "estado": True,
    }
]


@pytest.mark.parametrize(
    "respuesta_esperada,mock_ver_usuarios,es_admin",
    [
        ({"status_code": 200, "usuarios": DATOS}, DATOS, True),
        ({"status_code": 403, "error": "Acceso denegado."}, None, False),
    ],
    ids=["test_31", "test_32"],
)
def test_endpoint_usuarios(
    lifespan_mock, mocker: MockerFixture, respuesta_esperada, mock_ver_usuarios, es_admin
):
    """
    Test para validar que el API retorne los datos de los usuarios con una petición
    autenticada.
    """
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": es_admin}),
    )
    USUARIO = mocker.patch(
        "routers.usuarios_router.ver_datos_usuarios", return_value=mock_ver_usuarios
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.get(
            "/admin/usuarios",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
        )
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]
    assert (
        (JSON["usuarios"] == respuesta_esperada["usuarios"])
        if es_admin
        else (JSON["error"] == respuesta_esperada["error"])
    )

    DATOS_TOKEN.assert_called_once_with(
        MOCK_FIREBASE_APP, "Bearer token_valido", MOCK_TEXTOS, "es"
    )

    if es_admin:
        USUARIO.assert_called_once_with(MOCK_FIREBASE_APP, MOCK_TEXTOS, "es")


@pytest.mark.parametrize(
    "respuesta_esperada,mock_ver_usuario,es_admin",
    [
        ({"status_code": 200, "usuario": DATOS[0].copy()}, DATOS[0].copy(), True),
        (
            {"status_code": 403, "error": MOCK_TEXTOS["es"]["errAccesoDenegado"]},
            None,
            False,
        ),
    ],
    ids=["test_42", "test_43"],
)
def test_endpoint_ver_usuario(
    lifespan_mock, mocker: MockerFixture, respuesta_esperada, mock_ver_usuario, es_admin
):
    """
    Test para validar que el API retorne los datos de un usuario con una petición
    autenticada.
    """
    mocker.patch(
        "models.Respuestas.convertir_datetime_str", return_value="24/04/2026 12:30 AM"
    )
    UID = mocker.patch(
        "dependencies.usuarios_dependencies.validar_uid", return_value=True
    )
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": es_admin}),
    )
    FIREBASE = mocker.patch("routers.usuarios_router.ver_datos_usuario")
    FIREBASE.return_value = None if not es_admin else Usuario(**mock_ver_usuario)

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
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]

    if not es_admin:
        assert JSON["error"] == respuesta_esperada["error"]
        FIREBASE.assert_not_called()
    else:
        assert JSON["correo"] == respuesta_esperada["usuario"]["correo"]
        assert JSON["uid"] == respuesta_esperada["usuario"]["uid"]
        assert JSON["nombre"] == respuesta_esperada["usuario"]["nombre"]
        assert JSON["estado"] == respuesta_esperada["usuario"]["estado"]
        assert JSON["administrador"] == respuesta_esperada["usuario"]["administrador"]
        assert JSON["fecha_registro"] == respuesta_esperada["usuario"]["fecha_registro"]
        assert (
            JSON["ultima_conexion"] == respuesta_esperada["usuario"]["ultima_conexion"]
        )
        FIREBASE.assert_called_once_with(MOCK_FIREBASE_APP, "a1234H", MOCK_TEXTOS, "es")
        UID.assert_called_once_with("a1234H")

    DATOS_TOKEN.assert_called_once_with(
        MOCK_FIREBASE_APP, "Bearer token_valido", MOCK_TEXTOS, "es"
    )


@pytest.mark.parametrize(
    "instancia,respuesta_esperada,mock_actualizar,es_admin",
    [
        (
            DatosUsuario(desactivar=False, administrador=False, eliminado=False),
            {
                "status_code": 200,
                "usuario": {
                    "correo": "correo@correo.com",
                    "uid": "a1234H",
                    "estado": True,
                    "nombre": "usuario",
                    "fecha_registro": "31/12/1969 07:00 PM",
                    "ultima_conexion": "31/12/1969 07:00 PM",
                    "administrador": False,
                },
            },
            Usuario(
                nombre="usuario",
                uid="a1234H",
                estado=True,
                correo="correo@correo.com",
                fecha_registro=1,
                ultima_conexion=1,
                administrador=False,
            ),
            True,
        ),
        (
            DatosUsuario(desactivar=False, administrador=False, eliminado=False),
            {"status_code": 403, "error": MOCK_TEXTOS["es"]["errAccesoDenegado"]},
            None,
            False,
        ),
    ],
    ids=["test_60", "test_61"],
)
def test_endpoint_actualizar_usuario(
    lifespan_mock, mocker: MockerFixture, instancia, respuesta_esperada, mock_actualizar, es_admin
):
    """
    Test para validar que el API actualice el estado de un usuario correctamente.
    """
    UID = mocker.patch(
        "dependencies.usuarios_dependencies.validar_uid", return_value="a1234H"
    )
    DATOS_TOKEN = mocker.patch(
        "dependencies.usuarios_dependencies.verificar_token",
        return_value=({"uid": "a1234H", "admin": es_admin}),
    )
    FIREBASE = mocker.patch(
        "routers.usuarios_router.actualizar_datos_usuario", return_value=mock_actualizar
    )

    with TestClient(app) as CLIENTE:
        RES = CLIENTE.patch(
            "/admin/usuarios/a1234H",
            headers={
                "Origin": "http://localhost:5178",
                "Host": "localhost",
                "Authorization": "Bearer token_valido",
            },
            json={"desactivar": False, "administrador": False, "eliminado": False},
        )
        JSON = RES.json()

    assert RES.status_code == respuesta_esperada["status_code"]

    if not es_admin:
        assert JSON["error"] == respuesta_esperada["error"]
        FIREBASE.assert_not_called()
    else:
        assert JSON["correo"] == respuesta_esperada["usuario"]["correo"]
        assert JSON["uid"] == respuesta_esperada["usuario"]["uid"]
        assert JSON["nombre"] == respuesta_esperada["usuario"]["nombre"]
        assert JSON["estado"] == respuesta_esperada["usuario"]["estado"]
        assert JSON["administrador"] == respuesta_esperada["usuario"]["administrador"]
        assert JSON["fecha_registro"] == respuesta_esperada["usuario"]["fecha_registro"]
        assert (
            JSON["ultima_conexion"] == respuesta_esperada["usuario"]["ultima_conexion"]
        )
        UID.assert_called_once_with("a1234H")
        FIREBASE.assert_called_once_with(
            MOCK_FIREBASE_APP, "a1234H", instancia, MOCK_TEXTOS, "es"
        )

    DATOS_TOKEN.assert_called_once_with(
        MOCK_FIREBASE_APP, "Bearer token_valido", MOCK_TEXTOS, "es"
    )
