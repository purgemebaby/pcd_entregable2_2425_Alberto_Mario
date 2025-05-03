import pytest # type: ignore 
from unittest.mock import MagicMock, patch
from modules.camion import Camion
from modules.logist import CentroLogistico

# Los pytests.fixture son funciones que proporcionan automáticamente dato para usarlos como entrada en los tests
# (en nuestro caso para update)

# pytest.mark.asyncio indica que el test es asíncrono
# Con patch se puede fijar el comportamiento de funciones como si se importasen


@pytest.fixture
def example_CL():
    return CentroLogistico()

@pytest.fixture
def example_camion():
    camion = Camion()
    camion.gms = {
        "lat": (40.0, 25.0, 10.5, 'N'),
        "long": (3.0, 42.0, 20.3, 'W')
    }
    camion.temperaturas = [21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0]
    camion.humedades = [85.0, 85.5, 86.0, 86.5, 87.0, 87.5, 88.0]
    camion.media_actual = {
        "mean_temp": 22.0,
        "mean_hum": 86.0
    }
    camion.desviacion_actual = {
        "std_temp": 1.0,
        "std_hum": 1.0
    }
    return camion

@pytest.mark.asyncio
async def test_update(example_CL, example_camion):
    """Prueba que el centro logístico actualice los datos correctamente"""
    example_CL.add_camion(example_camion)
    adapter_falso = MagicMock()
    adapter_falso.gms_a_olc.return_value = "OLC:ES:40:25:10:N:3:42:20:W"
    example_CL.adapters[example_camion.matricula] = adapter_falso

    # Hemos tenido que fijar el tiempo para evitar problemas con datetime.now()
    time = "03/05/2025 18:00:00"
    with patch('datetime.datetime') as datetime:
        datetime.now.return_value.strftime.return_value = time


        await example_CL.update(example_camion, needed=True)


        # Comprobaciones
        # Medias
        assert len(example_CL.medias[example_camion.matricula]) == 2
        assert example_CL.medias[example_camion.matricula][0] == {
            "mean_temp": 22.0,
            "mean_hum": 86.0
        }
        assert example_CL.medias[example_camion.matricula][1] == time


        # Desviaciones estandar
        assert len(example_CL.std[example_camion.matricula]) == 2
        assert example_CL.std[example_camion.matricula][0] == {
            "std_temp": 1.0,
            "std_hum": 1.0
        }
        assert example_CL.std[example_camion.matricula][1] == time


        # Coordenadas
        assert example_CL.last_ocl[example_camion.matricula] == [
            "OLC:ES:40:25:10:N:3:42:20:W",
            time
        ]
        adapter_falso.gms_a_olc.assert_called_once()

