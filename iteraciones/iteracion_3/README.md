# Iteración 3 - Prototipo IoT Completo

**Versión:** v3.0 · **Fecha:** noviembre 2026 · **Avance asociado:** Avance 3

## Cambios respecto a v2

### Software
| Cambio | Razón |
|---|---|
| Rango de activación de 15 a 50 cm, confirmado con 3 lecturas seguidas del HC-SR04 | En v2 se rociaba a < 1,5 m; se acotó para actuar solo cuando el animal está frente al dispositivo |
| Reconocimiento de la figura objetivo con OpenCV en 2 capturas de la ESP32-CAM | Confirmar que es el animal objetivo antes de activar y reducir falsas activaciones |
| Verificación final de distancia antes de rociar | Evitar activar si el animal ya se alejó durante el análisis |
| Pulso de bomba de 2 s (antes 5 s) y pausa de 5 s con rearme del PIR | Disuadir con menos agua y evitar activaciones en cadena |
| Guardado de cada evento en `software/data/eventos.csv` | La pauta exige repositorio persistente; antes los datos se perdían al reiniciar |
| Indicadores: movimientos detectados, activaciones, descartes, % de confirmación, hora de mayor actividad y tiempo total de bomba | Convertir datos crudos en información para el agricultor |
| Gráfico de activaciones por hora | Identificar el horario de mayor actividad de los conejos |
| Alerta con ≥ 5 activaciones en la última hora | Avisar de alta presión para que el agricultor revise el predio |
| Descarga del historial en CSV (`/datos.csv`) y estado en JSON (`/api/estado`) | Analizar varias noches en Excel o R |

### Hardware
| Cambio | Razón |
|---|---|
| Se integró una **ESP32-CAM** que entrega fotos por WiFi a la Raspberry (`/capture`) | Confirmar visualmente la detección antes de activar la bomba |
| Relé de 1 canal en GPIO27 (pin 13) controlando la bomba de agua | Actuador que rocía agua para ahuyentar al animal |
| Todos los componentes montados dentro de la carcasa: Raspberry Pi 4 Model B, protoboard, relé, batería de 20.000 mAh y pila de 9 V en la base; PIR, HC-SR04, ESP32-CAM y boquilla en la torreta | Prototipo funcional como un solo equipo, listo para instalar en terreno |
| Manguera desde la base hasta la boquilla por el tubo pasamanguera | Llevar el agua sin exponer el circuito |

### Diseño 3D
| Cambio | Razón |
|---|---|
| Ensamble completo en Fusion 360 (`diseno_3d/fusion360/modelo. completof3d.f3d`) con las 6 piezas y todos los componentes internos | Responde al feedback del Avance 2: gemelo 3D con componentes internos |
| Bandeja con separadores para la Raspberry Pi 4 (58 × 49 mm) y placa soporte del protoboard | Fijar la electrónica y ordenar el cableado |
| Tapa con 4 tornillos M3 y tapa de torreta a presión | Abrir el equipo para reparación sin romper piezas |
| Ventana de servicio, rejilla de ventilación y tubo pasamanguera en la base | Acceso, disipación de calor y paso de la manguera |
| Planos técnicos (4 láminas A3) y renders exterior, desarmado e interior | Documentar el diseño para fabricación |

## Feedback del Avance 2 atendido
| Feedback / próximo paso planteado en v2 | Estado en v3 |
|---|---|
| Integrar un ensamble 3D completo con componentes internos | Hecho (ver `diseno_3d/`) |
| Ensamblar el prototipo en la carcasa impresa | Hecho |
| Integrar cámara para confirmar detecciones | Hecho (ESP32-CAM + reconocimiento en 2 capturas) |
| Datos base: 7 noches registrando actividad | Habilitado con el CSV persistente; queda como próximo paso |

## Limitaciones
- Para la demostración, el reconocimiento identifica una figura de estrella que representa al conejo; reconocer al animal real requiere entrenar un modelo con imágenes del predio.
- La dirección IP de la ESP32-CAM está fija en el código (`URL_CAMARA`); si cambia la red, hay que actualizarla.

## Próximos pasos
1. Registrar 7 noches de datos base en el predio con el CSV.
2. Piloto de 7 noches en los puntos críticos y comparar el daño con y sin el dispositivo.
3. Reemplazar el reconocimiento de figura por un modelo entrenado con imágenes de conejos.

## Resultados
Ver `testing/reportes/protocolo_pruebas.md`.
