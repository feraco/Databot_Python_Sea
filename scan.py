import asyncio
from bleak import BleakScanner
import nest_asyncio
nest_asyncio.apply()

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"{d.name or '(no name)'} — {d.address}")

asyncio.run(scan())

