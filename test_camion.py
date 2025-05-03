import pytest
from unittest.mock import patch
from modules.camion import Camion

@pytest.fixture
def camion_ejemplo():
    camion = Camion()
    camion.gms = {
        "lat": (40.0, 25.0, 10.5, 'N'),
        "long": (3.0, 42.0, 20.3, 'W')
    }
    return camion

@pytest.mark.asyncio
async def test_update_basico(camion_ejemplo):
    """Prueba el funcionamiento básico de update()"""
    with patch('random.normalvariate') as norm, patch('random.uniform') as unif, patch('random.choices') as choices:

        #Side_effect es para fijar valores de retorno
        norm.side_effect = [
            40.0, 25.0, 10.5,
            3.0, 42.0, 20.3,
            21.0
        ]
        unif.return_value = 87.5
        choices.side_effect = [['N'], ['W']]

        await camion_ejemplo.update()

        # Verificaciones
        assert len(camion_ejemplo.temperaturas) == 1
        assert camion_ejemplo.temperaturas[0] == 21.0
        assert len(camion_ejemplo.humedades) == 1
        assert camion_ejemplo.humedades[0] == 87.5
        assert camion_ejemplo._contador == 1