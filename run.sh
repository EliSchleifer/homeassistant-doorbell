#!/usr/bin/env bashio

echo Starting Homeassistant Doorbell

pip3 install mutagen


USERNAME=$(bashio::config 'username')

bashio::log.info "${USERNAME}"

IP_ADDRESS=$(bashio::config 'HomeAssistantIP')

bashio::log.info "${IP_ADDRESS}"

bashio::log.info "${bashio::hardware}"

python3 -u doorbell-server.py
