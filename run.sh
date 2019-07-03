echo Plugin Time!


#!/bin/bash

pip3 install --upgrade pip
pip3 install mutagen
pip3 install netifaces

python3 mp3-server.py
