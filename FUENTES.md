# FUENTES.md — Declaración de Fuentes e Inteligencia Artificial

Proyecto: **AgroSafe** · TEI201 Taller de Diseño en Ingeniería · Grupo 6 · UAI

---

## 1. Librerías utilizadas

| Librería | Versión | Uso en el proyecto | Fuente |
|---|---|---|---|
| Flask | ≥ 2.2 | Servidor web del dashboard, endpoints `/api/estadisticas` y `/datos.csv` | https://github.com/pallets/flask |
| gpiozero | ≥ 1.6 | PIR (`MotionSensor`), HC-SR04 (`DistanceSensor`) y relé (`DigitalOutputDevice`) | https://github.com/gpiozero/gpiozero |
| werkzeug | incluida con Flask | Servidor web en un hilo aparte (`make_server`) | https://github.com/pallets/werkzeug |
| Núcleo ESP32 para Arduino (Espressif) | 2.x o superior | Programar la ESP32-CAM desde Arduino IDE | https://github.com/espressif/arduino-esp32 |
| csv (estándar) | Python 3 | Almacenamiento persistente de eventos | https://docs.python.org/3/library/csv.html |
| threading (estándar) | Python 3 | Ejecutar sensores y dashboard en paralelo | https://docs.python.org/3/library/threading.html |
| collections.Counter (estándar) | Python 3 | Conteo de activaciones por hora | https://docs.python.org/3/library/collections.html |

---

## 2. Código externo adaptado

### Firmware de la ESP32-CAM (ejemplo `CameraWebServer`)
- Fuente: ejemplo oficial del núcleo ESP32 para Arduino (Espressif), https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer
- Adaptación: se dejó activo solo el modelo `CAMERA_MODEL_AI_THINKER` y se configuraron el nombre y la clave de la red WiFi. No se modificó la lógica del servidor; la Raspberry obtiene las capturas con `capturar()` del módulo `agrosafe_integracion_prueba_v2.py`.

### Medición de distancia con HC-SR04
- Fuente: clase `DistanceSensor` de gpiozero, que implementa el método de la hoja de datos del HC-SR04 (pulso en TRIG y medición del eco).
- Adaptación: se configuró con `echo=24`, `trigger=23` y `max_distance=2`; las lecturas fuera de 0–200 cm se descartan y se exigen 3 lecturas seguidas entre 15 y 50 cm.

---

## 3. Uso de Inteligencia Artificial

### Programa del dispositivo (`software/src/agrosafe.py` y `agrosafe_integracion_prueba_v2.py`)
- Herramienta: ChatGPT (OpenAI), 2026.
- Uso: apoyo para escribir el programa de control: lectura del PIR y del HC-SR04 con gpiozero, verificación de distancia, reconocimiento con 2 capturas de cámara, activación del relé de la bomba y dashboard Flask con estado e historial de la sesión.
- Prompts utilizados:
  - "¿Cómo le subo el código a la Raspberry?"
  - "Mi idea es que detecte movimiento, vea que está a una distancia adecuada, active la cámara, reconozca al conejo y luego active el relé para que salga agua."
  - "Quiero que el sistema, una vez que tenga energía, pueda funcionar automáticamente."
- Adaptación: el equipo definió los pines según el montaje real (PIR GPIO 17, TRIG 23, ECHO 24, relé 27), el rango de 15–50 cm, el pulso de 2 s, la pausa de 5 s y la figura objetivo usada en la demostración.
- Comprensión: `controlar()` espera movimiento del PIR; `evaluar()` exige 3 lecturas entre 15 y 50 cm, 2 capturas en que `detectar_estrella()` reconoce la figura y una verificación final de distancia. Solo si todo se cumple, el relé enciende la bomba 2 s (con `try/finally` para asegurar que siempre se apague). Luego hay una pausa de 5 s y `esperar_rearme()` espera a que termine el movimiento para no activar dos veces por el mismo animal. El servidor Flask corre en otro hilo para que el dashboard responda durante el control.


### Modelo 3D del encapsulado (`diseno_3d/fusion360/`)
- Herramienta: Claude (Anthropic), noviembre 2026, junto con Autodesk Fusion 360.
- Uso: el equipo le entregó a Claude los requisitos del encapsulado y las medidas de los componentes reales (Raspberry Pi 4 Model B, HC-SR04, PIR HC-SR501, ESP32-CAM, relé, protoboard, batería, pila y manguera). A partir de eso, Claude ayudó a crear el modelo 3D de las 6 piezas (base, tapa, bandeja, placa soporte del protoboard, torreta y tapa de torreta) y el ensamble con los componentes, que luego se trabajó en Fusion 360 y se exportó como `Montaje con componentes.step` y piezas STL.
- Requisitos definidos por el equipo: encapsulado de dos cuerpos (base fija y torreta con sensores arriba), tapa removible con tornillos para reparación, ventilación, paso de manguera y aberturas para cada sensor y la cámara.
- Adaptación: el equipo revisó en Fusion 360 que cada componente cupiera y realizó cambios según los requerimientos que se fueron encontrando.
- Comprensión: la base aloja la electrónica y tiene ventana de servicio y rejilla de ventilación; la tapa se fija con 4 tornillos M3 para poder abrirla en reparaciones; la bandeja sostiene la Raspberry Pi 4 con su patrón de 58 × 49 mm; la torreta ubica los sensores con aberturas a su medida.

### Planos técnicos y renders (`diseno_3d/planos/` y `diseno_3d/renders/`)
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: a partir del archivo STEP del modelo, generó los planos A3 (vistas ortogonales, cortes, cotas, tolerancias y cajetín) y los renders exterior, explosionado e interior.
- Adaptación: el equipo revisó que las cotas coincidieran con el modelo de Fusion 360.

### Documentación del repositorio
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: ayuda en la redacción de los README.
- Adaptación: los datos técnicos (componentes, conexiones, dimensiones, problema y contexto) provienen del trabajo del equipo.

### Esquemático y simulación de pruebas (`hardware/esquemas/` y `testing/`)
- Herramienta: Claude (Anthropic), noviembre 2026.
- Uso: dibujó el esquemático eléctrico a partir de las conexiones del equipo, y escribió `testing/simulacion/simulacion.py`, que ejecuta el programa real con sensores simulados e imágenes sintéticas para medir la lógica de activación, la latencia y la persistencia. La captura `dashboard_simulacion.png` es el dashboard real del programa después de esa simulación.
- Adaptación: el equipo revisó que el esquemático coincidiera con el cableado de las fotos de `hardware/fotos/`.
