# ESP32-CAM — Cámara de confirmación

La ESP32-CAM (AI-Thinker, sensor OV2640) se conecta a la misma red WiFi que la Raspberry Pi 4 Model B. Cuando el PIR y el ultrasónico detectan un objetivo, `agrosafe.py` toma 2 capturas y verifica en ambas la figura objetivo antes de activar la bomba.

```
Raspberry Pi 4 Model B  --(WiFi, captura)-->  ESP32-CAM  --> imagen --> reconocimiento --> relé de la bomba
```

## Firmware

Se usa el ejemplo **CameraWebServer** del núcleo ESP32 para Arduino (Espressif), configurado para el módulo AI-Thinker.

## Cargar el firmware

1. **Arduino IDE:** instalar el núcleo ESP32 (Herramientas → Placa → Gestor de placas → buscar "esp32" de Espressif).
2. **Abrir el ejemplo:** Archivo → Ejemplos → ESP32 → Camera → `CameraWebServer`.
3. **Configurar:**
   - Dejar activo solo `#define CAMERA_MODEL_AI_THINKER`.
   - Escribir el nombre y la clave de la red WiFi en `ssid` y `password`.
4. **Placa:** Herramientas → Placa → `AI Thinker ESP32-CAM`.
5. **Conectar el programador USB-serie (FTDI o placa base ESP32-CAM-MB):**

   | FTDI | ESP32-CAM |
   |---|---|
   | 5 V | 5V |
   | GND | GND |
   | TX | U0R (GPIO 3) |
   | RX | U0T (GPIO 1) |
   | — | **GPIO 0 a GND** (solo para cargar) |

6. **Subir el programa.** Al terminar, quitar el puente GPIO 0–GND y presionar RESET.
7. **Obtener la IP:** abrir el Monitor Serie a 115200 baudios. Aparece `Camera Ready! Use 'http://192.168.x.x'`.

## Probar

- `http://<IP-ESP32-CAM>/capture` → debe mostrar una foto.
- `http://<IP-ESP32-CAM>` → página de control con video en vivo (útil para ajustar el ángulo).

## Conectar con la Raspberry

La Raspberry obtiene las capturas de la ESP32-CAM mediante el módulo `software/src/agrosafe_integracion_prueba_v2.py` (función `capturar()`), que se usa en cada evaluación de `agrosafe.py`.

> Recomendación: reservar una IP fija para la ESP32-CAM en el router, así no cambia entre sesiones.

## Alimentación
- 5 V con al menos 500 mA (los picos al transmitir por WiFi reinician el módulo si la fuente es débil).
- `[COMPLETAR: alimentada desde la misma batería / otra fuente]`
