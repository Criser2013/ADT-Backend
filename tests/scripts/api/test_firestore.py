from pytest_mock import MockerFixture
import pytest
from app.apis.Firestore import verificar_rol_usuario
from google.cloud.firestore_v1 import AsyncClient, AsyncDocumentReference, DocumentSnapshot

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