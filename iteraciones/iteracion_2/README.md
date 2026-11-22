# Iteración 2 - Prototipo Alpha IoT

**Versión:** v2.0 · **Avance asociado:** Avance 2 · Presentación: [Avance 2](https://github.com/joaquinrami703-cell/TEI_201_Grupo6/tree/main/documentacion/presentacion)

## Cambios respecto a v1
| Cambio | Razón |
|---|---|
| Se eliminó el ESP32; todo en Raspberry Pi | Un solo programa en Python coordina sensores, actuador y dashboard |
| Se agregó HC-SR04 | Confirmar distancia y reducir falsas activaciones |
| Divisor de voltaje en ECHO | Proteger el GPIO de 3,3 V |
| Rocío de 5 s solo si < 1,5 m | Menor consumo de agua |
| Dashboard Flask por WiFi | Ver eventos desde el celular |
| Diseño 3D: base fija + torreta | Primer encapsulado |

## Feedback recibido
- Integrar un ensamble 3D completo con joints y componentes internos.
- `[COMPLETAR otros comentarios del docente]`

## Próximos pasos planteados
1. Ensamblar el prototipo en la carcasa impresa.
2. Integrar cámara para confirmar detecciones.
3. Datos base: 7 noches registrando actividad.
4. Piloto: 7 noches en puntos críticos y comparar.
