# Iteración 3 - Prototipo IoT Completo

**Versión:** v3.0 · **Fecha:** noviembre 2026 · **Avance asociado:** Avance 3

## Cambios respecto a v2

### Software
| Cambio | Razón |
|---|---|
| Guardado de cada evento en `data/eventos.csv` | La pauta exige repositorio persistente; antes los datos se perdían al reiniciar |
| Indicadores: activaciones, descartes, % confirmación, hora peak, distancia promedio, segundos de rocío | Convertir datos crudos en información para el agricultor |
| Gráfico de activaciones por hora | Identificar el horario de ataque de los conejos |
| Alerta ≥ 5 activaciones/hora | Avisar de alta presión para que el agricultor actúe |
| Descarga CSV y API JSON | Análisis posterior de varias noches |

### Hardware
- `[COMPLETAR: integración en carcasa, relé + bomba, cámara, etc.]`

### Diseño 3D
- `[COMPLETAR: ensamble .f3d con componentes internos y joints]`

## Resultados
Ver `testing/reportes/protocolo_pruebas.md`.
