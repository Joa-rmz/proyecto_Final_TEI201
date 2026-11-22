# Librerías

No se usan librerías modificadas; todas se instalan desde los repositorios de Raspberry Pi OS.

| Librería | Versión mínima | Uso | Instalación |
|---|---|---|---|
| Flask | 2.2 | Dashboard web y descarga del CSV | `sudo apt install python3-flask` |
| RPi.GPIO | 0.7 | Lectura del PIR/ultrasónico y control del LED/relé | `sudo apt install python3-rpi.gpio` |
| picamera2 | — (opcional) | Foto al detectar | `sudo apt install python3-picamera2` |
| urllib (estándar) | Python 3 | Pedir la foto a la ESP32-CAM | Incluida en Python 3 |
| Núcleo ESP32 para Arduino (Espressif) | 2.x o superior | Firmware `CameraWebServer` de la ESP32-CAM | Arduino IDE → Gestor de placas → "esp32" |
| csv, threading, datetime, collections | Estándar de Python | Almacenamiento, concurrencia y estadísticas | Incluidas en Python 3 |

Ver también `../requirements.txt` y `/FUENTES.md`.
