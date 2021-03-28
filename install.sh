#!/bin/bash

sudo apt install -y htop python3 python3-dev python3-pip gcc
sudo python3 -m pip install -r requirements.txt

sudo systemctl daemon-reload
sudo systemctl stop EventToInternet.service
sudo systemctl disable EventToInternet.service
sudo systemctl stop EventToInternetUpdate.service
sudo systemctl disable EventToInternetUpdate.service
sudo git pull --force
sudo cp -f /etc/systemd/system/EventToInternet/EventToInternet.service /etc/systemd/system/EventToInternet.service
sudo cp -f /etc/systemd/system/EventToInternet/EventToInternetUpdate.service /etc/systemd/system/EventToInternetUpdate.service
sudo systemctl daemon-reload
sudo systemctl enable EventToInternet.service
sudo systemctl start EventToInternet.service
sudo systemctl enable EventToInternetUpdate.service
sudo systemctl start EventToInternetUpdate.service

sudo systemctl status EventToInternet.service
sudo systemctl status EventToInternetUpdate.service
