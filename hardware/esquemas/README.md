# Esquemas de Circuito

> Subir aquí el esquemático completo (`.fzz` de Fritzing o equivalente) y su exportación `esquematico.pdf` / `.png`.

## Archivos esperados
- `agrosafe_circuito.fzz` — fuente Fritzing
- `esquematico.pdf` — exportación del esquema

## Conexiones (referencia para dibujar el esquema)

| Desde | Hacia |
|---|---|
| RPi pin 2 (5 V) | Riel + protoboard → VCC PIR, VCC HC-SR04 |
| RPi pin 6 (GND) | Riel − protoboard → GND PIR, GND HC-SR04, GND relé, divisor |
| RPi pin 11 (GPIO 17) | OUT PIR |
| RPi pin 13 (GPIO 27) | IN del módulo relé (bomba + pila 9 V en contacto NA) |
| RPi pin 16 (GPIO 23) | TRIG HC-SR04 |
| ECHO HC-SR04 | R1 → nodo → pin 18 (GPIO 24); nodo → R2 → GND |

## Notas de diseño
- Divisor de voltaje: Vout = 5 V × R2 / (R1 + R2) ≈ 3,3 V. `[COMPLETAR valores de R1 y R2]`
