import asyncio
from modules.logist import CentroLogistico
from modules.camion import Camion

async def main():
    centro = CentroLogistico()
    camion1 = Camion()
    camion2 = Camion()
    centro.add_camion(camion1)
    centro.add_camion(camion2)


    await centro.escuchar()
    await asyncio.sleep(62)
    print("\nDeteniendo monitoreo...")
    await centro.stop_escucha()


    print("\n📊 Datos finales almacenados:")
    print(f"Medias: {centro.medias}")
    print(f"Desviaciones: {centro.std}")
    print(f"Ubicación OLC: {centro.last_ocl}")

if __name__ == "__main__":
    asyncio.run(main())