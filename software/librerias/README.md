# Librerías

No se usan librerías modificadas; todas se instalan desde los repositorios de Raspberry Pi OS.

| Librería | Versión mínima | Uso | Instalación |
|---|---|---|---|
| Flask | 2.2 | Dashboard web, API y descarga del CSV | `sudo apt install python3-flask` |
| werkzeug | (incluida con Flask) | Servidor web en un hilo aparte (`make_server`) | Incluida con Flask |
| gpiozero | 1.6 | PIR (`MotionSensor`), HC-SR04 (`DistanceSensor`) y relé (`DigitalOutputDevice`) | `sudo apt install python3-gpiozero` |
| Núcleo ESP32 para Arduino (Espressif) | 2.x o superior | Firmware `CameraWebServer` de la ESP32-CAM | Arduino IDE → Gestor de placas → "esp32" |
| csv, threading, datetime, collections, os | Estándar de Python | Almacenamiento, concurrencia y estadísticas | Incluidas en Python 3 |

Ver también `../requirements.txt` y `/FUENTES.md`.
