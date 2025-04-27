from modules.camion import Camion
from typing import Optional, Tuple
from openlocationcode import openlocationcode as olc #Es una librería externa, hay que descargarla

class CamionAdapter:
    def __init__(self, camion: Camion) -> None:
        self.camion = camion

    def gms_a_decimal(self, g: float, m: float, s: float, direccion: str) -> float:
        """
        Convierte GMS (grados, minutos, segundos) a decimal.
        
        Args:
            - `g (float)`: Grados

            - `m (float)`: Minutos

            - `s (float)`: Segundos

            - `direccion (str)`: Dirección ('N', 'S', 'E', 'W')
            
        Returns:
            Coordenada en formato decimal
        """
        if direccion not in ['N', 'S', 'E', 'W']:
            raise ValueError("Dirección no válida.")
            
        decimal = g + m / 60 + s / 3600
        if direccion in ['S', 'W']:
            decimal *= -1
        return decimal
    
    def gms_a_olc(self) -> Optional[str]: #Se usa esta para la transformación
        """
        Convierte coordenadas GMS a OLC.
        
        Returns:
            OLC o None si las coordenadas son inválidas
        """
        try:
            lat_gms = self.camion.gms["lat"]
            lon_gms = self.camion.gms["long"]
            
            if lat_gms is None or lon_gms is None:
                return None
                
            if not (isinstance(lat_gms, tuple) and len(lat_gms) == 4 and
                    isinstance(lon_gms, tuple) and len(lon_gms) == 4):
                return None
                
            lat_decimal = self.gms_a_decimal(*lat_gms)
            lon_decimal = self.gms_a_decimal(*lon_gms)
            
            return olc.encode(lat_decimal, lon_decimal)
        except Exception as e:
            return None