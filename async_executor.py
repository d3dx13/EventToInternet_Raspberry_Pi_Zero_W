import asyncio
from EventToInternet.KeyboardListener import KeyboardListener


class BarcodeKeyboardListener(KeyboardListener):
    async def dict_handler(self, dict_event):
        print(f"\nString: {dict_event['string']}\n"
              f"Device: {''.join(['%s: %s; ' % (key, value) for (key, value) in dict_event['info'].items()])}")


BarcodeKeyboardListener()

loop = asyncio.get_event_loop()
loop.run_forever()
