import asyncio
import evdev
from datetime import datetime
from EventToInternet import _config_event_to_string, KEYBOARD_MAX_STRING_LENGTH, KEYBOARD_UPDATE_DEVICES_TIMEOUT


class KeyboardListener:
    def __init__(self, regular_letters_codes=_config_event_to_string.regular_letters_codes.copy(),
                 regular_symbols_codes=_config_event_to_string.regular_symbols_codes.copy(),
                 capital_letters_codes=_config_event_to_string.capital_letters_codes.copy(),
                 capital_symbols_codes=_config_event_to_string.capital_symbols_codes.copy(),
                 numpad_symbols_codes=_config_event_to_string.numpad_symbols_codes.copy(),
                 send_trigger_keys=_config_event_to_string.send_trigger_keys.copy(),
                 capitalize_all_keys=_config_event_to_string.capitalize_all_keys.copy(),
                 capitalize_symbols_turn_keys=_config_event_to_string.capitalize_symbols_turn_keys.copy()):
        self.event_devices = map(evdev.InputDevice, evdev.list_devices())
        self.event_devices = {dev.path: dev for dev in self.event_devices}
        self.memory_devices = {}
        self.regular_letters_codes = regular_letters_codes
        self.regular_symbols_codes = regular_symbols_codes
        self.capital_letters_codes = capital_letters_codes
        self.capital_symbols_codes = capital_symbols_codes
        self.numpad_symbols_codes = numpad_symbols_codes
        self.send_trigger_keys = send_trigger_keys
        self.capitalize_all_keys = capitalize_all_keys
        self.capitalize_symbols_turn_keys = capitalize_symbols_turn_keys
        asyncio.ensure_future(self.__update_devices())
        for device in self.event_devices.values():
            asyncio.ensure_future(self.__get_keyboard_events(device))

    async def __update_devices(self):
        while True:
            await asyncio.sleep(KEYBOARD_UPDATE_DEVICES_TIMEOUT)
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
                    except KeyError:
                        pass

    async def __get_keyboard_events(self, device):
        try:
            async for event in device.async_read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    category = evdev.categorize(event)
                    if type(category.keycode) == list:
                        continue
                    try:
                        await self.__keyboard_event_handler(device, category)
                    except Exception as e:
                        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
                        pass
        except OSError as e:
            if e.errno == 19:
                return

    async def __keyboard_event_handler(self, device, category):
        if self.memory_devices.get(device.path) is None:
            self.memory_devices[device.path] = {"string": "", "is_capital_letters": False, "is_capital_symbols": False}
        if len(self.memory_devices.get(device.path)["string"]) > KEYBOARD_MAX_STRING_LENGTH:
            self.memory_devices[device.path]["string"] = self.memory_devices[device.path]["string"][1:]
        if category.keystate == category.key_hold:
            return
        if category.keycode in self.send_trigger_keys:
            if len(self.memory_devices[device.path]["string"]) > 0:
                json_event = {
                    'string': self.memory_devices[device.path]["string"],
                    'name': device.name,
                    'timestamp': datetime.timestamp(datetime.now()),
                    'info': {
                        'phys': device.phys,
                        'path': device.path,
                        'fd': device.fd,
                        'bustype': device.info.bustype,
                        'product': device.info.product,
                        'vendor': device.info.vendor,
                        'version': device.info.version,
                    }
                }
                await self.dict_handler(json_event)
                self.memory_devices[device.path]["string"] = ""
            return
        if category.keycode in self.capitalize_all_keys:
            if category.keystate == category.key_down or category.keystate == category.key_up:
                self.memory_devices[device.path]["is_capital_letters"] = not self.memory_devices[
                    device.path]["is_capital_letters"]
                self.memory_devices[device.path]["is_capital_symbols"] = not self.memory_devices[
                    device.path]["is_capital_symbols"]
        elif category.keycode in self.capitalize_symbols_turn_keys and category.keystate == category.key_down:
            self.memory_devices[device.path]["is_capital_letters"] = not self.memory_devices[
                device.path]["is_capital_letters"]
        if category.keystate != category.key_down:
            return
        if self.memory_devices[device.path]["is_capital_letters"] \
                and category.scancode in self.capital_letters_codes.keys():
            self.memory_devices[device.path]["string"] += self.capital_letters_codes.get(category.scancode)
        elif not self.memory_devices[device.path]["is_capital_letters"] \
                and category.scancode in self.regular_letters_codes.keys():
            self.memory_devices[device.path]["string"] += self.regular_letters_codes.get(category.scancode)
        elif self.memory_devices[device.path]["is_capital_symbols"] \
                and category.scancode in self.capital_symbols_codes.keys():
            self.memory_devices[device.path]["string"] += self.capital_symbols_codes.get(category.scancode)
        elif not self.memory_devices[device.path]["is_capital_symbols"] \
                and category.scancode in self.regular_symbols_codes.keys():
            self.memory_devices[device.path]["string"] += self.regular_symbols_codes.get(category.scancode)
        elif category.scancode in self.numpad_symbols_codes.keys():
            self.memory_devices[device.path]["string"] += self.numpad_symbols_codes.get(category.scancode)

    async def dict_handler(self, dict_event):
        print(f"\nstring: {dict_event['string']}\n"
              f"device: {''.join(['%s: %s; ' % (key, value) for (key, value) in dict_event['info'].items()])}")
