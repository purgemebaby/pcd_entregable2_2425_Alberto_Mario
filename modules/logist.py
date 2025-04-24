import asyncio

from modules.camion import Camion
from typing import Set, Dict


class CentroLogistico():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
    
    def _init(self):
        self.camiones: Set[Camion] = set()
        self.data: Dict[str, Dict] = {
            "": {},
            "olc": {},
        }


    # async def run(self):
    #     try:
    #         while True:
    #             for i in self.camiones:
    #                 i.update()
    #                 i.send()
    #                 await asyncio.sleep(5)
    #             pass
    #     except KeyboardInterrupt:
    #         print("Seguimiento de la flota terminado")
    #         exit(0)