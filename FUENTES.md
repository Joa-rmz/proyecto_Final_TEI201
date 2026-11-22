# FUENTES.md — Declaración de Fuentes e Inteligencia Artificial

Proyecto: **AgroSafe** · TEI201 Taller de Diseño en Ingeniería · Grupo 6 · UAI

> **Equipo:** revisar y completar las secciones marcadas con `[COMPLETAR]` antes de la presentación. Todos los integrantes deben poder explicar cada función de `agrosafe.py`.

---

## 1. Librerías utilizadas

| Librería | Versión | Uso en el proyecto | Fuente |
|---|---|---|---|
| Flask | ≥ 2.2 | Servidor web del dashboard, endpoints `/api/estadisticas` y `/datos.csv` | https://github.com/pallets/flask |
| RPi.GPIO | ≥ 0.7 | Lectura del PIR y del HC-SR04; control del LED/relé | https://sourceforge.net/projects/raspberry-gpio-python/ |
| picamera2 | — (opcional) | Captura de foto al activarse el rociador | https://github.com/raspberrypi/picamera2 |
| urllib.request (estándar) | Python 3 | Pedir la foto a la ESP32-CAM por HTTP | https://docs.python.org/3/library/urllib.request.html |
| Núcleo ESP32 para Arduino (Espressif) | `[COMPLETAR versión]` | Programar la ESP32-CAM | https://github.com/espressif/arduino-esp32 |
| csv (estándar) | Python 3 | Almacenamiento persistente de eventos | https://docs.python.org/3/library/csv.html |
| threading (estándar) | Python 3 | Ejecutar sensores y dashboard en paralelo | https://docs.python.org/3/library/threading.html |
| collections.Counter (estándar) | Python 3 | Conteo de activaciones por hora | https://docs.python.org/3/library/collections.html |

---

## 2. Código externo adaptado

### Medición de distancia con HC-SR04 (`medir_distancia_cm()` en `software/src/agrosafe.py`)
- Fuente: patrón estándar TRIG/ECHO para HC-SR04 en Raspberry Pi. `[COMPLETAR: URL del tutorial que usaron, p. ej. The Pi Hut / Random Nerd Tutorials]`
- Adaptación: se usa `time.monotonic()` en vez de `time.time()` y se agregó un tiempo límite de 50 ms que devuelve `-1` si no hay eco, para que el programa no se quede bloqueado.

### Firmware de la ESP32-CAM (ejemplo `CameraWebServer`)
- Fuente: ejemplo oficial del núcleo ESP32 para Arduino, https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer
- Adaptación: se seleccionó `CAMERA_MODEL_AI_THINKER` y se configuró la red WiFi. `[COMPLETAR: otros cambios, p. ej. resolución]`. La Raspberry usa su endpoint `/capture` para obtener una foto en cada activación.

### Divisor de voltaje para ECHO (5 V → 3,3 V)
- Fuente: `[COMPLETAR]`
- Adaptación: `[COMPLETAR: valores de resistencias usados]`

---

## 3. Uso de Inteligencia Artificial

### Código base del sistema (Avance 2: sensores, lógica y dashboard)
- Herramienta: `[COMPLETAR: herramienta y fecha, o eliminar si fue escrito por el equipo]`
- Uso: `[COMPLETAR]`
- Comprensión: `[COMPLETAR]`

### Almacenamiento persistente y generación de información (Avance 3)
Funciones `foto_esp32cam()`, `iniciar_csv()`, `registrar()` (escritura a CSV), `calcular_estadisticas()`, `grafico_por_hora()`, endpoints `/api/estadisticas` y `/datos.csv`, y sección de indicadores/alerta del dashboard.
- Herramienta: Claude (Anthropic), noviembre 2026
- Prompt utilizado: "Realiza el GitHub con la información del Avance 3 siguiendo la estructura del repositorio de referencia" (se entregó la pauta del Avance 3 y el código existente del Avance 2).
- Adaptación: se mantuvo intacta la lógica de sensores del equipo (pines, umbral de 150 cm, rocío de 5 s, enfriamiento de 8 s). Se agregó el guardado en CSV y los indicadores pedidos por la pauta. `[COMPLETAR: ajustes que haga el equipo, p. ej. umbral de alerta]`
- Comprensión: `registrar()` abre `eventos.csv` en modo *append* y escribe una fila por evento, así el dato no se pierde si se corta la energía. `iniciar_csv()` crea el archivo con encabezado o, si ya existe, recarga las detecciones previas. `calcular_estadisticas()` filtra los eventos del día, cuenta activados y descartados, calcula el % de confirmación (activados / total de detecciones), agrupa por hora con `Counter` para obtener la hora peak, y activa la alerta si hay ≥ 5 activaciones en los últimos 60 minutos. Se probó con un GPIO simulado registrando 6 activaciones y 1 descarte: el dashboard mostró la alerta y la API devolvió 85,7 % de confirmación. `[COMPLETAR: prueba en la Raspberry real]`

### Documentación del repositorio
- Herramienta: Claude (Anthropic), noviembre 2026
- Uso: redacción de los README, FUENTES.md, BOM y protocolo de pruebas a partir de la pauta del Avance 3, la presentación del Avance 2 y el README existente. Los datos técnicos (componentes, dimensiones, pines, problema) provienen del trabajo del equipo; los resultados de pruebas y costos los completa el equipo.
