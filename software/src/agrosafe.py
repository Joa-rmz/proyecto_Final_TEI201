"""
AgroSafe - Protección inteligente de cultivos (TEI201 - Grupo 6)
Programa del dispositivo (Raspberry Pi 4 Model B).

Ciclo: PIR detecta movimiento -> HC-SR04 confirma distancia (15-50 cm, 3 lecturas)
-> 2 capturas de la cámara con reconocimiento de la figura objetivo
-> se vuelve a verificar la distancia -> relé de la bomba 2 s -> pausa 5 s.

[Avance 3] Cada evento se guarda en data/eventos.csv (persiste al reiniciar) y el
dashboard muestra indicadores calculados a partir del histórico.

Requiere el módulo agrosafe_integracion_prueba_v2.py (capturar, detectar_estrella)
en la misma carpeta. Ejecutar:  python3 agrosafe.py  ->  http://<IP-Raspberry>:5000
"""
import csv
import os
import threading
import time
from collections import Counter, deque
from datetime import datetime, timedelta

from flask import Flask, jsonify, render_template_string, send_file
from gpiozero import DigitalOutputDevice, MotionSensor, DistanceSensor
from werkzeug.serving import make_server

from agrosafe_integracion_prueba_v2 import capturar, detectar_estrella


app = Flask(__name__)
lock = threading.Lock()
eventos = deque(maxlen=50)

estado = {
    "fase": "Iniciando",
    "distancia": None,
    "movimiento": False,
    "rele": False,
    "captura": "Sin analizar",
    "actualizado": "",
}


def actualizar(**datos):
    with lock:
        estado.update(datos)
        estado["actualizado"] = datetime.now().strftime("%H:%M:%S")


# ---------------------------------------------------------------------------
# [Avance 3] Repositorio de datos: CSV persistente + histórico para indicadores
# ---------------------------------------------------------------------------
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, "eventos.csv")
COLUMNAS_CSV = ["fecha", "hora", "tipo", "mensaje", "distancia_cm"]
UMBRAL_ALERTA_HORA = 5      # >= 5 activaciones en la última hora -> alerta
historico = []              # eventos de tipo deteccion / activacion / descarte


def iniciar_csv():
    """Crea data/eventos.csv con encabezado o recarga el histórico si ya existe."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNAS_CSV)
        return
    with open(ARCHIVO_CSV, newline="") as f:
        for fila in csv.DictReader(f):
            if fila["tipo"] in ("deteccion", "activacion", "descarte"):
                historico.append(fila)


def registrar(mensaje, tipo="info"):
    """Registra un evento en el historial de la sesión y lo agrega al CSV.
    tipo: info | deteccion | activacion | descarte | error"""
    ahora = datetime.now()
    hora = ahora.strftime("%H:%M:%S")
    with lock:
        eventos.appendleft({"hora": hora, "mensaje": mensaje})
        fila = {
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": hora,
            "tipo": tipo,
            "mensaje": mensaje,
            "distancia_cm": estado.get("distancia"),
        }
        if tipo in ("deteccion", "activacion", "descarte"):
            historico.append(fila)
        # Se escribe de inmediato para que el dato sobreviva a un corte de energía
        try:
            with open(ARCHIVO_CSV, "a", newline="") as f:
                csv.DictWriter(f, fieldnames=COLUMNAS_CSV).writerow(fila)
        except OSError as error:
            print(f"No se pudo guardar en CSV: {error}", flush=True)
    print(f"{hora} {mensaje}", flush=True)


def calcular_estadisticas():
    """[Avance 3] Transforma el histórico en indicadores para el agricultor."""
    hoy = datetime.now().strftime("%Y-%m-%d")
    hace_una_hora = datetime.now() - timedelta(hours=1)
    with lock:
        datos = [e for e in historico if e["fecha"] == hoy]
    detecciones = [e for e in datos if e["tipo"] == "deteccion"]
    activaciones = [e for e in datos if e["tipo"] == "activacion"]
    descartes = [e for e in datos if e["tipo"] == "descarte"]
    ultima_hora = [
        e for e in activaciones
        if datetime.strptime(f"{e['fecha']} {e['hora']}", "%Y-%m-%d %H:%M:%S") >= hace_una_hora
    ]
    por_hora = Counter(int(e["hora"][:2]) for e in activaciones)
    return {
        "detecciones_hoy": len(detecciones),
        "activaciones_hoy": len(activaciones),
        "descartes_hoy": len(descartes),
        # % de movimientos detectados que terminaron en activación de la bomba
        "tasa_confirmacion": round(100 * len(activaciones) / len(detecciones), 1) if detecciones else 0,
        "segundos_bomba_hoy": len(activaciones) * 2,
        "activaciones_ultima_hora": len(ultima_hora),
        "alerta": len(ultima_hora) >= UMBRAL_ALERTA_HORA,
        "hora_peak": por_hora.most_common(1)[0][0] if por_hora else None,
        "por_hora": [por_hora.get(h, 0) for h in range(24)],
    }


HTML = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AgroSafe</title>
<style>
body{
    font-family:system-ui;
    background:#eef3ef;
    color:#183126;
    max-width:850px;
    margin:auto;
    padding:24px;
}
h1{margin-bottom:4px}
.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
    gap:12px;
    margin:20px 0;
}
.card{
    background:white;
    padding:20px;
    border-radius:12px;
}
.label{font-size:14px;color:#52645b}
.value{font-size:22px;font-weight:600;margin-top:8px}
table{width:100%;border-collapse:collapse;background:white}
th,td{text-align:left;padding:12px;border-bottom:1px solid #ddd}
#conexion{font-weight:bold}
</style>
</head>
<body>
<h1>AgroSafe</h1>
<p id="conexion">Conectando...</p>

<div class="grid">
    <div class="card">
        <div class="label">Estado</div>
        <div class="value" id="fase">—</div>
    </div>
    <div class="card">
        <div class="label">Última distancia</div>
        <div class="value" id="distancia">—</div>
    </div>
    <div class="card">
        <div class="label">Detección de movimiento</div>
        <div class="value" id="movimiento">—</div>
    </div>
    <div class="card">
        <div class="label">Bomba de agua</div>
        <div class="value" id="rele">—</div>
    </div>
    <div class="card">
        <div class="label">Último reconocimiento</div>
        <div class="value" id="captura">—</div>
    </div>
</div>

<div id="alerta" style="display:none;background:#fdecea;color:#b03a2e;padding:14px;border-radius:12px;font-weight:600"></div>
<h2>Indicadores de hoy</h2>
<div class="grid">
    <div class="card"><div class="label">Movimientos detectados</div><div class="value" id="i_det">—</div></div>
    <div class="card"><div class="label">Activaciones de la bomba</div><div class="value" id="i_act">—</div></div>
    <div class="card"><div class="label">Detecciones descartadas</div><div class="value" id="i_des">—</div></div>
    <div class="card"><div class="label">% confirmadas</div><div class="value" id="i_tasa">—</div></div>
    <div class="card"><div class="label">Hora de mayor actividad</div><div class="value" id="i_peak">—</div></div>
    <div class="card"><div class="label">Tiempo total de bomba</div><div class="value" id="i_seg">—</div></div>
</div>
<h2>Activaciones por hora (hoy)</h2>
<div id="grafico" style="display:flex;align-items:flex-end;height:120px;gap:2px;background:white;padding:10px;border-radius:12px"></div>
<p><a href="/datos.csv">Descargar historial completo (CSV)</a></p>

<p id="actualizado"></p>
<h2>Historial de esta sesión</h2>
<table>
    <thead>
        <tr><th>Hora</th><th>Evento</th></tr>
    </thead>
    <tbody id="historial"></tbody>
</table>

<script>
const texto=(id,valor)=>{
    document.getElementById(id).textContent=valor;
};

async function refrescar(){
    try{
        const r=await fetch('/api/estado',{
            cache:'no-store',
            signal:AbortSignal.timeout(4000)
        });

        if(!r.ok) throw new Error('Sin respuesta');
        const d=await r.json();

        texto('conexion','● Panel conectado');
        document.getElementById('conexion').style.color='#187044';
        texto('fase',d.fase);
        texto(
            'distancia',
            d.distancia===null?'Sin lectura':d.distancia+' cm'
        );
        texto(
            'movimiento',
            d.movimiento?'Movimiento':'Sin movimiento'
        );
        texto('rele',d.rele?'ENCENDIDA':'Apagada');

        // Cambio de texto únicamente; no cambia el detector.
        texto(
            'captura',
            d.captura
                .replace(/ESTRELLA/g,'CONEJO')
                .replace(/Estrella/g,'Conejo')
                .replace(/estrella/g,'conejo')
        );

        texto(
            'actualizado',
            'Última actualización del control: '+d.actualizado
        );

        // [Avance 3] indicadores calculados desde el CSV
        const s=d.estadisticas;
        texto('i_det',s.detecciones_hoy);
        texto('i_act',s.activaciones_hoy);
        texto('i_des',s.descartes_hoy);
        texto('i_tasa',s.tasa_confirmacion+' %');
        texto('i_peak',s.hora_peak===null?'—':String(s.hora_peak).padStart(2,'0')+':00');
        texto('i_seg',s.segundos_bomba_hoy+' s');
        const al=document.getElementById('alerta');
        al.style.display=s.alerta?'block':'none';
        al.textContent='ALTA ACTIVIDAD: '+s.activaciones_ultima_hora+' activaciones en la última hora. Revisar el predio y el estanque de agua.';
        const g=document.getElementById('grafico');
        g.replaceChildren();
        const max=Math.max(1,...s.por_hora);
        s.por_hora.forEach((n,h)=>{
            const b=document.createElement('div');
            b.style.cssText='flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;font-size:10px;height:100%';
            const barra=document.createElement('div');
            barra.style.cssText='width:100%;background:#2f7a4c;min-height:1px;height:'+(100*n/max)+'%';
            barra.title=h+':00 - '+n+' activaciones';
            const lab=document.createElement('span'); lab.textContent=h;
            b.append(barra,lab); g.appendChild(b);
        });

        const tabla=document.getElementById('historial');
        tabla.replaceChildren();

        for(const e of d.eventos){
            const fila=document.createElement('tr');
            for(const valor of [e.hora,e.mensaje]){
                const celda=document.createElement('td');
                celda.textContent=valor;
                fila.appendChild(celda);
            }
            tabla.appendChild(fila);
        }
    }catch(e){
        texto(
            'conexion',
            '● Sin conexión: no se puede confirmar el estado'
        );
        document.getElementById('conexion').style.color='#b33232';

        for(const id of [
            'fase','distancia','movimiento','rele','captura'
        ]){
            texto(id,'Sin datos actuales');
        }
    }finally{
        setTimeout(refrescar,1000);
    }
}

refrescar();
</script>
</body>
</html>
"""


@app.get("/")
def inicio():
    return render_template_string(HTML)


@app.get("/api/estado")
def datos():
    with lock:
        contenido = dict(estado)
        contenido["eventos"] = list(eventos)
    contenido["estadisticas"] = calcular_estadisticas()

    respuesta = jsonify(contenido)
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@app.get("/datos.csv")
def descargar_csv():
    """[Avance 3] Descarga del histórico completo para análisis en Excel/R."""
    return send_file(ARCHIVO_CSV, mimetype="text/csv", as_attachment=True,
                     download_name="agrosafe_eventos.csv")


def leer_sensores(pir, sensor):
    cm = float(sensor.distance * 100)
    if not 0 < cm < 200:
        cm = None

    actualizar(
        distancia=round(cm, 1) if cm is not None else None,
        movimiento=bool(pir.motion_detected),
    )
    return cm


def comprobar_distancia(pir, sensor):
    lecturas = []
    for _ in range(3):
        lecturas.append(leer_sensores(pir, sensor))
        time.sleep(0.2)

    return all(
        cm is not None and 15 <= cm <= 50
        for cm in lecturas
    )


def esperar(segundos, pir, sensor):
    fin = time.monotonic() + segundos
    while time.monotonic() < fin:
        leer_sensores(pir, sensor)
        time.sleep(0.2)


def esperar_rearme(pir, sensor):
    actualizar(fase="Esperando que termine el movimiento")
    while True:
        leer_sensores(pir, sensor)
        if not pir.motion_detected:
            return
        time.sleep(0.2)


def evaluar(pir, sensor):
    actualizar(
        fase="Comprobando distancia",
        captura="Sin analizar",
    )

    if not comprobar_distancia(pir, sensor):
        registrar("Distancia fuera del rango. Sin activación.", "descarte")
        return False

    for numero in (1, 2):
        actualizar(fase=f"Analizando captura {numero}/2")
        imagen = capturar()
        estrella = detectar_estrella(imagen)
        resultado = "Estrella" if estrella else "Sin estrella"

        actualizar(captura=f"{numero}/2: {resultado}")
        registrar(f"Captura {numero}/2: {resultado}")

        if not estrella:
            registrar("Figura descartada. Sin activación.", "descarte")
            return False

        if numero == 1:
            time.sleep(0.5)

    actualizar(fase="Verificando distancia final")
    if not comprobar_distancia(pir, sensor):
        registrar("La distancia cambió. Sin activación.", "descarte")
        return False

    return True


def controlar(rele, pir, sensor):
    registrar("Control iniciado. Relé apagado.")
    esperar(2, pir, sensor)
    esperar_rearme(pir, sensor)

    while True:
        actualizar(fase="Esperando movimiento")
        leer_sensores(pir, sensor)

        if not pir.motion_detected:
            time.sleep(0.2)
            continue

        registrar("Movimiento detectado.", "deteccion")

        try:
            if evaluar(pir, sensor):
                actualizar(fase="Activando bomba")
                try:
                    rele.on()
                    actualizar(rele=True)
                    registrar(
                        "Estrella confirmada. Pulso de 2 segundos.",
                        "activacion",
                    )
                    time.sleep(2)
                finally:
                    rele.off()
                    actualizar(rele=False)
                    registrar("Relé apagado.")

        except Exception as error:
            rele.off()
            actualizar(
                rele=False,
                fase="Error",
                captura="No confirmado",
            )
            registrar(f"Intento cancelado: {error}", "error")

        finally:
            rele.off()
            actualizar(rele=False)

        actualizar(fase="Pausa de 5 segundos")
        esperar(5, pir, sensor)
        esperar_rearme(pir, sensor)


def main():
    iniciar_csv()   # [Avance 3]
    with DigitalOutputDevice(
        27,
        active_high=True,
        initial_value=False,
    ) as rele:
        try:
            with MotionSensor(17) as pir, DistanceSensor(
                echo=24,
                trigger=23,
                max_distance=2,
            ) as sensor:
                servidor = make_server(
                    "0.0.0.0",
                    5000,
                    app,
                    threaded=True,
                )
                hilo = threading.Thread(
                    target=servidor.serve_forever,
                    daemon=True,
                )
                hilo.start()

                try:
                    controlar(rele, pir, sensor)
                finally:
                    rele.off()
                    actualizar(rele=False, fase="Detenido")
                    servidor.shutdown()
                    servidor.server_close()

        finally:
            rele.off()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa detenido.", flush=True)