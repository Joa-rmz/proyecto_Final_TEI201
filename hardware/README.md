# Hardware - AgroSafe

Prototipo IoT que detecta animales cerca de cultivos y activa una respuesta disuasoria no letal (rocío de agua). Una Raspberry Pi 4 Model B procesa las señales de dos sensores, controla el actuador y pide una foto a una ESP32-CAM por WiFi.

## Carpetas
- `esquemas/` — Esquemático del circuito
- `bom/` — Lista de materiales con costos
- `fotos/` — Fotografías del prototipo (mínimo 3 ángulos)

---

## Justificación de componentes

| Componente | Por qué se eligió |
|---|---|
| **Raspberry Pi 4 Model B** | WiFi integrado para el dashboard, corre Python + Flask y guarda el CSV en la microSD. Permite integrar cámara (CSI). Procesador de 4 núcleos a 1,5 GHz: corre sensores, servidor web y cámara en paralelo sin perder lecturas. Reemplazó a ESP32 + Raspberry, simplificando todo a un solo programa. |
| **ESP32-CAM (AI-Thinker, OV2640)** | Cámara de 2 MP con WiFi integrado y bajo costo. Toma una foto en cada activación para confirmar si el animal es un conejo (el PIR y el ultrasónico no distinguen especies). Al comunicarse por WiFi no ocupa pines GPIO de la Raspberry y puede ubicarse en la torreta. |
| **PIR HC-SR501** | Detecta calor en movimiento (un conejo es un cuerpo caliente) con alcance de 3–7 m y 110°; bajo consumo (< 65 µA) y salida de 3,3 V compatible directa con los GPIO. |
| **Ultrasónico HC-SR04** | Rango 2–400 cm con ±3 mm de precisión. Confirma que el objetivo está a < 150 cm (alcance de la boquilla), lo que elimina las falsas activaciones del PIR solo. |
| **LED + 220 Ω** | Representa al rociador durante la demo. (3,3 V − 2 V) / 220 Ω ≈ 6 mA, dentro del límite seguro de un GPIO. |
| **Divisor de voltaje** | El ECHO entrega 5 V y los GPIO aceptan máximo 3,3 V; el divisor protege la Raspberry. |
| **Batería 20.000 mAh** | Autonomía en terreno sin red eléctrica. La Raspberry Pi 4 Model B necesita 5 V / 3 A por USB-C, por lo que la batería debe entregar al menos 3 A. `[COMPLETAR: autonomía medida en horas]` |
| **Mini bomba + relé** | La bomba no puede alimentarse desde un GPIO; el relé la aísla y la activa con la señal del pin 12. |

---

## Conexiones eléctricas

| Elemento | GPIO | Pin físico |
|---|---|---|
| Alimentación 5 V / GND | — | 2 / 6 |
| Salida del PIR | GPIO 17 | 11 |
| LED / relé | GPIO 18 | 12 (con 220 Ω) |
| TRIG HC-SR04 | GPIO 23 | 16 |
| ECHO HC-SR04 | GPIO 24 | 18 (mediante divisor de voltaje) |
| ESP32-CAM | — | Sin cable a la Raspberry: WiFi (HTTP `/capture`). Alimentación 5 V / GND aparte |

## Pasos de ensamblaje
1. Pines 2 (5 V) y 6 (GND) a las líneas + y − de la protoboard.
2. PIR: VCC y GND a la protoboard, OUT al pin 11.
3. LED con resistencia de 220 Ω al pin 12.
4. HC-SR04: VCC/GND a la protoboard, TRIG al pin 16, ECHO al pin 18 a través del divisor.
5. ESP32-CAM: cargar el firmware (ver `software/esp32cam/`) y alimentarla con 5 V / GND.
6. Montar la electrónica en la base del encapsulado y los sensores y la ESP32-CAM en la torreta.

## Diseño para la reparación
- **Tapa removible** de la base para acceder a la Raspberry Pi y la protoboard sin romper nada.
- Conexiones con **cables jumper desmontables** (sin soldadura estructural ni pegamento).
- Sensores en la torreta, reemplazables de forma independiente.
- `[COMPLETAR: tipo de fijación — tornillos M3 / clips — y tiempo para abrir el equipo]`

## Precauciones
- No conectar ECHO directo a un GPIO (5 V dañan la Raspberry).
- No alimentar la bomba desde un GPIO; usar relé y fuente adecuada.
- Mantener la electrónica aislada del agua del rociador (en especial el lente de la ESP32-CAM).
- La ESP32-CAM necesita ≥ 500 mA a 5 V: con una fuente débil se reinicia al transmitir.

## Especificaciones técnicas
**Alimentación:** 5 V / 3 A por USB-C (batería 20.000 mAh)
**Consumo:** `[COMPLETAR: medir con tester USB, mA]`
**Dimensiones:** Base 132 × 132 × 203 mm · Torreta 59 × 81 × 88 mm
**Peso:** `[COMPLETAR] g`

## Troubleshooting

| Problema | Posible causa | Solución |
|---|---|---|
| Distancia siempre −1 | ECHO sin conexión o divisor mal armado | Revisar pin 18 y resistencias |
| Muchas activaciones falsas | PIR muy sensible | Bajar sensibilidad con el potenciómetro del HC-SR501 |
| Raspberry se reinicia o muestra ícono de rayo | Batería entrega menos de 3 A | Usar salida de 3 A o cable USB-C de buena calidad |
| No aparece foto en el dashboard | IP de la ESP32-CAM cambió o está en otra red | Revisar IP en el Monitor Serie y actualizar `ESP32_CAM_URL` |
| Dashboard no abre | Celular en otra red / IP cambió | Misma WiFi; verificar IP con `hostname -I` |
| LED no enciende | LED invertido o resistencia suelta | Revisar polaridad (pata larga al pin 12) |
