"""
Prueba de software de AgroSafe en simulación (sin Raspberry).
Usa el programa real (software/src/agrosafe.py) y la función real detectar_estrella(),
pero reemplaza los sensores por gpiozero.py (simulado) y la cámara por imágenes
sintéticas: una estrella (figura objetivo) o un círculo/cuadrado (otro objeto).

Escenarios: figura a 30 cm, figura a 80 cm y otro objeto a 30 cm, 10 intentos cada uno.
Ejecutar desde esta carpeta:  python3 simulacion.py
Los eventos quedan en software/data/eventos.csv y el resumen en resultado_simulacion.json.
"""
import sys, time, random, csv, json, math
from collections import Counter
import numpy as np, cv2
sys.path.insert(0, "../../software/src")  # usa el programa real
import agrosafe as A
random.seed(6); np.random.seed(6)

def imagen(tipo, k):
    img = np.full((480, 640, 3), 220, np.uint8)
    img = cv2.add(img, np.random.randint(0, 15, img.shape, dtype=np.uint8))
    cx, cy = 320 + random.randint(-60, 60), 240 + random.randint(-40, 40)
    R = random.randint(80, 120); ang = random.uniform(0, 2 * math.pi)
    if tipo == "estrella":
        pts = [(cx + (R if i % 2 == 0 else R * 0.42) * math.cos(ang + i * math.pi / 5),
                cy + (R if i % 2 == 0 else R * 0.42) * math.sin(ang + i * math.pi / 5)) for i in range(10)]
        cv2.fillPoly(img, [np.array(pts, np.int32)], (40, 40, 40))
    elif k % 2:
        cv2.circle(img, (cx, cy), R, (40, 40, 40), -1)
    else:
        box = cv2.boxPoints(((cx, cy), (1.6 * R, 1.6 * R), math.degrees(ang)))
        cv2.fillPoly(img, [box.astype(np.int32)], (40, 40, 40))
    return img

ESC = [("Figura a ~30 cm", 30, "estrella", True),
       ("Figura a ~80 cm", 80, "estrella", False),
       ("Otro objeto a ~30 cm", 30, "otro", False)]
A.iniciar_csv()
rele = A.DigitalOutputDevice(27); pir = A.MotionSensor(17); us = A.DistanceSensor()
res = {}; lat = []
for nombre, dist, tipo, esperado in ESC:
    act = 0
    for k in range(10):
        A.capturar = (lambda t=tipo, kk=k: imagen(t, kk))
        us.cm = dist; pir.motion_detected = True
        t0 = time.monotonic()
        A.registrar("Movimiento detectado.", "deteccion")
        if A.evaluar(pir, us):
            rele.on(); lat.append(rele.on_times[-1] - t0)
            A.registrar("Estrella confirmada. Pulso de 2 segundos.", "activacion")
            rele.off(); A.registrar("Relé apagado.")
            act += 1
        pir.motion_detected = False
    res[nombre] = {"activado": act, "descartado": 10 - act, "acierto": (act if esperado else 10 - act) * 10}
filas = list(csv.DictReader(open(A.ARCHIVO_CSV)))
json.dump({"res": res, "lat": lat, "csv": dict(Counter(f["tipo"] for f in filas)), "filas": len(filas),
           "est": A.calcular_estadisticas()}, open("resultado_simulacion.json", "w"), indent=1, ensure_ascii=False)
