#!/usr/bin/env bashio

bashio::log.yellow "Booting up..."

IP_ADDRESS=$(bashio::config "ip_address")
bashio::log.info "Configured to  use ${IP_ADDRESS} as root IP"

FILE_ROOT=$(bashio::config "file_root")
bashio::log.info "Serving audio files from ${FILE_ROOT}"

pip install mutagen

python -u doorbell-server.py --ip ${IP_ADDRESS:-\"\"} --file_root ${FILE_ROOT:-\"\"}
