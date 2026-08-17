import pytest
from apis.FirebaseAuth import *
from fastapi import Request
from firebase_admin.auth import (
    ExpiredIdTokenError,
    CertificateFetchError,
    ListUsersPage,
    ExportedUserRecord,
    UserMetadata,
    UserNotFoundError,
    UserRecord,
)
from firebase_admin.exceptions import FirebaseError
from models.Excepciones import AccesoNoAutorizado, ErrorInterno, UsuarioInexistente
from models.Peticiones import DatosUsuario
from pytest_mock import MockerFixture
from tests.scripts.conftest import MOCK_FIREBASE_APP, MOCK_TEXTOS


@pytest.mark.parametrize(
    "token,respuesta_esperada,arroja_excepcion",
    [
        ("Bearer token_valido", {"uid": "a1234H", "admin": False}, False),
        ("Bearer token_invalido", None, True),
    ],
    ids=["test_11", "test_12"],
)
def test_verificar_token(
    mocker: MockerFixture, token, respuesta_esperada, arroja_excepcion
):
    """
    Test para validar que la función "verificar_token" retorne un error cuando el token
    es inválido y si es válido, retorne la información contenida en este
    """
    VALIDADOR = mocker.patch(
        "apis.FirebaseAuth.validar_txt_token", return_value=not arroja_excepcion
    )
    FIREBASE = mocker.patch("apis.FirebaseAuth.verify_id_token")
    FIREBASE.return_value = None if arroja_excepcion else respuesta_esperada

    if arroja_excepcion:
        with pytest.raises(AccesoNoAutorizado) as exc_info:
            verificar_token(MOCK_FIREBASE_APP, token, MOCK_TEXTOS, "es")
            FIREBASE.assert_not_called()
            assert exc_info.value.mensaje == MOCK_TEXTOS["es"]["errTokenInvalido"]
    else:
        RES = verificar_token(MOCK_FIREBASE_APP, token, MOCK_TEXTOS, "es")
        FIREBASE.assert_called_once_with(
            token.replace("Bearer ", ""), MOCK_FIREBASE_APP, check_revoked=True
        )
        assert RES == respuesta_esperada

    VALIDADOR.assert_called_once_with(token.replace("Bearer ", ""))


@pytest.mark.parametrize(
    "token,respuesta_esperada,arroja_excepcion,excepcion_acceso_autorizado",
    [
        ("token_valido", {"uid": "a1234H", "admin": False}, False, False),
        ("token_invalido", None, True, True),
        ("token_valido", None, True, False),
    ],
    ids=["test_14", "test_15", "test_16"],
)
def test_validar_token(
    mocker: MockerFixture,
    token,
    respuesta_esperada,
    arroja_excepcion,
    excepcion_acceso_autorizado,
):
    """
    Test para validar que la función "validar_token" maneje correctamente un
    error provocado por usar un token expirado/revocado o si ocurre un error inesperado.
    """
    REQ = mocker.MagicMock(spec=Request)
    REQ.headers = {"authorization": "Bearer token_invalido"}
    FIREBASE = mocker.patch("apis.FirebaseAuth.verify_id_token")

    if excepcion_acceso_autorizado:
        FIREBASE.side_effect = ExpiredIdTokenError(
            "Token expirado", "El token está expirado."
        )
    elif arroja_excepcion and (not excepcion_acceso_autorizado):
        FIREBASE.side_effect = CertificateFetchError(
            "Error al obtener el certificado", "No se pudo obtener el certificado."
        )
    else:
        FIREBASE.return_value = respuesta_esperada

    if arroja_excepcion:
        with pytest.raises(
            AccesoNoAutorizado if excepcion_acceso_autorizado else ErrorInterno
        ) as exc_info:
            validar_token(MOCK_FIREBASE_APP, token, MOCK_TEXTOS, "es")
            exc_info.value.mensaje = (
                MOCK_TEXTOS["es"]["errTokenExpirado"]
                if excepcion_acceso_autorizado
                else MOCK_TEXTOS["es"]["errValidarToken"]
            )
    else:
        RES = validar_token(MOCK_FIREBASE_APP, token, MOCK_TEXTOS, "es")
        assert RES == respuesta_esperada

    FIREBASE.assert_called_once_with(token, MOCK_FIREBASE_APP, check_revoked=True)


@pytest.mark.parametrize(
    "respuesta_esperada,arroja_excepcion",
    [
        (
            [
                {
                    "administrador": False,
                    "correo": "usuario@correo.com",
                    "uid": "12345",
                    "nombre": "usuario",
                    "estado": True,
                    "fecha_registro": "26/07/2025 11:56 AM",
                    "ultima_conexion": "26/07/2025 11:56 AM",
                },
                {
                    "administrador": False,
                    "correo": "usuario@correo.com",
                    "uid": "12345",
                    "nombre": "usuario",
                    "estado": True,
                    "fecha_registro": "26/07/2025 11:56 AM",
                    "ultima_conexion": "26/07/2025 11:56 AM",
                }
            ],
            False,
        ),
        (None, True),
    ],
    ids=["test_26", "test_27"],
)
def test_ver_datos_usuarios(
    mocker: MockerFixture, respuesta_esperada, arroja_excepcion
):
    """
    Test para validar que la función "ver_datos_usuarios" retorne los datos de los usuarios o
    arroje una excepción si ocurre algún error.
    """
    mocker.patch(
        "models.Respuestas.convertir_datetime_str", return_value="26/07/2025 11:56 AM"
    )
    FIREBASE = mocker.patch("apis.FirebaseAuth.list_users")

    if arroja_excepcion:
        FIREBASE.side_effect = FirebaseError("error", "error")
        with pytest.raises(ErrorInterno) as exc_info:
            ver_datos_usuarios(MOCK_FIREBASE_APP, MOCK_TEXTOS, "es")
            assert (
                exc_info.value.mensaje == MOCK_TEXTOS["es"]["errObtenerDatosUsuarios"]
            )
    else:
        METADATOS = mocker.MagicMock(spec=UserMetadata)
        METADATOS.creation_timestamp = 1
        METADATOS.last_refresh_timestamp = 1
        USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
        USUARIO.email = "usuario@correo.com"
        USUARIO.uid = "12345"
        USUARIO.display_name = "usuario"
        USUARIO.user_metadata = METADATOS
        USUARIO.disabled = False
        USUARIO.custom_claims = {"admin": False, "eliminado": False}
        LISTA = mocker.MagicMock(spec=ListUsersPage)
        LISTA.users = [USUARIO]
        LISTA.has_next_page = True
        LISTA.get_next_page = lambda: LISTA2
        LISTA2 = mocker.MagicMock(spec=ListUsersPage)
        LISTA2.users = [USUARIO]
        LISTA2.has_next_page = False
        FIREBASE.return_value = LISTA
        RES = ver_datos_usuarios(MOCK_FIREBASE_APP, MOCK_TEXTOS, "es")
        assert RES == respuesta_esperada

    FIREBASE.assert_called_once_with(app=MOCK_FIREBASE_APP)


@pytest.mark.parametrize(
    "respuesta_esperada,arroja_excepcion,excepcion_usuario_inexistente",
    [
        (
            Usuario(
                correo="usuario@correo.com",
                uid="12345",
                nombre="usuario",
                administrador=False,
                estado=True,
                fecha_registro=1753549006090,
                ultima_conexion=1753549006090
            ),
            False,
            False,
        ),
        (None, True, True),
        (None, True, False),
    ],
    ids=["test_39", "test_40", "test_41"],
)
def test_ver_datos_usuario(
    mocker: MockerFixture,
    respuesta_esperada,
    arroja_excepcion,
    excepcion_usuario_inexistente,
):
    """
    Test para validar que la función "ver_datos_usuario" retorne los datos de un usuario.
    """
    mocker.patch(
        "models.Respuestas.convertir_datetime_str", return_value="26/07/2025 11:56 AM"
    )
    FIREBASE = mocker.patch("apis.FirebaseAuth.get_user")

    if arroja_excepcion and (not excepcion_usuario_inexistente):
        FIREBASE.side_effect = FirebaseError("error", "error")
    else:
        METADATOS = mocker.MagicMock(spec=UserMetadata)
        METADATOS.creation_timestamp = 1753549006090
        METADATOS.last_refresh_timestamp = 1753549008090
        USUARIO = mocker.MagicMock(spec=ExportedUserRecord)
        USUARIO.email = "usuario@correo.com"
        USUARIO.uid = "12345"
        USUARIO.display_name = "usuario"
        USUARIO.user_metadata = METADATOS
        USUARIO.disabled = False
        USUARIO.custom_claims = {
            "admin": False,
            "eliminado": excepcion_usuario_inexistente,
        }
        FIREBASE.return_value = USUARIO

    if arroja_excepcion:
        with pytest.raises(
            UsuarioInexistente if excepcion_usuario_inexistente else ErrorInterno
        ) as exc_info:
            ver_datos_usuario(MOCK_FIREBASE_APP, "a12345H", MOCK_TEXTOS, "es")
            assert (not excepcion_usuario_inexistente) or (
                exc_info.value.mensaje == MOCK_TEXTOS["es"]["errObtenerUsuario"]
            )

    else:
        RES = ver_datos_usuario(MOCK_FIREBASE_APP, "a12345H", MOCK_TEXTOS, "es")
        assert RES == respuesta_esperada

    FIREBASE.assert_called_once_with("a12345H", MOCK_FIREBASE_APP)


@pytest.mark.parametrize(
    "respuesta_esperada,arroja_excepcion,excepcion_usuario_inexistente",
    [
        (
            Usuario(
                correo="correo@correo.com",
                uid="a1234H",
                nombre="usuario",
                administrador=False,
                estado=True,
                fecha_registro=175354900609,
                ultima_conexion=175354900809,
            ),
            False,
            False,
        ),
        (None, True, True),
        (None, True, False),
    ],
    ids=["test_50", "test_51", "test_52"],
)
def test_actualizar_datos_usuario(
    mocker: MockerFixture,
    respuesta_esperada,
    arroja_excepcion,
    excepcion_usuario_inexistente,
):
    """
    Test para validar que la función "actualizar_estado_usuario" actualice los datos de un usuario correctamente o arroje
    el error correspondiente en caso de presentarse alguna excepción.
    """
    FIREBASE = mocker.patch("apis.FirebaseAuth.update_user")
    INST = DatosUsuario(desactivar=True, administrador=False, eliminado=False)
    if arroja_excepcion:
        FIREBASE.side_effect = (
            UserNotFoundError("error", "error")
            if excepcion_usuario_inexistente
            else FirebaseError("error", "error")
        )
        with pytest.raises(
            UsuarioInexistente if excepcion_usuario_inexistente else ErrorInterno
        ) as exc_info:
            RES = actualizar_datos_usuario(
                MOCK_FIREBASE_APP, "a1234H", INST, MOCK_TEXTOS, "es"
            )
            assert (not excepcion_usuario_inexistente) or (
                exc_info.value.mensaje == MOCK_TEXTOS["es"]["errActualizarUsuario"]
            )
    else:
        METADATOS = mocker.MagicMock(spec=UserMetadata)
        METADATOS.creation_timestamp = 175354900609
        METADATOS.last_refresh_timestamp = 175354900809
        USUARIO = mocker.MagicMock(spec=UserRecord)
        USUARIO.uid = "a1234H"
        USUARIO.disabled = False
        USUARIO.email = "correo@correo.com"
        USUARIO.display_name = "usuario"
        USUARIO.custom_claims = {"admin": False, "eliminado": False}
        USUARIO.user_metadata = METADATOS
        FIREBASE.return_value = USUARIO
        RES = actualizar_datos_usuario(
            MOCK_FIREBASE_APP, "a1234H", INST, MOCK_TEXTOS, "es"
        )
        assert RES == respuesta_esperada

    FIREBASE.assert_called_once_with(
        uid="a1234H",
        disabled=INST.desactivar,
        app=MOCK_FIREBASE_APP,
        custom_claims={"admin": INST.administrador, "eliminado": INST.eliminado},
    )


@pytest.mark.parametrize(
    "respuesta_esperada,arroja_excepcion,excepcion_usuario_inexistente",
    [(1, False, False), (None, True, True), (None, True, False)],
    ids=["test_92", "test_93", "test_94"],
)
def test_registrar_usuario_firebase(
    mocker: MockerFixture,
    respuesta_esperada,
    arroja_excepcion,
    excepcion_usuario_inexistente,
):
    """
    Test para validar que la función "establecer_rol_usuario" asigne correctamente el
    rol de un usuario recién registrado en las reclamaciones personalizadas de un usuario en Firebase Auth
    """
    FIREBASE = mocker.patch("apis.FirebaseAuth.set_custom_user_claims")

    if arroja_excepcion:
        FIREBASE.side_effect = (
            UserNotFoundError("error", "error")
            if excepcion_usuario_inexistente
            else FirebaseError("error", "error")
        )
        with pytest.raises(
            UsuarioInexistente if excepcion_usuario_inexistente else ErrorInterno
        ) as exc_info:
            RES = registrar_usuario_firebase(
                MOCK_FIREBASE_APP, "a1234h", MOCK_TEXTOS, "es"
            )
            assert (not excepcion_usuario_inexistente) or (
                exc_info.value.mensaje == MOCK_TEXTOS["es"]["errAsignarRol"]
            )
    else:
        FIREBASE.return_value = None
        RES = registrar_usuario_firebase(MOCK_FIREBASE_APP, "a1234h", MOCK_TEXTOS, "es")
        assert RES == respuesta_esperada

    FIREBASE.assert_called_once_with(
        "a1234h", {"admin": False, "eliminado": False}, app=MOCK_FIREBASE_APP
    )
