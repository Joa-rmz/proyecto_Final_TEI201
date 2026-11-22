# Simulación del programa

Prueba del software sin el equipo físico. Se ejecuta el programa real `agrosafe.py` con:
- `gpiozero.py`: reemplaza el PIR, el HC-SR04 (distancia fija ±1 cm) y el relé.
- Imágenes sintéticas en lugar de la ESP32-CAM: una estrella (figura objetivo) o un círculo o cuadrado (otro objeto), con posición, tamaño y giro al azar. El reconocimiento usa la función real `detectar_estrella()`.

```bash
cd testing/simulacion
python3 simulacion.py
```

Requiere `opencv-python`, `numpy` y `flask`. Resultados en `testing/reportes/protocolo_pruebas.md` (sección "Resultados en simulación").
