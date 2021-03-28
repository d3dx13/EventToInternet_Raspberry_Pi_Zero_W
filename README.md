# USB_to_Internet
## Что это такое? И как этим пользоваться?

**Легковесный** python **демон** для отправки **событий USB периферии** (и не только) на **удалённые WEB сервера**. 

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



## Как это установить?

Первым делом желательно обновить систему, чтобы не возникло проблем с пакетами.

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo reboot
# reboot - необходим, только если произошло обновления ядра, что весьма вероятно.
```

Для установки демона нам понадобится git, а ещё python3.X. Пакеты из requirements.txt обязательно ставить из под sudo.

```bash
sudo apt install -y git
sudo apt install -y htop python3 python3-dev python3-pip gcc

git clone https://github.com/ITMO-lab/EventToInternet.git
sudo mv EventToInternet /etc/systemd/system/
sudo chown -R root:root /etc/systemd/system/EventToInternet
cd /etc/systemd/system/EventToInternet

sudo python3 -m pip install -r requirements.txt
sudo bash install.sh
```



## Как это Удалить?

Удаление этого демона, если всё же понадобилось, также не представляет трудностей.

```bash
sudo bash /etc/systemd/system/EventToInternet/uninstall.sh

sudo rm -rf /etc/systemd/system/EventToInternet*
```

