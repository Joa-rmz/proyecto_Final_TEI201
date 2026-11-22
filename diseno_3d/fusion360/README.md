# Archivos Fusion 360 — AgroSafe

| Archivo | Contenido |
|---|---|
| `modelo. completof3d.f3d` | Archivo nativo de Fusion 360 con el ensamble completo |
| `Montaje con componentes` | Ensamble STEP con carcasa y todos los componentes internos |
| `Montaje completo .step` | Ensamble STEP del encapsulado |
| `Pieza 1.stl` … `Pieza 6.stl` | Piezas individuales para impresión 3D |

## Piezas STL

| Archivo | Pieza | Dimensiones (mm) |
|---|---|---|
| `Pieza 1.stl` | Base | 145,1 × 145,1 × 142,9 |
| `Pieza 2.stl` | Bandeja | 132,8 × 132,8 × 45,6 |
| `Pieza 3.stl` | Placa soporte protoboard | 60 × 87 × 6 |
| `Pieza 4.stl` | Tapa | 139,9 × 139,9 × 6,8 |
| `Pieza 5.stl` | Torreta | 59,3 × 102,7 × 109 |
| `Pieza 6.stl` | Tapa de torreta | 51 × 43,5 × 5 |

## Árbol de componentes del ensamble

```text
AgroSafe_Ensamble_Completo
├── Base
├── Tapa
├── Bandeja
├── Placa_protoboard
├── Torreta_cuerpo
├── Torreta_tapa
├── Raspberry_Pi_4B
├── Rele_1canal
├── Protoboard_400
├── Powerbank
├── Pila_9V
├── ESP32_CAM
├── PIR_HC_SR501
├── HC_SR04
└── Manguera
```

## Parámetros principales
- Grosor de pared: 2,8 mm (base) y 2,5 mm (torreta)
- Holgura tapa–base: 2,1 mm por lado (pestaña 130 × 130 en interior de 134,3)
- Holgura tapa de torreta: 0,3 mm por lado (pestaña 45,4 × 37,9 en abertura 46 × 38,5)
- Material: PETG (prototipo en PLA)
