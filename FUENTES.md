# FUENTES.md — Declaración de Fuentes e Inteligencia Artificial

Proyecto: **AgroSafe** · TEI201 Taller de Diseño en Ingeniería · Grupo 6 · UAI

---

## 1. Librerías utilizadas

| Librería | Versión | Uso en el proyecto | Fuente |
|---|---|---|---|
| Flask | ≥ 2.2 | Servidor web del dashboard, endpoints `/api/estadisticas` y `/datos.csv` | https://github.com/pallets/flask |
| RPi.GPIO | ≥ 0.7 | Lectura del PIR y del HC-SR04; control del LED/relé | https://sourceforge.net/projects/raspberry-gpio-python/ |
| picamera2 | — (opcional) | Captura de foto con cámara CSI como respaldo | https://github.com/raspberrypi/picamera2 |
| urllib.request (estándar) | Python 3 | Pedir la foto a la ESP32-CAM por HTTP | https://docs.python.org/3/library/urllib.request.html |
| Núcleo ESP32 para Arduino (Espressif) | 2.x o superior | Programar la ESP32-CAM desde Arduino IDE | https://github.com/espressif/arduino-esp32 |
| csv (estándar) | Python 3 | Almacenamiento persistente de eventos | https://docs.python.org/3/library/csv.html |
| threading (estándar) | Python 3 | Ejecutar sensores y dashboard en paralelo | https://docs.python.org/3/library/threading.html |
| collections.Counter (estándar) | Python 3 | Conteo de activaciones por hora | https://docs.python.org/3/library/collections.html |

---

## 2. Código externo adaptado

### Firmware de la ESP32-CAM (ejemplo `CameraWebServer`)
- Fuente: ejemplo oficial del núcleo ESP32 para Arduino (Espressif), https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer
- Adaptación: se dejó activo solo el modelo `CAMERA_MODEL_AI_THINKER` y se configuraron el nombre y la clave de la red WiFi. No se modificó la lógica del servidor: la Raspberry usa su ruta `/capture` para obtener una foto en cada activación.

### Medición de distancia con HC-SR04 (`medir_distancia_cm()` en `software/src/agrosafe.py`)
- Fuente: método de medición de la hoja de datos del HC-SR04 (pulso de 10 µs en TRIG y medición del ancho del pulso en ECHO; distancia = tiempo × 34300 / 2).
- Adaptación: se usa `time.monotonic()` y se agregó un tiempo límite de 50 ms que devuelve `-1` si no hay eco, para que el programa no se quede bloqueado esperando la señal.

---

## 3. Uso de Inteligencia Artificial

### Código base del sistema — Avance 2 (`software/src/agrosafe.py`)
- Herramienta: ChatGPT (OpenAI), octubre 2026.
- Uso: apoyo para escribir la primera versión del programa: configuración de pines, lectura del PIR, medición con el HC-SR04, lógica de activación del rociador (distancia < 150 cm, rocío de 5 s, enfriamiento de 8 s) y el primer dashboard en Flask con la tabla de eventos.
- Prompt utilizado: [completar con el prompt que usaron en ChatGPT]
- Adaptación: el equipo definió los pines según el montaje real (GPIO 17, 18, 23 y 24), los tiempos de activación y enfriamiento, y el umbral de 150 cm según el alcance de la boquilla.
- Comprensión: `bucle_sensores()` revisa el PIR cada 0,1 s; cuando detecta movimiento, mide la distancia y, si el objeto está a menos de 150 cm, enciende el rociador 5 s y espera 8 s antes de permitir otra activación. El PIR debe quedar 1 s en reposo antes de rearmarse, para no activar varias veces con la misma detección. Flask y los sensores corren en hilos separados (`threading`) para que el dashboard responda mientras se mide.

### Almacenamiento, indicadores y ESP32-CAM — Avance 3 (`software/src/agrosafe.py`)
- Herramienta: Claude (Anthropic), noviembre 2026.
- Prompts utilizados: "necesito que realices el GitHub con las siguientes infos" (se entregó la pauta del Avance 3 y el código del Avance 2) y "falta el ESP-32 con cámara en los componentes y para la instalación y uso también debe estar".
- Funciones generadas: `iniciar_csv()`, `registrar()` (escritura en CSV), `calcular_estadisticas()`, `grafico_por_hora()`, `foto_esp32cam()`, `tomar_foto()` (ESP32-CAM con respaldo CSI), las rutas `/api/estadisticas` y `/datos.csv`, y la sección de indicadores, gráfico y alerta del dashboard.
- Adaptación: se mantuvo sin cambios la lógica de sensores del equipo (pines, 150 cm, 5 s, 8 s). Se cambió la plataforma a Raspberry Pi 4 Model B y se agregó la ESP32-CAM según el hardware real del equipo.
- Comprensión: `registrar()` abre `eventos.csv` en modo *append* y escribe una fila por evento (fecha, hora, estado, distancia, foto), así el dato no se pierde si se corta la energía. `iniciar_csv()` crea el archivo con encabezado o, si ya existe, recarga las detecciones anteriores. `calcular_estadisticas()` filtra los eventos del día, cuenta activaciones y descartes, calcula el % de confirmación (activaciones / detecciones totales), agrupa por hora con `Counter` para obtener la hora de mayor actividad y activa la alerta si hay 5 o más activaciones en los últimos 60 minutos. `foto_esp32cam()` hace una petición HTTP a la ruta `/capture` de la ESP32-CAM y guarda la imagen; si la cámara no responde en 3 s, el sistema sigue funcionando sin foto. Se probó con sensores simulados: con 6 activaciones y 1 descarte, el dashboard mostró la alerta y la API devolvió 85,7 % de confirmación.

### Modelo 3D del encapsulado (`diseno_3d/fusion360/`)
- Herramienta: Claude (Anthropic), noviembre 2026, junto con Autodesk Fusion 360.
- Uso: el equipo le entregó a Claude los requisitos del encapsulado y las medidas de los componentes reales (Raspberry Pi 4 Model B, HC-SR04, PIR HC-SR501, ESP32-CAM, relé, protoboard, batería, pila y manguera). A partir de eso, Claude ayudó a crear el modelo 3D de las 6 piezas (base, tapa, bandeja, placa soporte del protoboard, torreta y tapa de torreta) y el ensamble con los componentes, que luego se trabajó en Fusion 360 y se exportó como `AgroSafe_montaje_completo_con_componentes.step` y piezas STL.
- Requisitos definidos por el equipo: encapsulado de dos cuerpos (base fija y torreta con sensores arriba), tapa removible con tornillos para reparación, ventilación, paso de manguera y aberturas para cada sensor y la cámara.
- Adaptación: el equipo revisó en Fusion 360 que cada componente cupiera y realizó cambios según los requerimientos que se fueron encontrando.
- Comprensión: la base aloja la electrónica y tiene ventana de servicio y rejilla de ventilación; la tapa se fija con 4 tornillos M3 para poder abrirla en reparaciones; la bandeja sostiene la Raspberry Pi 4 con su patrón de 58 × 49 mm; la torreta ubica los sensores con aberturas a su medida.

### Planos técnicos y renders (`diseno_3d/planos/` y `diseno_3d/renders/`)
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: a partir del archivo STEP del modelo, generó los planos A3 (vistas ortogonales, cortes, cotas, tolerancias y cajetín) y los renders exterior, explosionado e interior.
- Adaptación: el equipo revisó que las cotas coincidieran con el modelo de Fusion 360.

### Documentación del repositorio
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: redacción de los README de cada carpeta, el BOM, el protocolo de pruebas y las instrucciones de la ESP32-CAM, a partir de la pauta del Avance 3, la presentación del Avance 2 y la información entregada por el equipo.
- Adaptación: los datos técnicos (componentes, conexiones, dimensiones, problema y contexto) provienen del trabajo del equipo; los precios del BOM y los resultados de las pruebas los completa el equipo con mediciones reales.
