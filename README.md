# 🐇 AgroSafe — Protección inteligente de cultivos

Sistema IoT no letal que **detecta conejos cerca de los cultivos, los ahuyenta con un rocío de agua y registra cada evento** en un dashboard web, para que los agricultores del Valle del Choapa sepan cuándo y cuánto son atacados sus cultivos.

**TEI201 — Taller de Diseño en Ingeniería · Universidad Adolfo Ibáñez · Grupo 6**

> 📘 **Este repositorio es el informe del proyecto.** No hay un informe escrito aparte: cada sección del Avance 3 está documentada en su carpeta.

| Sección del informe | Dónde está |
|---|---|
| Problema y solución | Este README (abajo) |
| Software: captura, almacenamiento, dashboard e información | [`software/`](software/) · código en [`software/src/agrosafe.py`](software/src/agrosafe.py) |
| ESP32-CAM | [`software/esp32cam/`](software/esp32cam/) |
| Hardware: componentes, conexiones, reparación | [`hardware/`](hardware/) |
| BOM y costos | [`hardware/bom/`](hardware/bom/) |
| Diseño 3D: gemelo, planos, renders | [`diseno_3d/`](diseno_3d/) |
| Testing y validación contra el problema | [`testing/`](testing/) · [`protocolo_pruebas.md`](testing/reportes/protocolo_pruebas.md) |
| Evolución del prototipo (v1 → v3) | [`iteraciones/`](iteraciones/) |
| Declaración de fuentes e IA | [`FUENTES.md`](FUENTES.md) |
| Presentación | [`documentacion/`](documentacion/) |

---

## 👥 Integrantes

| Nombre | Rol |
|---|---|
| Vanessa Arévalo | Representante |
| Isidora González | Miembro |
| Francisca Mardones | Miembro |
| Joaquín Ramírez | Miembro |
| Nicolás Torres | Miembro |

---

## 🌱 Problema (Avance 1)

- **ODS 15:** Vida de ecosistemas terrestres — control de una especie exótica invasora.
- El **conejo europeo** es una especie invasora en Chile. En el Valle del Choapa (comuna de Salamanca) se registran **entre 200 y 300 conejos por predio agrícola**, y recuperar un cultivo dañado toma **4 a 5 años**.
- Los métodos actuales suelen ser letales. AgroSafe propone una **alternativa no letal**: detección temprana + rocío de agua.

## 💡 Solución

```
PIR detecta movimiento → Ultrasónico confirma < 1,5 m → Rocío 5 s + foto ESP32-CAM → Evento guardado en CSV → Dashboard + alertas
```

| Capa | Implementación |
|---|---|
| Captura | Sensor PIR HC-SR501 + sensor ultrasónico HC-SR04 + ESP32-CAM (foto del animal por WiFi) |
| Procesamiento | Raspberry Pi 4 Model B (Python) |
| Actuador | LED indicador (representa relé + mini bomba de agua) |
| Almacenamiento | CSV estructurado persistente (`software/data/eventos.csv`) |
| Dashboard | Flask por WiFi, visible desde el celular |
| Información | Activaciones del día, hora peak, % de confirmación, tiempo de rocío, gráfico por hora, alerta de alta actividad |

**¿Qué decisiones permite tomar?** El agricultor identifica el horario de mayor actividad de conejos, detecta noches de alta presión (alerta) y estima el consumo de agua del sistema.

---

## 📁 Estructura del Repositorio

```
├── README.md          # Este archivo
├── FUENTES.md         # Declaración de librerías, código externo e IA (obligatorio)
├── software/          # (= firmware/) Código Python, dashboard, datos
│   ├── src/agrosafe.py
│   ├── esp32cam/      # Instrucciones del firmware de la ESP32-CAM
│   ├── data/          # eventos.csv se genera al ejecutar
│   └── requirements.txt
├── hardware/          # Esquemático, BOM, fotos del prototipo
├── diseno_3d/         # Fusion 360 / STEP / STL, planos, renders
├── testing/           # Protocolo de pruebas, datos y evidencias
├── documentacion/     # (= docs/) Presentaciones
└── iteraciones/       # Historial v1 → v2 → v3
```

---

## 🧰 Componentes para replicar el hardware

| Componente | Cant. | Función |
|---|---|---|
| Raspberry Pi 4 Model B | 1 | Procesamiento, WiFi y dashboard |
| Sensor PIR HC-SR501 | 1 | Detección de movimiento |
| Sensor ultrasónico HC-SR04 | 1 | Confirmación de distancia (< 150 cm) |
| ESP32-CAM (AI-Thinker, OV2640) + programador FTDI | 1 | Foto del animal al activarse; confirma si es un conejo |
| LED + resistencia 220 Ω | 1 | Indicador del rociador |
| Resistencias para divisor de voltaje | 2 | ECHO 5 V → 3,3 V |
| Protoboard + cables jumper | 1 | Conexiones |
| Batería externa 20.000 mAh | 1 | Alimentación portátil |
| Mini bomba de agua + relé | 1 | Actuador final (en integración) |

Detalle con costos en [`hardware/bom/`](hardware/bom/).

---

## 🚀 Instalación y uso

### 1. Conectar el hardware
| Elemento | GPIO | Pin físico |
|---|---|---|
| PIR (OUT) | GPIO 17 | 11 |
| LED / relé | GPIO 18 | 12 |
| HC-SR04 TRIG | GPIO 23 | 16 |
| HC-SR04 ECHO (**con divisor de voltaje**) | GPIO 24 | 18 |
| 5 V / GND | — | 2 / 6 |

### 2. Preparar la ESP32-CAM
1. En Arduino IDE, instalar el núcleo ESP32 y abrir Archivo → Ejemplos → ESP32 → Camera → `CameraWebServer`.
2. Activar `CAMERA_MODEL_AI_THINKER` y escribir el WiFi en `ssid` / `password`.
3. Cargar con el programador FTDI (GPIO 0 a GND al cargar; quitarlo y presionar RESET al terminar).
4. Abrir el Monitor Serie a 115200 baudios y anotar la IP que aparece.
5. Probar `http://<IP-ESP32-CAM>/capture` en el navegador: debe mostrar una foto.

Detalle en [`software/esp32cam/`](software/esp32cam/).

### 3. Instalar dependencias en la Raspberry Pi
```bash
sudo apt update
sudo apt install python3-flask python3-rpi.gpio
```

### 4. Clonar y ejecutar
```bash
git clone https://github.com/Joa-rmz/proyecto_Final_TEI201.git
cd proyecto_Final_TEI201/software/src
ESP32_CAM_URL=http://<IP-ESP32-CAM>/capture python3 agrosafe.py
```

### 5. Abrir el dashboard
Desde un dispositivo en la misma red WiFi: **`http://<IP-de-la-Raspberry>:5000`** (IP con `hostname -I`).
- `/datos.csv` → descarga del histórico
- `/api/estadisticas` → indicadores en JSON
- La última foto de la ESP32-CAM aparece en el dashboard tras cada activación

---

## 📊 Estado del Proyecto
- **Versión:** v3.0 — Avance 3, Prototipo IoT completo
- **Última actualización:** 22 de noviembre de 2026
- **Presentación:** 23 de noviembre de 2026

---

## ✅ Checklist de Entrega (Avance 3)

### Software
- [x] Código Python comentado (`software/src/agrosafe.py`)
- [x] Almacenamiento persistente (CSV estructurado)
- [x] Dashboard con indicadores, gráfico y alerta
- [x] Librerías documentadas (`software/librerias/`, `FUENTES.md`)
- [ ] Captura de pantalla del dashboard y del CSV con datos reales (`testing/evidencias/`)

### Hardware
- [ ] Esquemático (Fritzing / KiCad / EasyEDA) en `hardware/esquemas/`
- [ ] BOM con costos completos (`hardware/bom/BOM.csv`)
- [ ] Fotografías del prototipo ensamblado (mínimo 3 ángulos)
- [x] Justificación de componentes (`hardware/README.md`)

### Diseño 3D
- [ ] Archivo `.f3d` / `.f3z` con ensamble completo (carcasa + componentes)
- [x] Archivo STEP y piezas STL
- [ ] Renders (exterior + explosionado)
- [ ] Planos técnicos en PDF con cotas y tolerancias

### Testing
- [x] Protocolo de pruebas (`testing/reportes/protocolo_pruebas.md`)
- [ ] Resultados cuantitativos completados
- [ ] Análisis de falla y solución
- [ ] Validación contra el problema del Avance 1

### GitHub / Documentación
- [x] README completo y FUENTES.md en la raíz
- [ ] Presentación Avance 3 en `documentacion/presentacion/`
- [ ] URL del repositorio en los slides

---

## 📄 Licencia
Proyecto desarrollado para el curso TEI201 — Facultad de Ingeniería y Ciencias — Universidad Adolfo Ibáñez.
