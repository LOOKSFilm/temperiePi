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
```
sudo apt-get update
sudo apt-get install git sense-hat python3-paramiko
git clone https://github.com/LOOKSFilm/temperiePi.git
chmod +x temperiePi/temperiePi.sh
```
#### Add script to Autostart
```crontab -e``` select 1 (nano editor)
```
@reboot /home/postpro/temperiePi/temperiePi.sh
```
am ende der Datei hinzufügen 
save: strg+s
exit: strg+x

## 3. Configure Lan
#### (notwendig 10.0.77.xx hat kein dhcp)
``` sh 
    sudo nmcli con add type ethernet ifname eth0 con-name eth0
    sudo nmcli con modify eth0 ipv4.addresses 10.0.77.112/24
    sudo nmcli con modify eth0 ipv4.gateway 10.0.77.13
    sudo nmcli con modify eth0 ipv4.dns 10.0.77.13
    sudo nmcli con modify eth0 ipv4.method manual
    sudo nmcli con down eth0
    sudo nmcli con up eth0
```

Jetzt nur noch neustarten ```sudo reboot``` und der temperiePi ist eingerichtet!


#### Logfile
Das Script loggt die Temperatur in einem logfile
```cat /home/postpro/temperiePi/temperature_log.json```