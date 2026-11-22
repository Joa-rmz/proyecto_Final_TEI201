# Software - AgroSafe

## 1. Descripción

Código y documentación del software de **AgroSafe**. Un único programa en Python (`src/agrosafe.py`) corre en la Raspberry Pi y cumple el ciclo completo IoT:

**Captura → Almacena → Visualiza → Genera información → Permite decidir**

| Etapa | Implementación |
|---|---|
| Captura | PIR HC-SR501 (leído cada 0,1 s) + HC-SR04 (confirmación de distancia) |
| Almacenamiento | `data/eventos.csv` — CSV estructurado (fecha, hora, estado, distancia, foto). Se escribe en cada evento y se recarga al reiniciar |
| Visualización | Dashboard Flask en `http://<IP-Raspberry>:5000`, se actualiza cada 2 s |
| Información | Activaciones del día, descartes, % de confirmación, hora peak, distancia promedio, tiempo de rocío, gráfico por hora y alerta de alta actividad |
| Decisión | El agricultor sabe **cuándo** hay más conejos (hora peak), **cuánta presión** hay (alerta) y **cuánta agua** se usa (segundos de rocío) |

## 2. Estructura de la carpeta

```
software/
├── src/agrosafe.py     # Programa principal
├── data/               # eventos.csv se crea aquí al ejecutar
├── requirements.txt    # Dependencias
├── librerias/          # Documentación de librerías
└── docs/               # Manual de instalación y operación, diagrama de flujo
```

## 3. Tecnologías

- **Plataforma:** Raspberry Pi 4 Model B (Raspberry Pi OS)
- **Lenguaje:** Python 3
- **GPIO:** RPi.GPIO
- **Dashboard:** Flask
- **Concurrencia:** `threading` (sensores y servidor web en paralelo)
- **Cámara (opcional):** picamera2

## 4. Funcionamiento

1. Inicialización de pines y del archivo CSV.
2. El PIR detecta movimiento.
3. El HC-SR04 mide la distancia.
4. Si la distancia es < 150 cm → se activa el rociador (LED/relé) 5 s, se toma foto y se registra `activado`.
5. Si es ≥ 150 cm o no hay eco → se registra `descartado`.
6. Enfriamiento de 8 s tras cada activación.
7. Cada 5 s se registra `reposo` con la distancia actual (prueba de captura continua).

## 5. Conexiones

| Componente | Pin GPIO | Pin físico |
|---|---:|---:|
| Sensor PIR HC-SR501 (OUT) | GPIO 17 | 11 |
| LED / relé rociador | GPIO 18 | 12 |
| TRIG del HC-SR04 | GPIO 23 | 16 |
| ECHO del HC-SR04 (con divisor de voltaje) | GPIO 24 | 18 |
| 5 V / GND | — | 2 / 6 |

## 6. Instalación y ejecución

```bash
sudo apt update
sudo apt install python3-flask python3-rpi.gpio
# opcional, cámara:
sudo apt install python3-picamera2

git clone https://github.com/Joa-rmz/proyecto_Final_TEI201.git
cd proyecto_Final_TEI201/software/src
python3 agrosafe.py
```

Abrir en el celular o computador (misma red WiFi): `http://<IP-de-la-Raspberry>:5000`
La IP se obtiene con `hostname -I`.

### Endpoints

| Ruta | Uso |
|---|---|
| `/` | Dashboard |
| `/api/estadisticas` | Indicadores en JSON |
| `/datos.csv` | Descarga del histórico completo |
| `/foto` | Última foto (si hay cámara) |
