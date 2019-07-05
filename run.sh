#!/usr/bin/env bashio

bashio::log.yellow "Booting up..."

IP_ADDRESS=$(bashio::config "ip_address")
bashio::log.info "Configured to  use ${IP_ADDRESS} as root IP"

pip install mutagen

python -u doorbell-server.py 
