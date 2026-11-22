# Software - AgroSafe

## 1. Descripción

El programa `src/agrosafe.py` corre en la Raspberry Pi 4 Model B y cumple el ciclo completo IoT:

**Captura → Almacena → Visualiza → Genera información → Permite decidir**

| Etapa | Implementación |
|---|---|
| Captura | PIR HC-SR501 + HC-SR04 (3 lecturas entre 15 y 50 cm) + 2 capturas de cámara con reconocimiento de la figura objetivo |
| Almacenamiento | `data/eventos.csv`: fecha, hora, tipo (detección, activación, descarte, error), mensaje y distancia. Se escribe en cada evento y se recarga al reiniciar |
| Visualización | Dashboard Flask en `http://<IP-Raspberry>:5000`, se actualiza cada 1 s |
| Información | Movimientos detectados, activaciones, descartes, % de confirmación, hora de mayor actividad, tiempo de bomba, gráfico por hora y alerta de alta actividad |
| Decisión | El agricultor sabe **cuándo** hay más actividad, **cuánta presión** hay (alerta) y **cuánta agua** se usa |

> Para la demostración, el reconocimiento por cámara detecta una **figura de estrella** que representa al conejo; el dashboard la muestra como "conejo".

## 2. Estructura de la carpeta

```
software/
├── src/agrosafe.py                       # Programa principal
├── src/agrosafe_integracion_prueba_v2.py # Cámara y reconocimiento
├── esp32cam/                             # Firmware e instrucciones de la ESP32-CAM
├── data/                                 # eventos.csv se crea aquí al ejecutar
├── requirements.txt
├── librerias/
└── docs/
```

## 3. Tecnologías

- **Plataforma:** Raspberry Pi 4 Model B (Raspberry Pi OS)
- **Lenguaje:** Python 3
- **GPIO:** gpiozero (`MotionSensor`, `DistanceSensor`, `DigitalOutputDevice`)
- **Dashboard:** Flask + servidor werkzeug en un hilo aparte
- **Cámara:** ESP32-CAM con firmware `CameraWebServer`

## 4. Funcionamiento

1. Espera movimiento del PIR.
2. Confirma con 3 lecturas del HC-SR04 que el objetivo está entre 15 y 50 cm.
3. Toma 2 capturas y verifica en ambas la figura objetivo.
4. Vuelve a verificar la distancia.
5. Si todo se cumple, activa el relé de la bomba por 2 s (`activacion`); si algo falla, registra `descarte`.
6. Pausa de 5 s y espera a que el PIR deje de detectar movimiento antes de rearmarse.

## 5. Conexiones (numeración BCM)

| Componente | GPIO | Pin físico |
|---|---:|---:|
| Sensor PIR HC-SR501 (OUT) | GPIO 17 | 11 |
| Relé de la bomba (IN) | GPIO 27 | 13 |
| TRIG del HC-SR04 | GPIO 23 | 16 |
| ECHO del HC-SR04 (con divisor de voltaje) | GPIO 24 | 18 |
| 5 V / GND | — | 2 / 6 |

## 6. Instalación y ejecución

Primero cargar el firmware de la ESP32-CAM (ver [`esp32cam/`](esp32cam/)). Luego, en la Raspberry:

```bash
sudo apt update
sudo apt install python3-flask python3-gpiozero

git clone https://github.com/Joa-rmz/proyecto_Final_TEI201.git
cd proyecto_Final_TEI201/software/src
python3 agrosafe.py
```

Abrir en el celular o computador (misma red WiFi): `http://<IP-de-la-Raspberry>:5000`. La IP se obtiene con `hostname -I`.

### Rutas del dashboard

| Ruta | Uso |
|---|---|
| `/` | Dashboard |
| `/api/estado` | Estado actual, historial de la sesión e indicadores en JSON |
| `/datos.csv` | Descarga del histórico completo |
