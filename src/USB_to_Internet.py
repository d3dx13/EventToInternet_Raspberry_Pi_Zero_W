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
MAX_BARCODE_LENGTH = 128 * 2
UPDATE_DEVICES_TIMEOUT = 1.0  # В секундах

event_devices = map(evdev.InputDevice, evdev.list_devices())
event_devices = {dev.path: dev for dev in event_devices}
memory_devices = {}


async def update_devices():
    while True:
        await asyncio.sleep(UPDATE_DEVICES_TIMEOUT)
        new_event_devices = set(evdev.list_devices())
        old_event_devices = set(event_devices.keys())
        add_event_devices = new_event_devices.difference(old_event_devices)
        remove_event_devices = old_event_devices.difference(new_event_devices)
        if len(add_event_devices) > 0:
            for device in add_event_devices:
                event_devices[device] = evdev.InputDevice(device)
                asyncio.create_task(get_keyboard_events(event_devices[device]))
        if len(remove_event_devices) > 0:
            for device in remove_event_devices:
                event_devices.pop(device)
                try:
                    memory_devices.pop(device)
                except:
                    pass


async def get_keyboard_events(device):
    try:
        async for event in device.async_read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                category = evdev.categorize(event)
                if type(category.keycode) == list \
                        or category.keycode not in ALLOWED_KEYBOARD_KEYS.keys() \
                        or category.keystate != category.key_down:
                    continue
                try:
                    await keyboard_event_handler(device, category)
                except:
                    print("WTF")
    except OSError as e:
        if e.errno == 19:
            return


async def keyboard_event_handler(device, category):
    if memory_devices.get(device.path) is None:
        memory_devices[device.path] = ""
    if len(memory_devices.get(device.path)) > MAX_BARCODE_LENGTH:
        memory_devices[device.path] = ""
    if category.keycode == "KEY_ENTER":
        if len(memory_devices[device.path]) > 0:
            await http_send(device, memory_devices[device.path])
        memory_devices.pop(device.path)
        return
    memory_devices[device.path] += ALLOWED_KEYBOARD_KEYS.get(category.keycode)


async def http_send(device, string):
    requests.post('https://webhook.site/2614203d-2f5f-4178-a56d-66e2d557f2dc',
                  data=f"{device.info}\n{device}\nbarcode:{string}")


asyncio.ensure_future(update_devices())
for device in event_devices.values():
    asyncio.ensure_future(get_keyboard_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
