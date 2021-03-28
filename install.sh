#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo reboot

sudo apt install -y htop
sudo apt install -y python3.7 python3.7-dev python3-pip gcc
python3 -m pip install evdev


