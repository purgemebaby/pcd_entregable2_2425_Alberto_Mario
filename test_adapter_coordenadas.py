import pytest
from unittest.mock import patch
from modules.camion import Camion
from modules.adapter_coordenadas import CamionAdapter
from openlocationcode import openlocationcode as olc

@pytest.fixture
def ejemplo_camion():
    camion = Camion()
    camion.gms = {
        "lat": (40.0, 25.0, 10.5, 'N'),
        "long": (3.0, 42.0, 20.3, 'W')
    }
    return camion

@pytest.fixture
def adapter(ejemplo_camion):
    return CamionAdapter(ejemplo_camion)

def test_gms_a_olc_valido(adapter):
    """Prueba conversión de coordenadas GMS a OLC válida"""
    with patch('openlocationcode.openlocationcode.encode') as olc:
        olc.return_value = "8FWC2345+67"
        resultado = adapter.gms_a_olc()
        
        assert resultado == "8FWC2345+67"
        olc.assert_called_once_with(
            pytest.approx(40.419583, 0.000001),
            pytest.approx(-3.705639, 0.000001)
        )


