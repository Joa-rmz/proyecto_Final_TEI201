# Código Fuente

| Archivo | Descripción |
|---|---|
| `agrosafe.py` | Programa principal: lectura de sensores, control del rociador, registro en CSV, cálculo de indicadores y dashboard Flask. |

## Estructura de `agrosafe.py`

| Sección | Funciones | Qué hace |
|---|---|---|
| Configuración | — | Pines (numeración BOARD), umbrales y rutas de archivos |
| Cámara | `foto_esp32cam()`, `tomar_foto()` | Pide una foto a la ESP32-CAM por WiFi al activarse (respaldo: cámara CSI; sin cámara el sistema sigue funcionando) |
| Sensores | `medir_distancia_cm()` | Mide distancia con el HC-SR04 (devuelve -1 si no hay eco) |
| Registro | `iniciar_csv()`, `registrar()` | Guarda cada evento en memoria y en `software/data/eventos.csv` |
| Información | `calcular_estadisticas()` | Convierte eventos en indicadores (activaciones, hora peak, alerta) |
| Lógica | `bucle_sensores()` | PIR → ultrasónico → ¿< 150 cm? → rocío 5 s → enfriamiento 8 s |
| Dashboard | `dashboard()`, `api_estadisticas()`, `descargar_csv()`, `foto()` | Interfaz web y endpoints |

## Parámetros principales

| Parámetro | Valor | Justificación |
|---|---|---|
| `DISTANCIA_MAXIMA_CM` | 150 | Solo se rocía si el objetivo está dentro del alcance de la boquilla; reduce falsas activaciones |
| `TIEMPO_ACTIVACION_S` | 5 | Rocío corto para disuadir sin desperdiciar agua |
| `TIEMPO_REPOSO_S` | 8 | Evita activaciones en cadena sobre el mismo animal |
| `INTERVALO_BEACON_S` | 5 | Registro de "reposo" que demuestra captura continua |
| Lectura del PIR | cada 0,1 s | Un conejo cruza 1,5 m en ~1 s; 10 lecturas/s aseguran no perder el evento |
| `ESP32_CAM_URL` | `http://192.168.1.50/capture` | Dirección de la ESP32-CAM; cambiar por la IP que muestra su Monitor Serie |
| `UMBRAL_ALERTA_HORA` | 5 | ≥ 5 activaciones en 1 h indica presión alta de conejos → el agricultor debe revisar el predio |

## Ejecución

```bash
cd software/src
ESP32_CAM_URL=http://<IP-ESP32-CAM>/capture python3 agrosafe.py
```
