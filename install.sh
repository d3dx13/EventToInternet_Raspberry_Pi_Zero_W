#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
# sudo reboot

sudo apt install -y htop python3 python3-dev python3-pip gcc
python3 -m pip install -r requirements.txt

git clone https://github.com/ITMO-lab/wifi-autoconnector.git
sudo mv EventToInternet/ /etc/systemd/system/
sudo chown -R root:root /etc/systemd/system/EventToInternet
cd /etc/systemd/system/EventToInternet

sudo git pull
sudo cp -f EventToInternet.service /etc/systemd/system/EventToInternet.service