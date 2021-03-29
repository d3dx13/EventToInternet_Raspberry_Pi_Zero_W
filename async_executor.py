import asyncio
import requests
from EventToInternet.KeyboardListener import KeyboardListener


class BarcodeKeyboardListener(KeyboardListener):
    async def dict_handler(self, dict_event):
        print(dict_event)


BarcodeKeyboardListener()

loop = asyncio.get_event_loop()
loop.run_forever()
