import asyncio
from USB_to_Internet.USBListener import USBListener


class SendUSBListener(USBListener):
    async def string_handler(self, device, string):
        print(f"\n{device.info}\n{device}\nstring:{string}")


usb = SendUSBListener()

loop = asyncio.get_event_loop()
loop.run_forever()
