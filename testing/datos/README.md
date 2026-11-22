# Datos de Testing

Copiar aquí el `eventos.csv` de cada sesión (descargable desde `http://<IP>:5000/datos.csv`), nombrado `AAAAMMDD_prueba_N.csv`.

## Formato

| Columna | Descripción | Ejemplo |
|---|---|---|
| `fecha` | AAAA-MM-DD | 2026-11-22 |
| `hora` | HH:MM:SS | 21:14:03 |
| `estado` | `activado` / `descartado` / `reposo` | activado |
| `distancia_cm` | Distancia medida (−1 = sin eco) | 84.2 |
| `foto` | Si se tomó foto | True |
