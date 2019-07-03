#!/usr/bin/env bashio

echo Starting Homeassistant Doorbell


bashio::log.yellow " - Go to the Hass.io Panel."


USERNAME=$(bashio::config "username")

bashio::log.info "${USERNAME}"

IP_ADDRESS=$(bashio::config "HomeAssistantIP")

bashio::log.info "${IP_ADDRESS}"

bashio::log.info "$(bashio::hardware)"

pip3 install mutagen

python3 -u doorbell-server.py
