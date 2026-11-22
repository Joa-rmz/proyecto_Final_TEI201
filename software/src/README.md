# Código Fuente

| Archivo | Descripción |
|---|---|
| `agrosafe.py` | Programa del dispositivo: control de sensores y bomba, reconocimiento por cámara, registro en CSV, indicadores y dashboard Flask |
| `agrosafe_integracion_prueba_v2.py` | Módulo de cámara y reconocimiento (`capturar()`, `detectar_estrella()`), requerido por `agrosafe.py` |

## Estructura de `agrosafe.py`

| Sección | Funciones | Qué hace |
|---|---|---|
| Estado y registro | `actualizar()`, `registrar()` | Estado actual para el dashboard; cada evento se guarda en el historial y en `software/data/eventos.csv` |
| Repositorio de datos | `iniciar_csv()`, `calcular_estadisticas()` | Crea o recarga el CSV y calcula los indicadores del día |
| Sensores | `leer_sensores()`, `comprobar_distancia()` | Lee PIR y HC-SR04; confirma con 3 lecturas que el objetivo está entre 15 y 50 cm |
| Decisión | `evaluar()` | Distancia → 2 capturas con reconocimiento → distancia final; solo si todo se cumple se activa |
| Control | `controlar()`, `esperar()`, `esperar_rearme()` | Ciclo principal: espera movimiento, evalúa, pulso de bomba de 2 s, pausa de 5 s y rearme del PIR |
| Dashboard | `inicio()`, `datos()`, `descargar_csv()` | Página web, API `/api/estado` y descarga `/datos.csv` |

## Parámetros principales

| Parámetro | Valor | Justificación |
|---|---|---|
| Rango de activación | 15–50 cm (3 lecturas seguidas) | Evita activar por objetos lejanos o lecturas aisladas erróneas |
| Confirmación por cámara | 2 capturas positivas | Reduce falsas activaciones por otros animales o movimiento |
| Pulso de bomba | 2 s | Disuade sin desperdiciar agua |
| Pausa tras cada intento | 5 s + rearme del PIR | Evita activaciones en cadena sobre el mismo animal |
| Lectura de sensores | cada 0,2 s | Suficiente para seguir el movimiento de un animal pequeño |
| `UMBRAL_ALERTA_HORA` | 5 | ≥ 5 activaciones en 1 h indica alta presión → el agricultor debe revisar el predio |

## Ejecución

```bash
cd software/src
python3 agrosafe.py
```
