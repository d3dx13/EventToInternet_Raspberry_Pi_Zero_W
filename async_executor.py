import asyncio
import requests
from EventToInternet.KeyboardListener import KeyboardListener


class BarcodeKeyboardListener(KeyboardListener):
    async def dict_handler(self, dict_event):
        requests.post("https://webhook.site/79d5f27a-7c16-47b6-97cc-9ba88d423499", json=dict_event)


BarcodeKeyboardListener()

loop = asyncio.get_event_loop()
loop.run_forever()
