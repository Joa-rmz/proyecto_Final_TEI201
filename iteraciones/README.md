# Historial de Iteraciones

| Aspecto | v1 (Avance 1) | v2 (Avance 2) | v3 (Avance 3) |
|---|---|---|---|
| Microcontrolador | ESP32 + Raspberry | Raspberry Pi 4 Model B | Raspberry Pi 4 Model B |
| Sensores | Solo PIR | PIR + ultrasónico | PIR + ultrasónico (+ cámara opcional) |
| Protección ECHO | Directo a 5 V | Divisor de voltaje | Divisor de voltaje |
| Lógica | Activa con cualquier movimiento | Rocía solo a < 1,5 m | Igual + registro de todos los eventos |
| Datos | — | Últimos 30 eventos en memoria | CSV persistente + estadísticas |
| Dashboard | — | Tabla de eventos (Flask) | Indicadores, gráfico por hora, alerta, descarga CSV |
| Encapsulado | — | Piezas 3D separadas | Ensamble completo `[COMPLETAR]` |
