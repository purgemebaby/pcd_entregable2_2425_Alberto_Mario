from typing import Dict, List, Optional, Tuple, Set
from abc import ABC, abstractmethod
from statistics import mean, stdev

import random as rd
import string

# Definimos una interfaz para los observers. Al ser abstractos, obliga a las clases a implementar el método update.
# No se puede instanciar directamente, sino para ser heredada.


class CamionObserver(ABC):
    @abstractmethod
    async def update(self, camion: 'Camion', needed: bool):
        """Recibe actualizaciones del camión
            - `camion (Camion)`: Camión que ha recibido la actualización
            
            - `needed (bool)`: Indica si se necesita actualizar la información de la media y desviación al centro.
        """
        pass


class Camion:
    TEMP_MAX = 22.5
    TEMP_MIN = 19.5
    HUM_MIN = 86
    HUM_MAX = 94
    _ids_generados = set()
    _observers: Set[CamionObserver] = set()


    @classmethod
    def add_observer(cls, observer: CamionObserver):
        """Añade un observer desde el centro logístico para recibir actualizaciones de los camiones"""
        cls._observers.add(observer)

    @classmethod
    async def notify_observers(cls, camion: 'Camion', needed: bool):
        """Notifica a los observers del centro logístico de que se ha actualizado el camión
        - `camion (Camion)`: Camión que ha recibido la actualización.
        
        - `needed (bool)`: Indica si se necesita actualizar la información de la media y desviación al centro.
        """
        for observer in cls._observers:
            await observer.update(camion, needed)

    @classmethod
    def new_id(cls) -> str:
        """Genera una matrícula para identificar de forma única el camión"""
        while True:
            new_id = "".join(rd.choices(string.ascii_uppercase + string.digits, k=6))
            if new_id not in cls._ids_generados:
                cls._ids_generados.add(new_id)
                return new_id


#Inicializamos las coordenadas suponiendo un centro de salida común para todos los camiones por comodidad
    def __init__(self):
        self.matricula: str = self.new_id()
        self.gms: Dict[str, Optional[Tuple[float, float, float, str]]] = {
            "lat": (40.0, 25.0, 10.5, 'N'),
            "long": (3.0, 42.0, 20.3, 'W')
        }
        self.temperaturas: List[float] = []
        self.humedades: List[float] = []
        self.media_actual: Dict[str, float] = {"mean_temp": 0.0, "mean_hum": 0.0}
        self.desviacion_actual: Dict[str, float] = {"std_temp": 0.0, "std_hum": 0.0}
        self._contador: int = 0
        self._half: int = 0


# Funciones de notificación
    async def variation2(self) -> None:
        """Verifica variaciones significativas en los últimos 30 segundos"""
        try:
            if len(self.temperaturas) < 6 or len(self.humedades) < 6:
                print("No hay datos suficientes para verificar variaciones")
                return

            temp_var = abs(self.temperaturas[-1] - self.temperaturas[-6])
            hum_var = abs(self.humedades[-1] - self.humedades[-6])

            if temp_var > 2:
                print(f"Camion - {self.matricula} - 🟥 Alerta temperatura - Variación de 2°C. {self.temperaturas[-1]}°C respecto a la anterior {self.temperaturas[-6]}°C")
                return

            if hum_var > 4:
                print(f"Camion - {self.matricula} - 🟥 Alerta humedad - Variación de 4%. {self.humedades[-1]}% respecto a la anterior {self.humedades[-6]}%")
                return

        except Exception as e:
            print(f"Error verificando variaciones: {e}")

    async def update(self) -> None:
        """
        Actualiza los datos del camión. Si hay más de 12 datos en humedades y temperaturas,
        se calculan las medias y desviaciones nuevas y se borran los datos antiguos.
        """

        needed = False # Indica si se necesita actualizar la media y desviación

        if self.gms["lat"] is None or self.gms["long"] is None:
            raise ValueError("Las coordenadas GMS no están inicializadas")

        lat_grados = self._rango(rd.normalvariate(self.gms["lat"][0], 0.01), 0, 90)
        lat_minutos = self._rango(rd.normalvariate(self.gms["lat"][1], 0.5), 0, 59)
        lat_segundos = self._rango(rd.normalvariate(self.gms["lat"][2], 1), 0, 59.999)
        lon_grados = self._rango(rd.normalvariate(self.gms["long"][0], 0.1), 0, 180)
        lon_minutos = self._rango(rd.normalvariate(self.gms["long"][1], 0.5), 0, 59)
        lon_segundos = self._rango(rd.normalvariate(self.gms["long"][2], 1), 0, 59.999)
        self.gms = {
            "lat": (lat_grados, lat_minutos, lat_segundos, rd.choices(["S", "N"], weights=[0.5, 0.5])[0]),
            "long": (lon_grados, lon_minutos, lon_segundos, rd.choices(["W", "E"], weights=[0.5, 0.5])[0])
        }

        temperatura = round(rd.normalvariate(21, 0.8), 2) 
        humedad = round(rd.uniform(85, 95), 2)
        self.temperaturas.append(temperatura)
        self.humedades.append(humedad)
        self._contador += 1
        self._half += 1

        #1. Si ya ha pasado un minuto, actualizamos la media
        if self._half == 2:
            needed = True
            medias = list(map(lambda x: round(mean(x), 2), [self.temperaturas, self.humedades]))
            stds = list(map(lambda x: round(stdev(x), 2), [self.temperaturas, self.humedades]))

            self.media_actual = dict(zip(["mean_temp", "mean_hum"], medias))
            self.desviacion_actual = dict(zip(["std_temp", "std_hum"], stds))

            await self.__class__.notify_observers(self, needed)

        else:
            await self.__class__.notify_observers(self, needed)

        # 2. Comprobamos si hay alguna variación que supere el umbral
        if temperatura > self.TEMP_MAX or temperatura < self.TEMP_MIN:
            print(f"Camion - {self.matricula} - 🟥 Alerta de temperatura. Umbral excedido: {temperatura}°C")
        
        if humedad < self.HUM_MIN or humedad > self.HUM_MAX:
            print(f"Camion - {self.matricula} - 🟥 Alerta de humedad. Umbral excedido: {humedad}%")


        # 3. Si ya ha pasado 30 segundos, comprobamos si hay alguna variación que supere el umbral
        if self._contador == 6:
            await self.variation2()
            self._contador = 0

            if self._half == 2:
                self.temperaturas.clear()
                self.humedades.clear()
                self._half = 0





    def _rango(self, value: float, min_value: float, max_value: float) -> float:
        """Define el rango de valores posibles para las coordenadas para que sea realista 
        y no dé errores al transformar coordenadas.
        - `value (float)`: Valor a evaluar

        - `min_value (float)`: Valor mínimo

        - `max_value (float)`: Valor máximo
        """
        return max(min(value, max_value), min_value)



# Funciones para almacenar la información crucial en el centro.
    def get_gms(self) -> Dict[str, Optional[Tuple[float, float, float, str]]]:
        return self.gms

    def get_means(self) -> Dict[str, float]:
        return self.media_actual

    def get_stds(self) -> Dict[str, float]:
        return self.desviacion_actual



# Métodos mágicos
    def __repr__(self) -> str:
        return f"Camion({self.matricula}, {self.media_actual['mean_temp']}°C, {self.media_actual['mean_hum']}%)"

    def __str__(self) -> str:
        return (f"Camion: {self.matricula}\n"
                f"Temperatura: {self.media_actual['mean_temp']}°C\n"
                f"Humedad: {self.media_actual['mean_hum']}%\n"
                f"(Lat: {self.gms['lat']}, Long: {self.gms['long']})")


