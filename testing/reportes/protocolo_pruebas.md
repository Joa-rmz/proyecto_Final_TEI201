# Protocolo de Pruebas — AgroSafe (Avance 3)

> Las tablas de resultados están vacías: completarlas con las mediciones reales del equipo. No inventar datos.

---

## Prueba 1 — Precisión del sensor ultrasónico

| Campo | Detalle |
|---|---|
| **Objetivo** | Verificar que el HC-SR04 mide correctamente la distancia que decide si se rocía. |
| **Condiciones** | Interior, objeto plano de `[COMPLETAR]` cm, sensor fijo en la torreta. |
| **Procedimiento** | 1. Ubicar el objeto a 15, 25, 35, 50 y 80 cm (medido con huincha). 2. Tomar 10 lecturas en cada distancia desde `/api/estado` o el CSV. 3. Calcular promedio y error. |
| **Criterio de éxito** | Error promedio ≤ 3 cm entre 15 y 50 cm. |

| Distancia real (cm) | Promedio medido (cm) | Error abs. (cm) | Error (%) |
|---|---|---|---|
| 15 | | | |
| 25 | | | |
| 35 | | | |
| 50 | | | |
| 80 | | | |

---

## Prueba 2 — Lógica de activación / descarte

| Campo | Detalle |
|---|---|
| **Objetivo** | Comprobar que la bomba solo se activa con la figura objetivo entre 15 y 50 cm. |
| **Procedimiento** | 1. Presentar 10 veces la figura a ~30 cm, 10 veces a ~80 cm y 10 veces otro objeto a ~30 cm. 2. Registrar el resultado en el dashboard. |
| **Criterio de éxito** | ≥ 9/10 activaciones con la figura cerca y ≥ 9/10 descartes en los otros dos casos. |

| Escenario | Intentos | Activado | Descartado | Sin detección | Tasa de acierto |
|---|---|---|---|---|---|
| Figura a ~30 cm | 10 | | | | |
| Figura a ~80 cm | 10 | | | | |
| Otro objeto a ~30 cm | 10 | | | | |

---

## Prueba 3 — Latencia

| Campo | Detalle |
|---|---|
| **Objetivo** | Medir el tiempo desde el movimiento hasta (a) el encendido de la bomba y (b) la aparición en el dashboard. |
| **Procedimiento** | Grabar en video el movimiento, la bomba y la pantalla del dashboard; contar frames. 5 repeticiones. |
| **Criterio de éxito** | Bomba < 5 s (incluye 3 lecturas de distancia y 2 capturas); dashboard < 2 s (refresco cada 1 s). |

| Repetición | Movimiento → bomba (s) | Movimiento → dashboard (s) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| **Promedio** | | |

---

## Prueba 4 — Captura continua y persistencia

| Campo | Detalle |
|---|---|
| **Objetivo** | Demostrar que el sistema registra sin interrupciones y que los datos sobreviven a un reinicio. |
| **Procedimiento** | 1. Dejar el sistema funcionando `[COMPLETAR]` horas. 2. Generar N movimientos y contar que cada uno tenga su fila en `eventos.csv`. 3. Desconectar la energía, reiniciar y verificar que los indicadores del día siguen en el dashboard. |
| **Criterio de éxito** | 100 % de los eventos registrados; 0 datos perdidos tras reinicio. |

| Duración (h) | Eventos generados | Filas en CSV | % registrados | ¿Datos tras reinicio? |
|---|---|---|---|---|
| | | | | |

---

## Prueba 5 — Autonomía de la batería

| Duración total (h) | Consumo medido (mA) | Observaciones |
|---|---|---|
| | | |

---

## Análisis de fallas

| Falla encontrada | Causa | Solución aplicada | Resultado |
|---|---|---|---|
| Falsas activaciones con solo PIR (Avance 2) | El PIR detecta cualquier calor en movimiento a 3–7 m | Se agregó el HC-SR04 (15–50 cm) y la confirmación con 2 capturas de cámara | `[COMPLETAR con datos de Prueba 2]` |
| ECHO conectado directo a 5 V (Avance 2) | Riesgo de dañar el GPIO de 3,3 V | Divisor de voltaje | Sin daños en la Raspberry |
| Datos se perdían al reiniciar | Eventos solo en memoria (últimos 50) | Escritura en `eventos.csv` en cada evento | `[COMPLETAR con Prueba 4]` |
| `[COMPLETAR: falla nueva de Avance 3]` | | | |

**Propuestas de mejora:** `[COMPLETAR, p. ej. confirmación por cámara para distinguir conejos de perros, protección IP del encapsulado]`

---

## Validación contra el problema original (Avance 1)

En el Avance 1 se identificó que los agricultores del Valle del Choapa enfrentan entre 200 y 300 conejos por predio y no tienen una forma no letal de proteger sus cultivos ni información sobre **cuándo** ocurren los ataques.

| Necesidad del Avance 1 | Cómo la responde AgroSafe | Evidencia |
|---|---|---|
| Detectar la presencia de conejos | PIR + ultrasónico | Pruebas 1 y 2 |
| Ahuyentar sin dañar | Rocío de agua de 2 s | Prueba 2 |
| Saber cuándo atacan | Gráfico por hora y hora peak en el dashboard | `[COMPLETAR: captura del gráfico tras N noches]` |
| No desperdiciar agua | Rocío solo con objetivo confirmado entre 15 y 50 cm; contador de segundos de bomba | `[COMPLETAR: segundos de rocío por noche]` |

**Conclusión:** `[COMPLETAR, p. ej. "Durante X noches el sistema registró N activaciones, con peak entre las HH y HH. Esto permite al agricultor..."]`
