# Testing y Validación

## Objetivo
Validar que AgroSafe detecta correctamente, actúa solo cuando corresponde, registra los datos de forma persistente y entrega información útil para el problema del Avance 1.

## Carpetas
- `reportes/` — [`protocolo_pruebas.md`](reportes/protocolo_pruebas.md): objetivo, condiciones, procedimiento, criterio de éxito y tablas de resultados de cada prueba
- `datos/` — copias de `eventos.csv` de cada sesión de prueba
- `evidencias/` — capturas del dashboard, fotos y videos

## Resumen de pruebas

| # | Prueba | Métrica | Criterio de éxito | Resultado |
|---|---|---|---|---|
| 1 | Precisión ultrasónico | Error (cm) | ≤ 3 cm entre 15 y 50 cm | `[ ]` |
| 2 | Activación / descarte | Tasa de acierto | ≥ 90 % | `[ ]` |
| 3 | Latencia | Segundos | Bomba < 5 s, dashboard < 2 s | `[ ]` |
| 4 | Captura continua y persistencia | % registros | ≥ 95 %, 0 pérdida | `[ ]` |
| 5 | Autonomía | Horas | `[definir]` | `[ ]` |
