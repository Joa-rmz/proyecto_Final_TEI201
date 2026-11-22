# Datos de Testing

Copias del `eventos.csv` de cada sesión (descargable desde `http://<IP>:5000/datos.csv`), con nombre `AAAAMMDD_prueba.csv`.

| Archivo | Sesión |
|---|---|
| `20261122_simulacion.csv` | Simulación del programa (30 intentos, ver `testing/simulacion/`) |

## Formato

| Columna | Descripción | Ejemplo |
|---|---|---|
| `fecha` | AAAA-MM-DD | 2026-11-22 |
| `hora` | HH:MM:SS | 20:05:48 |
| `tipo` | `deteccion` / `activacion` / `descarte` / `info` / `error` | activacion |
| `mensaje` | Texto del evento | Estrella confirmada. Pulso de 2 segundos. |
| `distancia_cm` | Última distancia medida | 29.4 |
