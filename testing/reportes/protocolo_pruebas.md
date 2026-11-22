# Protocolo de Pruebas — AgroSafe (Avance 3)

> ⚠️ Las tablas de resultados están vacías: completarlas con las mediciones reales del equipo. No inventar datos.

---

## Prueba 1 — Precisión del sensor ultrasónico

| Campo | Detalle |
|---|---|
| **Objetivo** | Verificar que el HC-SR04 mide correctamente la distancia que decide si se rocía. |
| **Condiciones** | Interior, objeto plano de `[COMPLETAR]` cm, sensor fijo en la torreta. |
| **Procedimiento** | 1. Ubicar el objeto a 30, 60, 100, 140 y 200 cm (medido con huincha). 2. Tomar 10 lecturas en cada distancia desde `/api/estadisticas` o el CSV. 3. Calcular promedio y error. |
| **Criterio de éxito** | Error promedio ≤ 3 cm bajo 150 cm. |

| Distancia real (cm) | Promedio medido (cm) | Error abs. (cm) | Error (%) |
|---|---|---|---|
| 30 | | | |
| 60 | | | |
| 100 | | | |
| 140 | | | |
| 200 | | | |

---

## Prueba 2 — Lógica de activación / descarte

| Campo | Detalle |
|---|---|
| **Objetivo** | Comprobar que el rociador solo se activa si el objetivo está a < 150 cm. |
| **Procedimiento** | 1. Generar 10 movimientos a ~80 cm y 10 a ~250 cm. 2. Registrar el estado en el dashboard. |
| **Criterio de éxito** | ≥ 9/10 "activado" cerca y ≥ 9/10 "descartado" lejos. |

| Escenario | Intentos | Activado | Descartado | Sin detección | Tasa de acierto |
|---|---|---|---|---|---|
| Cerca (~80 cm) | 10 | | | | |
| Lejos (~250 cm) | 10 | | | | |

---

## Prueba 3 — Latencia

| Campo | Detalle |
|---|---|
| **Objetivo** | Medir el tiempo desde el movimiento hasta (a) el encendido del LED y (b) la aparición en el dashboard. |
| **Procedimiento** | Grabar en video (cámara lenta) el movimiento, el LED y la pantalla del dashboard; contar frames. 5 repeticiones. |
| **Criterio de éxito** | LED < 1 s; dashboard < 3 s (refresco cada 2 s). |

| Repetición | Movimiento → LED (s) | Movimiento → dashboard (s) |
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
| **Procedimiento** | 1. Dejar el sistema funcionando `[COMPLETAR]` horas. 2. Contar filas "reposo" en `eventos.csv` (esperado: 1 cada 5 s = 720/hora). 3. Desconectar la energía, reiniciar y verificar que el histórico sigue en el dashboard. |
| **Criterio de éxito** | ≥ 95 % de los registros esperados; 0 datos perdidos tras reinicio. |

| Duración (h) | Registros esperados | Registros obtenidos | % captura | ¿Datos tras reinicio? |
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
| Falsas activaciones con solo PIR (Avance 2) | El PIR detecta cualquier calor en movimiento a 3–7 m | Se agregó el HC-SR04 y la condición < 150 cm | `[COMPLETAR con datos de Prueba 2]` |
| ECHO conectado directo a 5 V (Avance 2) | Riesgo de dañar el GPIO de 3,3 V | Divisor de voltaje | Sin daños en la Raspberry |
| Datos se perdían al reiniciar (Avance 2) | Eventos solo en memoria (lista de 30) | Escritura en `eventos.csv` en cada evento | `[COMPLETAR con Prueba 4]` |
| `[COMPLETAR: falla nueva de Avance 3]` | | | |

**Propuestas de mejora:** `[COMPLETAR, p. ej. confirmación por cámara para distinguir conejos de perros, protección IP del encapsulado]`

---

## Validación contra el problema original (Avance 1)

En el Avance 1 se identificó que los agricultores del Valle del Choapa enfrentan entre 200 y 300 conejos por predio y no tienen una forma no letal de proteger sus cultivos ni información sobre **cuándo** ocurren los ataques.

| Necesidad del Avance 1 | Cómo la responde AgroSafe | Evidencia |
|---|---|---|
| Detectar la presencia de conejos | PIR + ultrasónico | Pruebas 1 y 2 |
| Ahuyentar sin dañar | Rocío de agua de 5 s | Prueba 2 |
| Saber cuándo atacan | Gráfico por hora y hora peak en el dashboard | `[COMPLETAR: captura del gráfico tras N noches]` |
| No desperdiciar agua | Rocío solo < 150 cm; contador de segundos de rocío | `[COMPLETAR: segundos de rocío por noche]` |

**Conclusión:** `[COMPLETAR, p. ej. "Durante X noches el sistema registró N activaciones, con peak entre las HH y HH. Esto permite al agricultor..."]`
