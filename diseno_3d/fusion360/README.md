# Archivos Fusion 360 — AgroSafe

## Archivos disponibles

| Archivo | Contenido |
|---|---|
| `Montaje completo .step` | Ensamble completo del prototipo (encapsulado + componentes) |
| `Pieza 1.stl` … `Pieza 6.stl` | Piezas individuales para impresión 3D |
| `AgroSafe_ensamble_v3.f3z` | ⚠️ **Por subir** — archivo nativo de Fusion 360 (la pauta lo exige: sin `.f3d`/`.f3z` no se puede verificar el modelo) |

> Para exportar: Fusion 360 → File → Export → *Fusion 360 Archive (.f3z)*, incluyendo componentes referenciados.

## Árbol de componentes del ensamble

```text
Agrosafe_Ensamble_Completo
├── Base_Fija (132 × 132 × 203 mm)
├── Tapa_Removible_Mantenimiento
├── Torreta_Giratoria (59 × 81 × 88 mm)
├── Raspberry_Pi_4B (85 × 56 × 17 mm)
├── Protoboard
├── Bateria_20000mAh
├── Sensor_PIR_HC-SR501
├── Sensor_Ultrasonico_HC-SR04
├── Bomba_y_Rele
├── Servomotor
└── Tornilleria_M3
```

`[COMPLETAR: qué pieza corresponde a cada archivo Pieza 1–6]`

## Parámetros principales
- Grosor de pared: `[COMPLETAR] mm`
- Holgura de encaje de la tapa: `[COMPLETAR] mm`
- Material: PLA (prototipo) / PETG (exterior)
