#!/usr/bin/env bashio

echo Starting Homeassistant Doorbell

pip3 install mutagen


USERNAME=$(bashio::config 'username')

bashio::log.info "${USERNAME}"

bashio::config.info "${USERNAME}"

bashio::log.info "$(bashio::hardware)"

python3 -u doorbell-server.py
