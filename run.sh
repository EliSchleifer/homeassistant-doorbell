#!/usr/bin/env bashio

echo Starting Homeassistant Doorbell


bashio::log.yellow " - Go to the Hass.io Panel."


USERNAME=$(bashio::config "username")

bashio::log.info "${USERNAME}"

IP_ADDRESS=$(bashio::config "HomeAssistantIP")

bashio::log.info "${IP_ADDRESS}"

HARDWARE=$(bashio::hardware)

bashio::log.info "$HARDWARE"

pip install mutagen
#pip3 install mutagen

python -u doorbell-server.py
