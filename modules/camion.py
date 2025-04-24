from typing import Dict
import string
import random as rd
from statistics import mean, stdev

from typing import List, Tuple


class Camion:
    _ids_generados = set()

    @classmethod
    def new_id(cls) -> str:
        while True:
            new_id = "".join(rd.choices(string.ascii_uppercase + string.digits, k=6))
            if new_id not in cls._ids_generados:
                cls._ids_generados.add(new_id)
                return new_id

    def __init__(self):
        self.id: str = self.new_id()
        self.gms: Dict[str, Tuple[float, float, float, str]] = {
            "lat": None,  # (40, 25, 10.5, 'N')
            "long": None   # (3, 42, 20.3, 'W')
        }
        self.temperaturas: List[float] = []
        self.humedades: List[float] = []
        self.media_actual: Dict[str, float] = {"mean_temp": 0.0, "mean_hum": 0.0}
        self.desviacion_actual: Dict[str, float] = {"std_temp": 0.0, "std_hum": 0.0}



    async def update(self):
        """
        Actualiza los datos del camión. Si hay más de 12 datos en humedades y temperaturas, se calculan las medias y desviaciones nuevas y se borran los datos antiguos.

        - `temperatura`: La temperatura tomará valores aleatorios entre 19 y 23 grados. Para conseguir este efecto, se ha utilizado una normal de media 21 y desviación 0.8. Esta elección es debida a que la temperatura es una magnitud que puede variar por miles de factores ruidosos, haciéndola adecuada para esta distribución.

        - `humedad`: La humedad toma valores entre 85% y 95%. Para conseguir este efecto, se ha utilizado una uniforme de rango 85 a 95. La humedad es controlada, y cada alimento tiene la suya, lo cual hace que estos valores sean equiprobables, perfecto para una uniforme.

        - `gms`: Las coordenadas GMS se generan aleatoriamente. Para conseguir esto, se ha utilizado una normal de media 0 y desvia
        """

        def rango(value: float, min_value: float, max_value: float) -> float:
            """Define el rango de valores posibles para las coordenadas"""
            return max(min(value, max_value), min_value)

        lat_grados = rango(rd.normalvariate(self.gms["lat"][0], 0.01), 0, 90)
        lat_minutos = rango(rd.normalvariate(self.gms["lat"][1], 0.5), 0, 59)
        lat_segundos = rango(rd.normalvariate(self.gms["lat"][2], 1), 0, 59.999)

    # Generar nueva longitud con límites
        lon_grados = rango(rd.normalvariate(self.gms["long"][0], 0.1), 0, 180)
        lon_minutos = rango(rd.normalvariate(self.gms["long"][1], 0.5), 0, 59)
        lon_segundos = rango(rd.normalvariate(self.gms["long"][2], 1), 0, 59.999)

        self.gms = {
            "lat": (lat_grados, lat_minutos, lat_segundos, rd.choice(['N', 'S'])),
            "long": (lon_grados, lon_minutos, lon_segundos, rd.choice(['E', 'W']))
        }

        temperatura = round(rd.normalvariate(21, 0.8), 2) 
        humedad = round(rd.uniform(85, 95), 2)
        self.temperaturas.append(temperatura)
        self.humedades.append(humedad)

        # Si ya hay 12 datos nuevos
        if len(self.temperaturas) > 12 and len(self.humedades) > 12:
            medias = list(map(lambda x: round(mean(x), 2), [self.temperaturas, self.humedades]))
            stds = list(map(lambda x: round(stdev(x), 2), [self.temperaturas, self.humedades]))

            self.media_actual = dict(zip(["mean_temp", "mean_hum"], medias))
            self.desviacion_actual = dict(zip(["std_temp", "std_hum"], stds))

            self.temperaturas.clear()
            self.humedades.clear()

def __repr__(self) -> str:
    return f"Camion({self.id}, {self.media_actual['mean_temp']}°C, {self.media_actual['mean_hum']}%)"

def __str__(self) -> str:
    return f"Camion: {self.id}\n Temperatura: {self.media_actual['mean_temp']}°C\n Humedad: {self.media_actual['mean_hum']}% \n (Lat: {self.gms['lat']}, Long: {self.gms['long']})"

# async def send(self)

