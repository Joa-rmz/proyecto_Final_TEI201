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

### Modelo 3D del encapsulado (diseno_3d/fusion360/)
- Herramienta: Claude (Anthropic), noviembre 2026, junto con Autodesk Fusion 360.
- Uso: el equipo le entregó a Claude los requisitos del encapsulado y las medidas de los componentes reales (Raspberry Pi 4 Model B, HC-SR04, PIR HC-SR501, ESP32-CAM, relé, protoboard, batería, pila y manguera). A partir de eso, Claude ayudó a crear el modelo 3D de las 6 piezas (base, tapa, bandeja, placa soporte del protoboard, torreta y tapa de torreta) y el ensamble con los componentes, que luego se trabajó en Fusion 360 y se exportó como `AgroSafe_montaje_completo_con_componentes.step` y piezas STL.
- Requisitos definidos por el equipo: encapsulado de dos cuerpos (base fija y torreta con sensores arriba), tapa removible con tornillos para reparación, ventilación, paso de manguera y aberturas para cada sensor y la cámara.
- Adaptación: el equipo revisó en Fusion 360 que cada componente cupiera y [completar: ajustes que hicieron, p. ej. holguras, posición de sensores, espesores].
- Comprensión: la base aloja la electrónica y tiene ventana de servicio y rejilla de ventilación; la tapa se fija con 4 tornillos M3 para poder abrirla en reparaciones; la bandeja sostiene la Raspberry Pi 4 con su patrón de 58 × 49 mm; la torreta ubica los sensores con aberturas a su medida.

### Planos técnicos y renders (diseno_3d/planos/ y diseno_3d/renders/)
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: a partir del archivo STEP del modelo, generó los planos A3 (vistas ortogonales, cortes, cotas, tolerancias y cajetín) y los renders exterior, explosionado e interior.
- Adaptación: el equipo revisó que las cotas coincidieran con el modelo de Fusion 360.
