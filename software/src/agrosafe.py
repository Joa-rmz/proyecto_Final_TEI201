"""
AgroSafe - Protección inteligente de cultivos (TEI201 - Grupo 6)

Programa principal que corre en la Raspberry Pi 4 Model B:
  1. CAPTURA   : PIR HC-SR501 detecta movimiento; HC-SR04 confirma distancia;
                 la ESP32-CAM toma una foto del animal por WiFi.
  2. ACTÚA     : si el objetivo está a < 150 cm, activa el rociador (LED/relé) 5 s.
  3. ALMACENA  : cada evento se guarda en data/eventos.csv (persiste al reiniciar).
  4. VISUALIZA : dashboard Flask en http://<IP-de-la-Raspberry>:5000
  5. INFORMA   : estadísticas del día, actividad por hora y alerta de alta actividad.

Ejecutar:  python3 agrosafe.py
"""

import csv
import os
import time
import threading
import urllib.request
from collections import Counter
from datetime import datetime, timedelta

import RPi.GPIO as GPIO
from flask import Flask, send_file, jsonify

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

# Pines físicos de la Raspberry Pi (numeración BOARD)
PIR_PIN = 11       # Salida del sensor PIR (GPIO 17)
LED_PIN = 12       # LED / relé de la bomba, con resistencia de 220 ohm (GPIO 18)
TRIG_PIN = 16      # Trigger del sensor ultrasónico (GPIO 23)
ECHO_PIN = 18      # Echo del ultrasónico mediante divisor de tensión (GPIO 24)

# Parámetros del sistema
DISTANCIA_MAXIMA_CM = 150   # Solo se rocía si el objetivo está más cerca que esto
TIEMPO_ACTIVACION_S = 5     # Duración del rocío (ahorra agua)
TIEMPO_REPOSO_S = 8         # Enfriamiento tras una activación
TIEMPO_REARME_S = 1         # El PIR debe estar 1 s en reposo antes de re-detectar
INTERVALO_BEACON_S = 5      # Cada 5 s se registra un "reposo" (prueba que el sistema está vivo)
MAX_EVENTOS = 30            # Eventos mostrados en la tabla del dashboard

# Generación de información
UMBRAL_ALERTA_HORA = 5      # >= 5 activaciones en la última hora -> alerta de alta actividad

# Almacenamiento persistente
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, "eventos.csv")
COLUMNAS_CSV = ["fecha", "hora", "estado", "distancia_cm", "foto"]
FOTO_PATH = "/tmp/agrosafe_ultima.jpg"

# Cámara ESP32-CAM (en la misma red WiFi). Su IP aparece en el Monitor Serie al encenderla.
# Se puede cambiar sin editar el código:  ESP32_CAM_URL=http://192.168.1.50/capture python3 agrosafe.py
ESP32_CAM_URL = os.environ.get("ESP32_CAM_URL", "http://192.168.1.50/capture")

# ---------------------------------------------------------------------------
# Cámara: ESP32-CAM por WiFi (principal) o cámara CSI de la Raspberry (respaldo).
# Si ninguna responde, el sistema sigue funcionando sin foto.
# ---------------------------------------------------------------------------
camara = None

try:
    from picamera2 import Picamera2

    camara = Picamera2()
    camara.configure(camara.create_still_configuration())
    camara.start()
    print("Cámara detectada.")

except Exception as e:
    camara = None
    print(f"Sin cámara: el sistema funciona igual. Detalle: {e}")


def foto_esp32cam():
    """Pide una foto a la ESP32-CAM (endpoint /capture) y la guarda en FOTO_PATH."""
    if not ESP32_CAM_URL:
        return False

    try:
        with urllib.request.urlopen(ESP32_CAM_URL, timeout=3) as respuesta:
            imagen = respuesta.read()

        with open(FOTO_PATH, "wb") as f:
            f.write(imagen)
        return True

    except Exception as e:
        print("ESP32-CAM no responde:", e)
        return False


def tomar_foto():
    """Toma una fotografía: primero con la ESP32-CAM y, si falla, con la cámara CSI."""
    if foto_esp32cam():
        return True

    if camara is None:
        return False

    try:
        camara.capture_file(FOTO_PATH)
        return True

    except Exception as e:
        print("Error al tomar foto:", e)
        return False


# ---------------------------------------------------------------------------
# GPIO y sensores
# ---------------------------------------------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO_PIN, GPIO.IN)


def medir_distancia_cm():
    """Mide la distancia con el HC-SR04. Devuelve -1 si no hay eco."""
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    limite = time.monotonic() + 0.05
    inicio = time.monotonic()

    while GPIO.input(ECHO_PIN) == 0:
        inicio = time.monotonic()

        if inicio > limite:
            return -1

    fin = time.monotonic()

    while GPIO.input(ECHO_PIN) == 1:
        fin = time.monotonic()

        if fin > limite + 0.05:
            return -1

    # Velocidad del sonido = 34300 cm/s; se divide por 2 (ida y vuelta)
    return round((fin - inicio) * 34300 / 2, 1)


# ---------------------------------------------------------------------------
# Registro de eventos: memoria (para el dashboard) + CSV (persistente)
# ---------------------------------------------------------------------------
eventos = []                 # Últimos eventos, el más reciente primero
historico = []               # Eventos "activado"/"descartado" (para estadísticas)
lock = threading.Lock()


def iniciar_csv():
    """Crea data/eventos.csv con encabezado si no existe y carga el histórico."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNAS_CSV)
        return

    # Si ya existía, se cargan las detecciones previas para no perder estadísticas
    with open(ARCHIVO_CSV, newline="") as f:
        for fila in csv.DictReader(f):
            if fila["estado"] in ("activado", "descartado"):
                historico.append(fila)


def registrar(estado, distancia, foto=False):
    """Registra un evento en memoria y lo agrega al CSV."""
    ahora = datetime.now()
    evento = {
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "estado": estado,
        "distancia_cm": distancia,
        "foto": foto,
    }

    with lock:
        eventos.insert(0, evento)
        del eventos[MAX_EVENTOS:]

        if estado in ("activado", "descartado"):
            historico.append(evento)

        # Se escribe inmediatamente para que el dato sobreviva a un corte de energía
        with open(ARCHIVO_CSV, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=COLUMNAS_CSV).writerow(evento)

    print(evento)


# ---------------------------------------------------------------------------
# Generación de información a partir de los datos
# ---------------------------------------------------------------------------
def calcular_estadisticas():
    """Transforma los eventos crudos en indicadores para el agricultor."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    hace_una_hora = datetime.now() - timedelta(hours=1)

    with lock:
        datos = list(historico)

    del_dia = [e for e in datos if e["fecha"] == hoy]
    activados_hoy = [e for e in del_dia if e["estado"] == "activado"]
    descartados_hoy = [e for e in del_dia if e["estado"] == "descartado"]

    ultima_hora = [
        e for e in activados_hoy
        if datetime.strptime(f"{e['fecha']} {e['hora']}", "%Y-%m-%d %H:%M:%S") >= hace_una_hora
    ]

    # Activaciones por hora del día (0-23): muestra en qué horario hay más conejos
    por_hora = Counter(int(e["hora"][:2]) for e in activados_hoy)

    distancias = [float(e["distancia_cm"]) for e in activados_hoy]
    total_detecciones = len(del_dia)

    return {
        "activaciones_hoy": len(activados_hoy),
        "descartes_hoy": len(descartados_hoy),
        # % de detecciones del PIR que el ultrasónico confirmó como cercanas
        "tasa_confirmacion": round(100 * len(activados_hoy) / total_detecciones, 1) if total_detecciones else 0,
        "distancia_promedio": round(sum(distancias) / len(distancias), 1) if distancias else 0,
        # Agua usada estimada = activaciones x segundos de rocío
        "segundos_rocio_hoy": len(activados_hoy) * TIEMPO_ACTIVACION_S,
        "activaciones_ultima_hora": len(ultima_hora),
        "alerta": len(ultima_hora) >= UMBRAL_ALERTA_HORA,
        "hora_peak": por_hora.most_common(1)[0][0] if por_hora else None,
        "por_hora": [por_hora.get(h, 0) for h in range(24)],
        "historico_total": len([e for e in datos if e["estado"] == "activado"]),
    }


# ---------------------------------------------------------------------------
# Lógica principal: sensores y actuador
# ---------------------------------------------------------------------------
def bucle_sensores():
    ultimo_beacon = 0
    preparado = False
    inactivo_desde = None

    while True:
        ahora = time.monotonic()

        # Registro periódico de "reposo" para evidenciar captura continua
        if ahora - ultimo_beacon >= INTERVALO_BEACON_S:
            registrar("reposo", medir_distancia_cm())
            ultimo_beacon = ahora

        movimiento = bool(GPIO.input(PIR_PIN))

        if not movimiento:
            if inactivo_desde is None:
                inactivo_desde = time.monotonic()

            elif time.monotonic() - inactivo_desde >= TIEMPO_REARME_S:
                preparado = True

        else:
            inactivo_desde = None

        if movimiento and preparado:
            # Consumir la detección para evitar activaciones repetidas
            # mientras la señal del PIR permanezca activa.
            preparado = False
            distancia = medir_distancia_cm()

            if 0 < distancia < DISTANCIA_MAXIMA_CM:
                GPIO.output(LED_PIN, GPIO.HIGH)

                try:
                    foto = tomar_foto()
                    registrar("activado", distancia, foto)
                    time.sleep(TIEMPO_ACTIVACION_S)

                finally:
                    GPIO.output(LED_PIN, GPIO.LOW)

                time.sleep(TIEMPO_REPOSO_S)

            else:
                registrar("descartado", distancia)
                time.sleep(1)

        time.sleep(0.1)


# ---------------------------------------------------------------------------
# Dashboard web (Flask)
# ---------------------------------------------------------------------------
app = Flask(__name__)

COLORES = {
    "activado": "#e74c3c",
    "descartado": "#f39c12",
    "reposo": "#27ae60",
}


def grafico_por_hora(por_hora):
    """Gráfico de barras (HTML/CSS puro, sin internet) de activaciones por hora."""
    maximo = max(por_hora) or 1
    barras = ""

    for hora, cantidad in enumerate(por_hora):
        alto = int(100 * cantidad / maximo)
        barras += (
            f"<div class='barra' title='{hora:02d}:00 - {cantidad} activaciones'>"
            f"<div style='height:{alto}%'></div><span>{hora}</span></div>"
        )

    return f"<div class='grafico'>{barras}</div>"


@app.route("/")
def dashboard():
    with lock:
        lista = list(eventos)

    est = calcular_estadisticas()
    ultimo = lista[0] if lista else None

    filas = ""

    for evento in lista:
        color = COLORES.get(evento["estado"], "#888")

        filas += (
            f"<tr><td>{evento['hora']}</td>"
            f"<td style='color:{color};font-weight:bold'>"
            f"{evento['estado']}</td>"
            f"<td>{evento['distancia_cm']} cm</td></tr>"
        )

    estado_html = "Esperando datos..."

    if ultimo:
        color = COLORES.get(ultimo["estado"], "#888")

        estado_html = (
            f"<span style='color:{color}'>"
            f"{ultimo['estado'].upper()}</span>"
            f" &middot; {ultimo['distancia_cm']} cm"
            f" &middot; {ultimo['hora']}"
        )

    alerta_html = ""

    if est["alerta"]:
        alerta_html = (
            "<div class='alerta'>⚠️ ALTA ACTIVIDAD: "
            f"{est['activaciones_ultima_hora']} activaciones en la última hora. "
            "Revisar el predio y el nivel del estanque de agua.</div>"
        )

    hora_peak = f"{est['hora_peak']:02d}:00" if est["hora_peak"] is not None else "—"

    foto_html = ""

    if camara is not None or ESP32_CAM_URL:
        foto_html = (
            "<h2>Última foto</h2>"
            f"<img src='/foto?t={time.time()}' style='max-width:100%'>"
        )

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="2">
<title>AGROSAFE</title>
<style>
body {{ font-family: sans-serif; max-width: 760px; margin: auto; padding: 16px; }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 6px; border-bottom: 1px solid #ddd; }}
.kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }}
.kpi {{ background: #f4f6f4; border-radius: 8px; padding: 10px; }}
.kpi b {{ display: block; font-size: 1.6em; }}
.alerta {{ background: #fdecea; color: #b03a2e; padding: 12px; border-radius: 8px; font-weight: bold; }}
.grafico {{ display: flex; align-items: flex-end; height: 140px; gap: 2px; }}
.barra {{ flex: 1; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; text-align: center; font-size: 10px; }}
.barra div {{ background: #e74c3c; min-height: 1px; }}
</style>
</head>
<body>
<h1>🐇 AGROSAFE</h1>
{alerta_html}
<h2>Estado actual</h2>
<p style="font-size:1.3em">{estado_html}</p>

<h2>Indicadores de hoy</h2>
<div class="kpis">
  <div class="kpi"><b>{est['activaciones_hoy']}</b>rocíos activados</div>
  <div class="kpi"><b>{est['descartes_hoy']}</b>detecciones descartadas (&gt; {DISTANCIA_MAXIMA_CM} cm)</div>
  <div class="kpi"><b>{est['tasa_confirmacion']} %</b>detecciones confirmadas</div>
  <div class="kpi"><b>{hora_peak}</b>hora de mayor actividad</div>
  <div class="kpi"><b>{est['distancia_promedio']} cm</b>distancia promedio</div>
  <div class="kpi"><b>{est['segundos_rocio_hoy']} s</b>tiempo total de rocío</div>
</div>

<h2>Activaciones por hora (hoy)</h2>
{grafico_por_hora(est['por_hora'])}
<p>Total histórico de activaciones: {est['historico_total']} &middot;
<a href="/datos.csv">Descargar datos (CSV)</a></p>

{foto_html}
<h2>Últimos eventos</h2>
<table>{filas}</table>
</body>
</html>"""


@app.route("/api/estadisticas")
def api_estadisticas():
    """Indicadores en formato JSON (útil para pruebas y análisis)."""
    return jsonify(calcular_estadisticas())


@app.route("/datos.csv")
def descargar_csv():
    """Descarga el histórico completo para analizarlo en Excel/R."""
    return send_file(ARCHIVO_CSV, mimetype="text/csv", as_attachment=True,
                     download_name="agrosafe_eventos.csv")


@app.route("/foto")
def foto():
    try:
        return send_file(FOTO_PATH, mimetype="image/jpeg")

    except Exception:
        return "Sin foto aún", 404


# ---------------------------------------------------------------------------
# Inicio del sistema
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        iniciar_csv()

        hilo_sensores = threading.Thread(target=bucle_sensores, daemon=True)
        hilo_sensores.start()

        app.run(host="0.0.0.0", port=5000)

    except KeyboardInterrupt:
        print("Cierre solicitado por el usuario.")

    finally:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.cleanup()

        if camara is not None:
            camara.stop()
