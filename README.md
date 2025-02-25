# Temperaturepi
### Temperaturmessung und Not-Aus bei Überhitzung des Serverraums

## 1. Headless installation & Config des Pi OS
- SD-Karte aus dem Rpi ziehen 
- Download & Install Pi Imager (https://downloads.raspberrypi.org/imager/imager_latest.exe)
- Model Rpi 4; Raspberry Pi OS Lite (64-Bit)
- Einstellungen bearbeiten:
    - hostname: killswitch.local
    - username: postpro
    - password: ***
    - Zeitzone: Europe/Berlin
    - Tastaturlayout: de
    - Configure Wifi
    - Dienste: SSH Aktivieren
- SD Karte in den RasperryPi stecken & Booten (ca. 5min warten)
- Vom Arbeitsplatz via ssh verbinden:
    - ```ssh postpro@killswitch```

## 2. Install Python Script
Install sense-hat:
```
sudo apt-get update
sudo apt-get install sense-hat python3-paramiko

sudo reboot
```