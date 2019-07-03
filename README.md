# homeassistant-doorbell
HTTP driven doorbell chime

This project was created in order to serve custom MP3 files to a home automation Doorbell system. Directly hosting
MP3 files on a HomeAssistant box can cause problems when Sonos (or other players) cannot authenticate the TLS/SSL
certificate that is used. This simple project exposes a local HTTP server (without https). It also does a little
throttling so if a call comes in while the previous song would theoretically be playing...it rejects the request.


### Home Assistant
1. TODO: Setup system to provide well named songs and list of dates. So on birthdays birthday song can be played..etc...

