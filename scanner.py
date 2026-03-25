import asyncio
import threading
from bleak import BleakScanner


class BluetoothScanner:
    def __init__(self, on_device_found):
        self.on_device_found = on_device_found
        self.seen = set()
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _run_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._scan_loop())

    async def _scan_loop(self):
        while self._running:
            try:
                # return_adv=True gives us (BLEDevice, AdvertisementData) per address
                results = await BleakScanner.discover(timeout=5.0, return_adv=True)
                for addr, (device, adv) in results.items():
                    if addr not in self.seen:
                        self.seen.add(addr)
                        rssi = adv.rssi if adv.rssi is not None else -100
                        self.on_device_found({
                            "id":      addr,
                            "name":    device.name or "Unknown",
                            "address": addr,
                            "rssi":    rssi,
                        })
            except Exception as e:
                print(f"[Scanner] Error: {e}")
            await asyncio.sleep(2)
