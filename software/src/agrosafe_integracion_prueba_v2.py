import subprocess
import time

import cv2
import numpy as np


URL_CAMARA = "http://10.77.103.105/capture"


def capturar():
    respuesta = subprocess.run(
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--max-time", "10",
            URL_CAMARA,
        ],
        capture_output=True,
        timeout=12,
        check=True,
    )

    imagen = cv2.imdecode(
        np.frombuffer(respuesta.stdout, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if imagen is None:
        raise ValueError("La cámara no devolvió una imagen válida.")

    return imagen


def detectar_estrella(imagen):
    # Convertir la fotografía a tonos de gris.
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Suavizar pequeños detalles y ruido.
    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    # Separar figuras oscuras del fondo claro.
    _, mascara = cv2.threshold(
        gris,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # Buscar también los contornos interiores.
    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    alto, ancho = gris.shape
    detectada = False

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        # Descartar figuras muy pequeñas o demasiado grandes.
        if not 300 < area < alto * ancho * 0.8:
            continue

        x, y, w, h = cv2.boundingRect(contorno)

        # Descartar figuras cortadas por los bordes.
        if (
            x <= 1
            or y <= 1
            or x + w >= ancho - 1
            or y + h >= alto - 1
        ):
            continue

        # Aproximar el contorno mediante un polígono.
        perimetro = cv2.arcLength(contorno, True)
        poligono = cv2.approxPolyDP(
            contorno,
            0.02 * perimetro,
            True,
        )

        puntos = poligono[:, 0, :].astype(float)
        vertices = len(puntos)

        # Comparar el área de la figura con su envolvente convexa.
        envolvente = cv2.contourArea(
            cv2.convexHull(contorno)
        )
        solidez = area / envolvente if envolvente else 1

        # Calcular el sentido del giro en cada vértice.
        giros = []
        for i in range(vertices):
            a = puntos[i] - puntos[i - 1]
            b = puntos[(i + 1) % vertices] - puntos[i]
            cruz = a[0] * b[1] - a[1] * b[0]
            giros.append(np.sign(cruz))

        # Buscar cinco puntas y cinco entrantes alternados.
        alternan = vertices == 10 and all(
            giros[i] * giros[(i + 1) % vertices] < 0
            for i in range(vertices)
        )

        estrella = alternan and 0.35 < solidez < 0.75
        detectada = detectada or estrella

        etiqueta = "ESTRELLA" if estrella else "OTRO CONTORNO"
        print(
            f"  {etiqueta}: {vertices} vertices, "
            f"solidez={solidez:.2f}",
            flush=True,
        )

        color = (0, 255, 0) if estrella else (0, 0, 255)
        cv2.drawContours(imagen, [poligono], -1, color, 2)

    return detectada


def prueba_dos_capturas():
    resultados = []
    print("Prueba de reconocimiento. No se controla ningún GPIO.")

    try:
        for numero in (1, 2):
            print(f"\nCaptura {numero}/2...", flush=True)
            imagen = capturar()
            estrella = detectar_estrella(imagen)
            resultados.append(estrella)

            cv2.imwrite(
                f"/tmp/agrosafe-resultado-{numero}.jpg",
                imagen,
            )

            print(
                "ESTRELLA DETECTADA" if estrella else "SIN ESTRELLA",
                flush=True,
            )

            if numero == 1:
                time.sleep(0.5)

    except Exception as error:
        print(f"ERROR: {error}")
        print("ESTRELLA NO CONFIRMADA.")
        return

    if all(resultados):
        print("\nESTRELLA CONFIRMADA EN DOS CAPTURAS.")
    else:
        print("\nESTRELLA NO CONFIRMADA.")


if __name__ == "__main__":
    prueba_dos_capturas()