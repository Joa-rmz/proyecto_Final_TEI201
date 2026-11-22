# Protocolo de Pruebas — AgroSafe (Avance 3)

> Las tablas de cada prueba son para las mediciones con el equipo real. Antes se probó el programa en simulación (abajo): sensores simulados e imágenes sintéticas, sin la Raspberry ni la cámara.

## Resultados en simulación (22-11-2026)

Se ejecutó el programa real `agrosafe.py` con sensores simulados y la función real de reconocimiento `detectar_estrella()` sobre imágenes generadas (estrella = figura objetivo; círculo o cuadrado = otro objeto). Script y detalle en `testing/simulacion/`; datos en `testing/datos/20261122_simulacion.csv`; captura en `testing/evidencias/dashboard_simulacion.png`.

**Prueba 2 en simulación: lógica de activación / descarte**

| Escenario | Intentos | Activado | Descartado | Tasa de acierto |
|---|---|---|---|---|
| Figura a ~30 cm | 10 | 10 | 0 | 100 % |
| Figura a ~80 cm | 10 | 0 | 10 | 100 % |
| Otro objeto a ~30 cm | 10 | 0 | 10 | 100 % |

Con la figura a 80 cm el programa descarta antes de tomar fotos (falla la verificación de distancia); con otro objeto descarta en la primera captura.

**Prueba 3 en simulación: latencia del programa**
- Movimiento → encendido del relé: 1,71 s en promedio (mín. 1,71 s, máx. 1,73 s; 10 activaciones). Corresponde a 3 lecturas de distancia, 2 capturas con 0,5 s entre ellas y la verificación final. No incluye el tiempo real de descarga de la foto desde la ESP32-CAM.
- Dashboard: se actualiza cada 1 s, por lo que un evento aparece en ≤ 1 s.

**Prueba 4 en simulación: persistencia**
- Se generaron 100 eventos y el CSV quedó con 100 filas (100 % registrados).
- Al reiniciar el programa se recargaron los 60 eventos de detección, activación y descarte, y los indicadores del día quedaron iguales: 30 movimientos, 10 activaciones, 20 descartes, 33,3 % confirmadas.
- Con 10 activaciones en la última hora apareció la alerta de alta actividad (umbral: 5).

**Alcance:** la simulación no mide la precisión física del HC-SR04 (Prueba 1), el tiempo de la cámara por WiFi ni la autonomía (Prueba 5), y las imágenes sintéticas son más limpias que una foto real. Las tablas siguientes sirven para registrar esas mediciones con el equipo armado.

---

## Prueba 1 — Precisión del sensor ultrasónico

| Campo | Detalle |
|---|---|
| **Objetivo** | Verificar que el HC-SR04 mide correctamente la distancia que decide si se rocía. |
| **Condiciones** | Interior, objeto plano (cartón), sensor fijo en la torreta. |
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
| **Procedimiento** | 1. Dejar el sistema funcionando 2 horas. 2. Generar N movimientos y contar que cada uno tenga su fila en `eventos.csv`. 3. Desconectar la energía, reiniciar y verificar que los indicadores del día siguen en el dashboard. |
| **Criterio de éxito** | 100 % de los eventos registrados; 0 datos perdidos tras reinicio. |

| Duración (h) | Eventos generados | Filas en CSV | % registrados | ¿Datos tras reinicio? |
|---|---|---|---|---|
| | | | | |

---

## Prueba 5 — Autonomía de la batería

| Duración total (h) | Consumo medido (mA) | Observaciones |
|---|---|---|
| | | No se contó con tester USB; autonomía estimada con fichas técnicas: 12 a 18 h |

---

## Análisis de fallas

| Falla encontrada | Causa | Solución aplicada | Resultado |
|---|---|---|---|
| Falsas activaciones con solo PIR (Avance 2) | El PIR detecta cualquier calor en movimiento a 3–7 m | Se agregó el HC-SR04 (15–50 cm) y la confirmación con 2 capturas de cámara | Ver Prueba 2 |
| ECHO conectado directo a 5 V (Avance 2) | Riesgo de dañar el GPIO de 3,3 V | Divisor de voltaje | Sin daños en la Raspberry |
| Datos se perdían al reiniciar | Eventos solo en memoria (últimos 50) | Escritura en `eventos.csv` en cada evento | Ver Prueba 4 |
| Una lectura aislada del HC-SR04 podía activar la bomba | Rebotes y lecturas erróneas del ultrasónico | Se exigen 3 lecturas seguidas entre 15 y 50 cm, y una verificación final antes de rociar | Incorporado en `agrosafe.py` |

**Propuestas de mejora:**
1. Reemplazar el reconocimiento de la figura por un modelo entrenado con fotos de conejos reales.
2. Sellar la carcasa para que resista lluvia y polvo en terreno.
3. Dejar una IP fija para la ESP32-CAM, así no hay que cambiar el código si cambia la red.
4. Enviar la alerta de alta actividad al celular del agricultor.
5. Agregar un panel solar para no depender de recargar la batería.

---

## Validación contra el problema original (Avance 1)

En el Avance 1 se identificó que los agricultores del Valle del Choapa enfrentan entre 200 y 300 conejos por predio y no tienen una forma no letal de proteger sus cultivos ni información sobre **cuándo** ocurren los ataques.

| Necesidad del Avance 1 | Cómo la responde AgroSafe | Evidencia |
|---|---|---|
| Detectar la presencia de conejos | PIR + ultrasónico | Pruebas 1 y 2 |
| Ahuyentar sin dañar | Rocío de agua de 2 s | Prueba 2 |
| Saber cuándo atacan | Gráfico por hora y hora peak en el dashboard | Gráfico de activaciones por hora del dashboard, calculado desde `eventos.csv` |
| No desperdiciar agua | Rocío solo con objetivo confirmado entre 15 y 50 cm; contador de segundos de bomba | Indicador "Tiempo total de bomba" del dashboard |

**Conclusión:** El prototipo v3 responde a las cuatro necesidades del Avance 1: detecta movimiento, confirma con distancia y cámara antes de actuar, ahuyenta con un rocío corto de agua y guarda cada evento para mostrar cuándo hay más actividad. El siguiente paso es usarlo varias noches en el predio para medir cuánto reduce el daño en los cultivos.
