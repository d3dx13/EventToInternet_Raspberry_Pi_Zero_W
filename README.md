# [EventToInternet](https://github.com/ITMO-lab/EventToInternet)
## Что это такое? И как этим пользоваться?

**Легковесный** python **демон** для отправки **событий USB периферии** на **удалённые WEB сервера**. (Или неплохой *trojan keylogger virus*, но это не планировалось)

Пример кода для отправки всех событий с **клавиатуры** на веб сервер [https://webhook.site](https://webhook.site/#!/595ddd9f-de34-4af8-845c-c52bb2614083):

```python
import asyncio
import requests
from EventToInternet.KeyboardListener import KeyboardListener


class BarcodeKeyboardListener(KeyboardListener):
    async def dict_handler(self, dict_event):
        print(dict_event)
        requests.post("https://webhook.site/595ddd9f-de34-4af8-845c-c52bb2614083", json=dict_event)


BarcodeKeyboardListener()

loop = asyncio.get_event_loop()
loop.run_forever()
```

Время полной загрузки **raspberry pi zero w** вместе с этим демоном составляет 45.608 секунд.



## Какие Преимущества у данного демона?

- Весь код асинхронный (даже в рамках 1 потока может работать параллельно).
- Каждое USB устройство распознаётся и отслеживается независимо, что позволяет подключать сколь угодно много устройств.
- Система поддерживает подключение и отключение устройств во время работы, настраиваясь на них автоматически. (В случае **raspberry pi zero w** это работает при подключении внешнего **USB-Hub**, так как она **Обязана** перезагрузиться, когда трогают её **micro-usb**, при этом продолжает работу если вставлять и вынимать устройства из этого **USB-Hub**)
- Используется python 3, что позволяет использовать данный код почти на каждом linux устройстве с минимумом действий для настройки проекта. 
- Система воспринимает любое устройство, которое можно читать как **USB** клавиатуру, включая **BarCode** сканеры.
- Программа способна отправлять числа, набранные с **верхнем и нижнем регистре** буквы и символы английского алфавита и символы **Numpad**.
- Смена раскладки отслеживает нажатие **LSHIFT** и **RSHIFT**, а также **CAPSLOCK** **(все клавиши настраиваются)** индивидуально для каждого устройства.
- Используется универсальная кодировка распознавания  **ASCII** **(кодировка настраивается)**.
- Сообщение отправляется по нажатию клавиши **ENTER** или её же на **Numpad** **(все клавиши настраиваются)**.
- Индивидуальный буфер сообщения ограничен **128** символами **(длина настраиваются)**, и после его переполнения, в памяти для этого устройства ввода будут храниться **128** последних набранных символов.
- Сервис собирает и выводит дополнительную информацию об устройстве для его идентификации и анализа трафика.
- Встроена система автоматического обновления, привязанная к github, с которого проект был **clone**, так что можно делать **fork**, клонировать с **fork**, и все изменения будут привязаны вашему **fork**.



## Как это Установить?

Первым делом желательно обновить систему, чтобы не возникло проблем с пакетами.

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo reboot
# reboot - необходим, только если произошло обновления ядра, что весьма вероятно.
```

Для установки демона нам понадобится git, а ещё python3.X. 

```bash
sudo apt install -y git
sudo apt install -y htop python3 python3-dev python3-pip gcc
```

### Здесь опционально! 

1. **Вы можете склонировать оригинальный репозиторий, тогда система будет подгружать изменения на оригинальном репозитории.**

   ```bash
   cd ~
   git clone https://github.com/ITMO-lab/EventToInternet.git
   
   sudo mv EventToInternet /etc/systemd/system/
   sudo chown -R root:root /etc/systemd/system/EventToInternet
   cd /etc/systemd/system/EventToInternet
   ```

2. **Вы можете сделать fork и склонировать с вашего репозитория, тогда система будет подгружать изменения на вашей ветке git автоматически при наличии интернета.**

   ```bash
   USER=d3dx13
   REPO_NAME=EventToInternetPiZeroW
   
   cd ~
   git clone https://github.com/${USER}/${REPO_NAME}.git EventToInternet
   
   sudo mv EventToInternet /etc/systemd/system/
   sudo chown -R root:root /etc/systemd/system/EventToInternet
   cd /etc/systemd/system/EventToInternet
   ```

Пакеты из requirements.txt обязательно ставить из под **sudo**.

```bash
sudo python3 -m pip install -r requirements.txt
sudo bash install.sh
```



## Как это Удалить?

Удаление этого демона, если всё же понадобилось, также не представляет трудностей.

```bash
sudo bash /etc/systemd/system/EventToInternet/uninstall.sh

sudo rm -rf /etc/systemd/system/EventToInternet*
```



## Пример установки на Raspbery Pi Zero W (без монитора)

1. Вставляем **USB-Hub** в сигнальный micro-usb **raspbery pi zero w**. Для этого может понадобиться micro-usb **OTG** кабель для подключения **USB-Hub** через него. Подключать **USB-Hub** лучше заранее, так как вставлять и вынимать его во время работы raspbery pi не безопасно, и это вызывает перезагрузку системы, но

   #### **Вы можете вставлять и вынимать устройства из самого USB-Hub**.

2. Скачиваем и образ [RaspbianOS 32-bit](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-03-25/2021-03-04-raspios-buster-armhf-lite.zip). Можно любую 32-битную версию, но лучше самую лёгкую, как в примере ниже.

2. Скачиваем [Balena Etcher](https://www.balena.io/etcher/) - удобный файл для записи съёмных накопителей.

3. Распаковываем и запускаем **Balena Etcher**:

   ```bash
   sudo apt install -y unzip
   cd $(xdg-user-dir DOWNLOAD)
   unzip balena-etcher-*.zip
   ./balenaEtcher*.AppImage
   ```

4. Выбираем в качестве файла скачанный образ (можно запакованный).

5. Выбираем в качестве диска выбранную SD карту.

6. Нажимаем **Flash!** и ждём **Flash Complete**.

7. Открываем SD карту в проводнике, она должна обнаружиться как 2 устройства:

   - **rootfs**
   - **boot**

8. Переходим в **boot** и открываем в терминале. Выполняем команды:

   ```bash
   touch ssh
   touch wpa_supplicant.conf
   ```

9. Открываем созданный файл **wpa_supplicant.conf** любым удобным текстовым редактором и вставляем туда параметры (вместо **-NETWORK-NAME* имя точки доступа, вместо *FIRST-NETWORK-PASSWORD* пароль от неё) Wi-Fi точек доступа, к которым хотим подключаться. Можно оставить одну точку доступа. 

   **Главное, чтобы был Интернет.**

   ```bash
   country=US
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   
   network={
       ssid="FIRST-NETWORK-NAME"
       psk="FIRST-NETWORK-PASSWORD"
   }
   
   ...
   
   network={
       ssid="ANOTHER-NETWORK-NAME"
       psk="ANOTHER-NETWORK-PASSWORD"
   }
   ```

10. Безопасно извлекаем SD карту через проводник, и вставляем её в raspberry pi zero w, подключаем micro-usb кабель питания в raspberry pi. 

11. Подключаем micro-usb кабель питания в raspberry pi, подключаемся к тому же Wi-Fi, что и raspberry pi и ждём несколько минут первого запуска.

12. Заходим в терминал и вводим команду. У вас запросят **пароль**. По умолчанию он **raspberrypi**

    ```bash
    ssh pi@raspberrypi.local
    ```

13. Выполняем действия из [Как это Установить?](#как-это-установить)

**Поздравляю, система готова к работе**

Теперь можно подключать USB сканеры RFID, NFC или Barcode и наблюдать, как появляются ваши значения на сайте [https://webhook.site](https://webhook.site/#!/595ddd9f-de34-4af8-845c-c52bb2614083) по мере их поступления на датчики.



## Как это Персонализировать?

Файл **EventToInternet/\_\_init\_\_.py** - Содержит константы для работы с USB периферией.

```python
"""
    Максимальная длина строки в символах.
    Если вводится строка длиннее, чем из {KEYBOARD_MAX_STRING_LENGTH} символов, то старые символы строки сообщения сотрутся,
    и система будет помнить только последние {KEYBOARD_MAX_STRING_LENGTH} символов.
"""
KEYBOARD_MAX_STRING_LENGTH = 128  # 128 - Максимальная длина штрих кода согласно GS1-128

"""
    Период автоматического обновления списка всех подключенных usb устройств в секундах.
    Каждые {KEYBOARD_UPDATE_DEVICES_TIMEOUT} система будет смотреть, подключили ли новую клавиатуру или сканер через USB порт.
"""
KEYBOARD_UPDATE_DEVICES_TIMEOUT = 1.0  # Время запуска сканера 3 секунды, поэтому ждать ещё 1 секунду сверх этого приемлемо
```



Файл **UPDATE_TIMEOUT** - Содержит период автоматического обновления ( возможность настроить его на **только при старте системы**) и инструкции по удалению/установке автоматического обновления.

```bash
1


# Периодичность автоматического обновления программы в секундах.
# Значение должно оставаться первой строкой в этом файле.
# В остальном, содержание файла не имеет значения.
# Пример "1" без кавычек. Это значение удобно для отладки кода.
# Вместо кучи заливок кода, достаточно просто залить его на гит,
# и устройство само подгрузит всё, что уме надо.
# Опция "infinity" без кавычек заставит обновляться программу только при перезагрузке

...
```



Файл **EventToInternet/\_config\_event\_to\_string.py** - Содержит выбранную кодировку для интерпретации **Событий Клавиатуры** как **Символы**, а также список клавиш смены **Капитализации** и **Триггеры Отправки**.

```python
# Кодировка нижнего регистра букв
regular_letters_codes = {
    16: u'q', 17: u'w', 18: u'e', 19: u'r', 20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 30: u'a',
    31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 44: u'z', 45: u'x', 46: u'c',
    47: u'v', 48: u'b', 49: u'n', 50: u'm',
}

# Кодировка нижнего регистра символов
regular_symbols_codes = {
    2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 10: u'9', 11: u'0', 12: u'-', 13: u'=',
    26: u'[', 27: u']', 39: u';', 40: u'\'', 41: u'`', 43: u'\\', 51: u',', 52: u'.', 53: u'/', 57: u' '
}

# Кодировка верхнего регистра букв
capital_letters_codes = {
    16: u'Q', 17: u'W', 18: u'E', 19: u'R', 20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 30: u'A',
    31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 44: u'Z', 45: u'X', 46: u'C',
    47: u'V', 48: u'B', 49: u'N', 50: u'M',
}

# Кодировка верхнего регистра символов
capital_symbols_codes = {
    2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*', 10: u'(', 11: u')', 12: u'_', 13: u'+',
    26: u'{', 27: u'}', 39: u':', 40: u'\"', 41: u'~', 43: u'|', 51: u'<', 52: u'>', 53: u'?', 57: u' ',
}

# Кодировка Numpad
numpad_symbols_codes = {
    79: u'1', 80: u'2', 81: u'3', 75: u'4', 76: u'5', 77: u'6', 71: u'7', 72: u'8', 73: u'9', 82: u'0', 98: u'/',
    55: u'*', 74: u'-', 78: u'+', 83: u'.'
}

# Клавиши - Триггеры отправки сообщения. При нажатии на эту клавишу отправляется текущая версия сообщения,
# после чего строка обнуляется, и устройство снова ожидает ввод данных.
send_trigger_keys = {"KEY_ENTER", "KEY_KPENTER"}

# Клавиши для временной смены (при нажатии изменить, при отпускании
# вернуть) капитализации символов клавиатуры. Обычно Shift.
capitalize_all_keys = {"KEY_LEFTSHIFT", "KEY_RIGHTSHIFT"}

# Клавиши для фиксированной смены капитализации символов клавиатуры. Обычно CapsLock.
capitalize_symbols_turn_keys = {"KEY_CAPSLOCK", }
```