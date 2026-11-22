# Librerías

No se usan librerías modificadas; todas se instalan desde los repositorios de Raspberry Pi OS.

| Librería | Versión mínima | Uso | Instalación |
|---|---|---|---|
| Flask | 2.2 | Dashboard web y descarga del CSV | `sudo apt install python3-flask` |
| RPi.GPIO | 0.7 | Lectura del PIR/ultrasónico y control del LED/relé | `sudo apt install python3-rpi.gpio` |
| picamera2 | — (opcional) | Foto al detectar | `sudo apt install python3-picamera2` |
| csv, threading, datetime, collections | Estándar de Python | Almacenamiento, concurrencia y estadísticas | Incluidas en Python 3 |

Ver también `../requirements.txt` y `/FUENTES.md`.
