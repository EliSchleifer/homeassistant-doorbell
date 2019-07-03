#!/usr/bin/env bashio

echo Starting Homeassistant Doorbell




USERNAME=$(bashio::config "username")

bashio::log.info "${USERNAME}"

IP_ADDRESS=$(bashio::config "HomeAssistantIP")

IP_ADDRESS=$(bashio::config "HomeAssistantIP")

EXISTS=$(bashio::config.exists "HomeAssistantIP")

bashio::log.info "${EXISTS}"

bashio::log.info "${IP_ADDRESS}"

bashio::log.info "$(bashio::hardware)"

pip3 install mutagen

#python3 -u doorbell-server.py
