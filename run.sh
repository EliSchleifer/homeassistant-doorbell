#!/usr/bin/env bashio

bashio::log.yellow "Booting up..."

IP_ADDRESS=$(bashio::config "ip_address")
bashio::log.info "CONFIG ip_address: ${IP_ADDRESS}"

FILE_ROOT=$(bashio::config "file_root")
bashio::log.info "CONFIG file_root: ${FILE_ROOT}"

pip install mutagen

python -u doorbell-server.py --ip ${IP_ADDRESS:-\"\"} --file_root ${FILE_ROOT:-\"\"}
