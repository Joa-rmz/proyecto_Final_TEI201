# Diseño 3D - AgroSafe

Encapsulado de dos cuerpos (base fija y torreta con sensores) con gemelo 3D de todos los componentes internos.

| Pieza | Dimensiones | Función |
|---|---|---|
| Base | 145 × 145 × 143 mm | Aloja la Raspberry Pi 4 Model B, batería, pila, relé y protoboard. Ventana de servicio, rejilla de ventilación y tubo pasamanguera. |
| Tapa | 140 × 140 × 6,9 mm | Cierra la base con 4 tornillos M3 (desmontable para reparación) y sostiene la torreta. |
| Bandeja | 132,8 × 132,8 × 45,6 mm | Soporta la Raspberry Pi 4 (separadores 58 × 49 mm) y los postes de la placa del protoboard. |
| Placa soporte protoboard | 60 × 87 × 6 mm | Aloja el protoboard de 400 puntos. |
| Torreta | 51 × 43,5 × 109 mm (disco Ø59,3) | Ubica el HC-SR04, el PIR, la ESP32-CAM y la boquilla. |
| Tapa de torreta | 51 × 43,5 × 5 mm | Cierra la torreta a presión. |

**Software:** Autodesk Fusion 360 · **Unidades:** mm · **Escala:** 1:1
**Material:** PETG (prototipo en PLA)

## Carpetas
- `fusion360/` — archivo de Fusion 360, ensambles STEP y piezas STL
- `planos/` — planos técnicos en PDF (4 láminas A3)
- `renders/` — vista exterior, desarmada e interior

## Gemelo 3D — componentes incluidos en el ensamble

| Componente | Volumen en el modelo (mm) |
|---|---|
| Raspberry Pi 4 Model B | 87 × 56,5 × 17 |
| Protoboard 400 puntos | 82 × 54 × 9,1 |
| Batería 20.000 mAh | 100,5 × 64,1 × 31,8 |
| Pila 9 V | 50 × 25 × 15 |
| Módulo relé 1 canal | 35 × 26 × 17 |
| Sensor PIR HC-SR501 | 34 × 23,2 × 23 |
| Sensor HC-SR04 | 45 × 23,3 × 20 |
| ESP32-CAM | 22 × 20,2 × 40 |
| Manguera | recorrido desde la base hasta la boquilla |

## Checklist
- [x] Archivo de Fusion 360 (`fusion360/modelo. completof3d.f3d`)
- [x] Ensamble STEP con todos los componentes y piezas STL
- [x] Planos técnicos en PDF (vistas, cortes, cotas, tolerancias, escala)
- [x] Renders exterior, desarmado e interior
