#!/usr/bin/env bashio

IP_ADDRESS=$(bashio::config "ip_address")
bashio::log.info "${IP_ADDRESS}"

pip install mutagen

python -u doorbell-server.py
