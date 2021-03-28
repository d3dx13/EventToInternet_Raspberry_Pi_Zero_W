# USB_to_Internet
Легковесный python демон для отправки событий USB периферии на удалённые WEB сервера



Время полной загрузки raspberry pi zero w вместе с этим фреймворком составляет 45.608 секунд.



```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo reboot
```



```bash
sudo apt install -y git

git clone https://github.com/ITMO-lab/wifi-autoconnector.git
sudo mv EventToInternet/ /etc/systemd/system/
sudo chown -R root:root /etc/systemd/system/EventToInternet
cd /etc/systemd/system/EventToInternet

sudo bash install.bash

cd ~
```

