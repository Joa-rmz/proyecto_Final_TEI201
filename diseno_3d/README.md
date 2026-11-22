# Diseño 3D - AgroSafe

Encapsulado de **dos piezas** con gemelo 3D de todos los componentes internos.

| Pieza | Dimensiones | Función |
|---|---|---|
| Base fija | 132 × 132 × 203 mm | Aloja Raspberry Pi 3 B+ (85 × 56 mm), protoboard, batería y cableado. Tapa removible para mantenimiento. |
| Torreta giratoria | 59 × 81 × 88 mm | Sensores PIR y HC-SR04 arriba (campo de visión despejado), brazo y boquilla. Gira con servomotor. |

**Software:** Autodesk Fusion 360 · **Unidades:** mm · **Escala:** 1:1
**Material:** PLA (prototipo) · PETG (uso exterior: resiste sol y humedad)
**Detalles:** aberturas de ventilación y pasacables.

## 📁 Carpetas
- `fusion360/` — `Montaje completo .step` (ensamble) + `Pieza 1.stl` a `Pieza 6.stl` · **falta `.f3d`/`.f3z`**
- `planos/` — planos técnicos en PDF
- `renders/` — renders exterior y explosionado

## Gemelo 3D — componentes que deben estar en el ensamble

| Componente | Volumen de referencia (mm) | ¿Modelado? |
|---|---|---|
| Raspberry Pi 3 B+ | 85 × 56 × 17 | [ ] |
| Protoboard | `[COMPLETAR]` | [ ] |
| Batería 20.000 mAh | `[COMPLETAR]` | [ ] |
| Sensor PIR HC-SR501 | 32 × 24 × 25 (con domo) | [ ] |
| Sensor HC-SR04 | 45 × 20 × 15 | [ ] |
| Mini bomba + relé | `[COMPLETAR]` | [ ] |
| Servomotor | `[COMPLETAR]` | [ ] |
| Tornillería | M3 | [ ] |

## Checklist
- [ ] `fusion360/AgroSafe_ensamble_v3.f3z` con carcasa + componentes internos
- [x] `fusion360/Montaje completo .step` y piezas STL (6)
- [ ] `planos/plano_conjunto_v3.pdf` (vistas ortogonales, cotas, tolerancias, escala)
- [ ] `renders/01_exterior.png` y `renders/02_explosionado.png`
