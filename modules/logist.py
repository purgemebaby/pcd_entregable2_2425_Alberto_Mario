import asyncio
import datetime
from typing import Dict, Set
from modules.camion import Camion, CamionObserver
from modules.adapter_coordenadas import CamionAdapter

class CentroLogistico(CamionObserver):
    # Patrón singleton según las transparencias
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.camiones: Set[Camion] = set()
        self.adapters: Dict[str, CamionAdapter] = {}
        self.medias: Dict[str, list] = {}
        self.std: Dict[str, list] = {}
        self.last_ocl: Dict[str, list] = {}
        self._escuchando = None


    async def update(self, camion: Camion, needed: bool):
        """Actualiza el centro logísitco con la información recibida del camión a través del observer.
        Si hay más de 12 datos en humedades y temperaturas, se calculan las medias y desviaciones nuevas y se borran los datos antiguos.
        """
        try:
            print(f"\nActualización rutinaria camión {camion.matricula}")
            
            temp = camion.temperaturas[-1] if camion.temperaturas else None
            hum = camion.humedades[-1] if camion.humedades else None
            
            print(f"📍 Ubicación: {camion.gms}")
            print(f"🌡 Temp: {temp}°C | 💧 Hum: {hum}%\n")


    #No se guarda un historial completo de las coordenadas, solo cada vez que se calculan los estadísticos
            if camion.matricula in self.adapters:
                fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                olc_code = self.adapters[camion.matricula].gms_a_olc()

                if olc_code:
                    self.last_ocl[camion.matricula] = [olc_code, fecha]
                else:
                    print("Error al convertir coordenadas a OLC")

            if needed:
                print("📊 Estadísticas actualizadas:")
                print(f"Avg Temp: {camion.media_actual['mean_temp']}°C")
                print(f"Avg Hum: {camion.media_actual['mean_hum']}%")
                print(f"Std Temp: {camion.desviacion_actual['std_temp']}°C")
                print(f"Std Hum: {camion.desviacion_actual['std_hum']}%\n")

                fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.medias[camion.matricula] += [camion.media_actual.copy(), fecha]
                self.std[camion.matricula] += [camion.desviacion_actual.copy(), fecha]

        except Exception as e:
            print(f"Error de seguimiento: {str(e)}")


    async def escuchar(self):
        """Permite recibir actualizaciones de los camiones"""
        if not self._escuchando or self._escuchando.done(): #Si no está siendo ejecutado ninguna o ya ha terminado
            self._escuchando = asyncio.create_task(self._escuchar_camiones())


    async def stop_escucha(self):
        """Detiene el seguimiento"""
        if self._escuchando:
            self._escuchando.cancel()
            try:
                await self._escuchando
            except asyncio.CancelledError:
                pass

    async def _escuchar_camiones(self):
        """Al escuchar, se recibe actualizaciones de los camiones cada 5 segundos y lo notifica 
        al centro logístico a través del Observer"""
        while True:
            update_tasks = [camion.update() for camion in self.camiones]
            await asyncio.gather(*update_tasks)
            await asyncio.sleep(5)  #R2


    def add_camion(self, camion: Camion):
        self.camiones.add(camion)
        self.adapters[camion.matricula] = CamionAdapter(camion)
        self.medias[camion.matricula] = []
        self.std[camion.matricula] = []
        Camion.add_observer(self)