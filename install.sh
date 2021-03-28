#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
# sudo reboot

sudo apt install -y htop python3 python3-dev python3-pip gcc
python3 -m pip install -r requirements.txt

