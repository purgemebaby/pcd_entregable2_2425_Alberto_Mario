from openlocationcode import openlocationcode as olc  # Corrección en la importación
from modules.camion import Camion
from typing import Optional, Tuple

class CamionAdapter:
    def __init__(self, camion: Camion):
        self.camion = camion

    def gms_a_decimal(self, grados: int, minutos: int, segundos: float, direccion: str) -> float:
        """
        Convierte GMS (grados, minutos, segundos) a decimal.
        """
        decimal = grados + minutos / 60 + segundos / 3600
        if direccion in ['S', 'W']:
            decimal *= -1
        return decimal
    
    def gms_a_olc(self) -> str:
        """
        Convierte las coordenadas GMS del camión a código OLC.
        """
        lat_gms = self.camion.gms["lat"]
        lon_gms = self.camion.gms["long"]
        
        if lat_gms is None or lon_gms is None:
            raise ValueError("Coordenadas no definidas en el camión.")
        
        if not (isinstance(lat_gms, tuple) and len(lat_gms) == 4 and
                isinstance(lon_gms, tuple) and len(lon_gms) == 4):
            raise ValueError("Formato de coordenadas GMS inválido")
        
        lat_decimal = self.gms_a_decimal(*lat_gms)
        lon_decimal = self.gms_a_decimal(*lon_gms)
        
        return olc.encode(lat_decimal, lon_decimal) # e.g. '7FG9V+2C Madrid, España'

