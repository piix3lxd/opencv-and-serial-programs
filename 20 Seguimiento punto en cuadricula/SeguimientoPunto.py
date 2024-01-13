import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Variables globales
puntos_interseccion = []
gris_anterior = None
punto_seleccionado = None

def mostrar_imagen(imagen):
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(imagen_rgb)
    img = ImageTk.PhotoImage(img)

    panel_imagen.img = img
    panel_imagen.config(image=img)

def actualizar_coordenadas(x, y):
    texto_coordenadas.set("Coordenadas seleccionadas: ({}, {})".format(x, y))
    guardar_coordenadas(x, y)

def guardar_coordenadas(x, y):
    with open("coordenadas.txt", "a") as archivo:
        archivo.write("Coordenadas: ({}, {})\n".format(x, y))

def procesar_imagen():
    global gris_anterior, punto_seleccionado, puntos_interseccion

    # Obtener el valor actual del slidebar
    umbral_canny = slidebar_canny.get()

    # Capturar un fotograma de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar la imagen de la cámara")
        return

    # Convertir a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(desenfoque, umbral_canny, 2 * umbral_canny)

    # Inicializar la lista de puntos de intersección
    puntos_interseccion = []

    # Rastrear el punto solo si se ha seleccionado uno
    if punto_seleccionado is not None:
        # Rastrear el punto usando el método de Lucas-Kanade
        p0 = np.array([punto_seleccionado], dtype=np.float32)

        # Crear una copia de la imagen original para el seguimiento óptico
        frame_con_puntos = frame.copy()

        # Mostrar las intersecciones en la imagen copiada
        for punto_interseccion in puntos_interseccion:
            cv2.circle(frame_con_puntos, punto_interseccion, 5, (255, 0, 0), -1)

        # Utilizar la imagen con puntos de intersección para el seguimiento óptico
        p1, st, err = cv2.calcOpticalFlowPyrLK(gris_anterior, gris, p0, None, **lk_params)

        # Actualizar la posición del punto seleccionado si el seguimiento es exitoso
        if st is not None and st[0][0] == 1:
            punto_seleccionado = (int(p1[0][0]), int(p1[0][1]))

    # Dibujar el punto en la imagen
    if punto_seleccionado is not None:
        cv2.circle(frame, punto_seleccionado, 5, (0, 255, 0), -1)

    # Detectar líneas en la imagen usando HoughLinesP
    lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Dibujar las líneas en la imagen
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Buscar intersección de las líneas
        puntos_interseccion = encontrar_puntos_interseccion(lineas)

    # Mostrar las intersecciones en la imagen
    for punto_interseccion in puntos_interseccion:
        cv2.circle(frame, punto_interseccion, 5, (255, 0, 0), -1)

    # Mostrar la imagen con el punto rastreado y las líneas
    mostrar_imagen(frame)

    # Actualizar la imagen anterior
    gris_anterior = gris.copy()

    # Actualizar las coordenadas
    if punto_seleccionado is not None:
        actualizar_coordenadas(punto_seleccionado[0], punto_seleccionado[1])

    # Llamar recursivamente para procesar el siguiente fotograma después de 1 segundo
    ventana.after(1000, procesar_imagen)

def encontrar_puntos_interseccion(lineas):
    puntos_interseccion = []

    for i in range(len(lineas)):
        for j in range(i + 1, len(lineas)):
            x1, y1, x2, y2 = lineas[i][0]
            x3, y3, x4, y4 = lineas[j][0]

            # Calcular la intersección de las líneas
            det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if det != 0:
                px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
                py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det
                puntos_interseccion.append((int(px), int(py)))

    return puntos_interseccion

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Seguimiento de Punto")

# Iniciar la cámara
cap = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

# Parámetros para el seguimiento óptico de Lucas-Kanade
lk_params = {
    'winSize': (15, 15),
    'maxLevel': 2,
    'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
}

# Panel para mostrar la imagen
panel_imagen = tk.Label(ventana)
panel_imagen.pack()

# Slidebar para ajustar el umbral de Canny
slidebar_canny = tk.Scale(ventana, from_=0, to=200, orient=tk.HORIZONTAL, label="Umbral Canny", length=300, resolution=1)
slidebar_canny.set(50)  # Valor inicial
slidebar_canny.pack(pady=10)

# Label para mostrar las coordenadas
texto_coordenadas = tk.StringVar()
label_coordenadas = tk.Label(ventana, textvariable=texto_coordenadas, font=("Arial", 12))
label_coordenadas.pack(pady=10)

# Inicializar el punto seleccionado (None al principio)
punto_seleccionado = None

# Inicializar la imagen anterior para el seguimiento óptico
ret, frame = cap.read()
gris_anterior = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Función para cerrar la cámara cuando se cierra la ventana
def cerrar_ventana():
    cap.release()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Manejar clic en la imagen
def clic_en_imagen(event):
    global punto_seleccionado
    x, y = event.x, event.y
    punto_seleccionado = (x, y)
    actualizar_coordenadas(x, y)

panel_imagen.bind("<Button-1>", clic_en_imagen)

# Iniciar el procesamiento de la imagen
procesar_imagen()

ventana.mainloop()
