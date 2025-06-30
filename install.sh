#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install platformio
pip3 install PyQt5
pip3 install datetime
python3 main.py