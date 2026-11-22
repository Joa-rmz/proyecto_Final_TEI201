# Testing y Validación

## Objetivo
Validar que AgroSafe detecta correctamente, actúa solo cuando corresponde, registra los datos de forma persistente y entrega información útil para el problema del Avance 1.

## Carpetas
- `reportes/` — [`protocolo_pruebas.md`](reportes/protocolo_pruebas.md): objetivo, condiciones, procedimiento, criterio de éxito y tablas de resultados de cada prueba
- `datos/` — copias de `eventos.csv` de cada sesión de prueba
- `evidencias/` — capturas del dashboard, fotos y videos
- `simulacion/` — prueba del programa real con sensores simulados e imágenes sintéticas

## Resumen de pruebas

| # | Prueba | Métrica | Criterio de éxito | Resultado | Fuente |
|---|---|---|---|---|---|
| 1 | Precisión ultrasónico | Error (cm) | ≤ 3 cm entre 15 y 50 cm | ±3 mm | Ficha técnica del HC-SR04 |
| 2 | Activación / descarte | Tasa de acierto | ≥ 90 % | 100 % (30/30) | Simulación |
| 3 | Latencia | Segundos | Bomba < 5 s, dashboard < 2 s | 1,71 s / ≤ 1 s (sin tiempo de cámara) | Simulación |
| 4 | Captura continua y persistencia | % registros | ≥ 95 %, 0 pérdida | 100 %, 0 pérdida tras reinicio | Simulación |
| 5 | Autonomía | Horas | ≥ 12 h (una noche) | 12–18 h | Estimación con fichas técnicas |

La simulación prueba la lógica del programa con el código real. Detalle en [`reportes/protocolo_pruebas.md`](reportes/protocolo_pruebas.md).
