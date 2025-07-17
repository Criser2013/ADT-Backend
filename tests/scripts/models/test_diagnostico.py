from app.models.Diagnostico import Diagnostico
from numpy import array

def test_7():
    """
    Test para validar que la clase se inicialice correctamente con una instancia de datos
    y cargue el normalizador.
    """
    INSTANCIA =array([
        4,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,9,4,4,4,0,0,0,0,2,4,4,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ])
    OBJ = Diagnostico(INSTANCIA)

    assert OBJ.datos.all() == INSTANCIA.all()
    assert OBJ.datos_normalizados.shape == (0,)
    assert "/app" in str(OBJ.BASE_PATH)
    assert (OBJ.scaler is not None) and (str(type(OBJ.scaler)) == "<class 'sklearn.preprocessing._data.StandardScaler'>")


def test_8():
    """
    Test para validar que el normalizador funcione correctamente.
    """
    INSTANCIA =array([
        4,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,9,4,4,4,0,0,0,0,2,4,4,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ])
    OBJ = Diagnostico(INSTANCIA)
    RES = array([ 
        0.92448059, 1.12870395, -0.13566469, -0.22501758, 2.5584086, 2.2689531,
        0, -0.30348849, -0.69436507, 0.70391441, 0.83299313, -0.26639771,
    -0.17622684, -0.32659863, -0.34874292, -0.5819877, -1.24901253, 1.9045084,
    -0.03366946, 0.06808517, -0.11043153, -0.3805622, -0.25318484, -0.19364917,
    0.95243839, -1.92854697, 0.10621482, -0.42107596, 0.55415396, -0.25318484,
    2.04633819, 3.94968353, -0.34874292, -0.52623481, -0.31517891, -0.11043153,
    1.4401646, -0.33777797, -0.54486237, -0.31517891, -0.11043153, -0.22501758,
    -0.42107596, -0.07784989]).all()

    OBJ.normalizar_datos()
    assert OBJ.datos_normalizados.shape == (1, 44)
    assert OBJ.datos_normalizados.all() == RES

def test_9():
    """
    Test para validar que la clase cargue el modelo y genere un diagnóstico
    correctamente.
    """
    INSTANCIA =array([
        4,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,9,4,4,4,0,0,0,0,2,4,4,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0
        ])
    OBJ = Diagnostico(INSTANCIA)
    RES = OBJ.generar_diagnostico()
    assert {"prediccion": True, "probabilidad": 1.0 } == RES
