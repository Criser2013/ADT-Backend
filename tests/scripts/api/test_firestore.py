from pytest_mock import MockerFixture
import pytest
from app.apis.Firestore import *
from google.cloud.firestore_v1 import AsyncClient, AsyncDocumentReference, DocumentSnapshot, AsyncCollectionReference
import asyncio

@pytest.mark.asyncio
async def test_31(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_rol_usuario" retorne True si el usuario
    es administrador.
    """
    DOCUMENTO = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO.to_dict.return_value = {"rol": 1001}

    REF = mocker.MagicMock(spec=AsyncDocumentReference)
    REF.get.return_value = DOCUMENTO

    CLIENTE = mocker.MagicMock(spec=AsyncClient)
    CLIENTE.document.return_value = REF

    FIREBASE = mocker.patch("firebase_admin.firestore_async.client",return_value=CLIENTE)

    RES = await verificar_rol_usuario("usuario@correo.com")

    assert RES == True

    FIREBASE.assert_called_once()

@pytest.mark.asyncio
async def test_32(mocker: MockerFixture):
    """
    Test para validar que la función "verificar_rol_usuario" retorne False si el usuario
    no es administrador.
    """
    DOCUMENTO = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO.to_dict.return_value = {"rol": 0}

    REF = mocker.MagicMock(spec=AsyncDocumentReference)
    REF.get.return_value = DOCUMENTO

    CLIENTE = mocker.MagicMock(spec=AsyncClient)
    CLIENTE.document.return_value = REF

    FIREBASE = mocker.patch("firebase_admin.firestore_async.client",return_value=CLIENTE)

    RES = await verificar_rol_usuario("usuario@correo.com")

    assert RES == False

    FIREBASE.assert_called_once()

@pytest.mark.asyncio
async def test_38(mocker: MockerFixture):
    """
    Test para validar que la función "obtener_roles_usuarios" retorne los roles de los usuarios.
    """
    DOCUMENTO1 = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO1.to_dict.return_value = {"correo": "usuario@correo.com", "rol": 0}

    DOCUMENTO2 = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO2.to_dict.return_value = {"correo": "usuario2@correo.com", "rol": 1001}

    REF = mocker.MagicMock(spec=AsyncCollectionReference)
    REF.get.return_value = [DOCUMENTO1, DOCUMENTO2]

    CLIENTE = mocker.MagicMock(spec=AsyncClient)
    CLIENTE.collection.return_value = REF

    FIREBASE = mocker.patch("firebase_admin.firestore_async.client",return_value=CLIENTE)

    RES = await obtener_roles_usuarios()

    assert RES == {"usuario@correo.com": 0, "usuario2@correo.com": 1001}

    FIREBASE.assert_called_once()

@pytest.mark.asyncio
async def test_41(mocker: MockerFixture):
    """
    Test para validar que la función "obtener_rol_usuario" retorne el rol de un usuario.
    """
    DOCUMENTO = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO.exists = True
    DOCUMENTO.to_dict.return_value = {"correo": "usuario@correo.com", "rol": 0}

    REF = mocker.MagicMock(spec=AsyncCollectionReference)
    REF.get.return_value = DOCUMENTO

    CLIENTE = mocker.MagicMock(spec=AsyncClient)
    CLIENTE.document.return_value = REF

    FIREBASE = mocker.patch("firebase_admin.firestore_async.client",return_value=CLIENTE)

    RES = await obtener_rol_usuario("usuario@correo.com")

    assert RES == 0

    FIREBASE.assert_called_once()

@pytest.mark.asyncio
async def test_42(mocker: MockerFixture):
    """
    Test para validar que la función "obtener_rol_usuario" retorne -1 cuando el usuario no existe.
    """
    DOCUMENTO = mocker.MagicMock(spec=DocumentSnapshot)
    DOCUMENTO.exists = False
    DOCUMENTO.to_dict.return_value = {"correo": "usuario1@correo.com", "rol": 0}

    REF = mocker.MagicMock(spec=AsyncCollectionReference)
    REF.get.return_value = DOCUMENTO


    CLIENTE = mocker.MagicMock(spec=AsyncClient)
    CLIENTE.document.return_value = REF

    FIREBASE = mocker.patch("firebase_admin.firestore_async.client",return_value=CLIENTE)

    RES = await obtener_rol_usuario("usuario@correo.com")

    assert RES == -1

    FIREBASE.assert_called_once()