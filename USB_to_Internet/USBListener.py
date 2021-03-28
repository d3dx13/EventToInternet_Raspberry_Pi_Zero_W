import asyncio
import evdev
import requests

ALLOWED_KEYBOARD_KEYS = {
    "KEY_0": "0",
    "KEY_1": "1",
    "KEY_2": "2",
    "KEY_3": "3",
    "KEY_4": "4",
    "KEY_5": "5",
    "KEY_6": "6",
    "KEY_7": "7",
    "KEY_8": "8",
    "KEY_9": "9",
    "KEY_ENTER": "\n",
}
SPLIT_KEY = "KEY_ENTER"
MAX_BARCODE_LENGTH = 128 * 2
UPDATE_DEVICES_TIMEOUT = 1.0  # В секундах


class USBListener:
    def __init__(self):
        self.event_devices = map(evdev.InputDevice, evdev.list_devices())
        self.event_devices = {dev.path: dev for dev in self.event_devices}
        self.memory_devices = {}
        asyncio.ensure_future(self.__update_devices())
        for device in self.event_devices.values():
            asyncio.ensure_future(self.__get_keyboard_events(device))

    async def __update_devices(self):
        while True:
            await asyncio.sleep(UPDATE_DEVICES_TIMEOUT)
            new_event_devices = set(evdev.list_devices())
            old_event_devices = set(self.event_devices.keys())
            add_event_devices = new_event_devices.difference(old_event_devices)
            remove_event_devices = old_event_devices.difference(new_event_devices)
            if len(add_event_devices) > 0:
                for device in add_event_devices:
                    self.event_devices[device] = evdev.InputDevice(device)
                    asyncio.create_task(self.__get_keyboard_events(self.event_devices[device]))
            if len(remove_event_devices) > 0:
                for device in remove_event_devices:
                    self.event_devices.pop(device)
                    try:
                        self.memory_devices.pop(device)
                    except Exception as e:
                        print(e)
                        pass

    async def __get_keyboard_events(self, device):
        try:
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    category = evdev.categorize(event)
                    if type(category.keycode) == list \
                            or category.keycode not in ALLOWED_KEYBOARD_KEYS.keys() \
                            or category.keystate != category.key_down:
                        continue
                    try:
                        await self.__keyboard_event_handler(device, category)
                    except Exception as e:
                        print(e)
                        pass
        except OSError as e:
            if e.errno == 19:
                return

    async def __keyboard_event_handler(self, device, category):
        if self.memory_devices.get(device.path) is None:
            self.memory_devices[device.path] = ""
        if len(self.memory_devices.get(device.path)) > MAX_BARCODE_LENGTH:
            self.memory_devices[device.path] = ""
        if category.keycode == SPLIT_KEY:
            if len(self.memory_devices[device.path]) > 0:
                await self.string_handler(device, self.memory_devices[device.path])
                self.memory_devices.pop(device.path)
            return
        self.memory_devices[device.path] += ALLOWED_KEYBOARD_KEYS.get(category.keycode)

    async def string_handler(self, device, string):
        requests.post('https://webhook.site/2614203d-2f5f-4178-a56d-66e2d557f2dc',
                      data=f"{device.info}\n{device}\nbarcode:{string}")
