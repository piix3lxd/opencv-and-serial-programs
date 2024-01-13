# Importamos las bibliotecas necesarias
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
import numpy as np

# Creamos la ventana principal con título
ventana = tk.Tk()
ventana.geometry("1400x730")
ventana.resizable(0, 0)
ventana.title("Umbralización RGB")

# Función para iniciar la cámara
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

# Función para mostrar la imagen de la cámara
def iniciar():
    global capture
    if capture is not None:
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagen.after(1, iniciar)
        else:
            LImagen.image = ""
            capture.release()

# Función para capturar una foto
def Capturar():
    global Captura
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img


# Función para umbralizar cada canal y mostrar los resultados
def umbralizar(n):
    canal_r, canal_g, canal_b = cv2.split(Captura)
    umbral_r_min = int(SRedI.get())
    umbral_g_min = int(SGreenI.get())
    umbral_b_min = int(SBlueI.get())
    umbral_r_max = int(SRedD.get())
    umbral_g_max = int(SGreenD.get())
    umbral_b_max = int(SBlueD.get())

    umbralizado_r = cv2.threshold(canal_r, umbral_r_min, umbral_r_max, cv2.THRESH_BINARY)[1]
    umbralizado_g = cv2.threshold(canal_g, umbral_g_min, umbral_g_max, cv2.THRESH_BINARY)[1]
    umbralizado_b = cv2.threshold(canal_b, umbral_b_min, umbral_b_max, cv2.THRESH_BINARY)[1]
    imagen_umbralizada = cv2.merge((umbralizado_r, umbralizado_g, umbralizado_b))

    if n == 1:
        im = Image.fromarray(umbralizado_r)
        img = ImageTk.PhotoImage(image=im)
        ImagenRed.configure(image=img)
        ImagenRed.image = img
    elif n == 2:
        im = Image.fromarray(umbralizado_g)
        img = ImageTk.PhotoImage(image=im)
        ImagenGreen.configure(image=img)
        ImagenGreen.image = img
    elif n == 3:
        im = Image.fromarray(umbralizado_b)
        img = ImageTk.PhotoImage(image=im)
        ImagenBlue.configure(image=img)
        ImagenBlue.image = img
    elif n == 4:
        im = Image.fromarray(imagen_umbralizada)
        img = ImageTk.PhotoImage(image=im)
        ImagenUmbra.configure(image=img)
        ImagenUmbra.image = img

# Creación de escalas para la umbralización RGB
SRedD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedD.set(255)
SRedD.place(x=220, y=630)
SGreenD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenD.set(255)
SGreenD.place(x=550, y=630)
SBlueD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueD.set(255)
SBlueD.place(x=900, y=630)

SRedI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedI.place(x=80, y=630)
SGreenI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenI.place(x=410, y=630)
SBlueI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueI.place(x=760, y=630)

# Botones para las acciones
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=500, y=330, width=90, height=23)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=840, y=330, width=91, height=23)

# Etiquetas para mostrar las imágenes
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=390, y=50, width=300, height=240)
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=730, y=50, width=300, height=240)

ImagenRed = tk.Label(ventana, background="gray")
ImagenRed.place(x=50, y=380, width=300, height=240)
ImagenGreen = tk.Label(ventana, background="gray")
ImagenGreen.place(x=390, y=380, width=300, height=240)
ImagenBlue = tk.Label(ventana, background="gray")
ImagenBlue.place(x=730, y=380, width=300, height=240)
ImagenUmbra = tk.Label(ventana, background="gray")
ImagenUmbra.place(x=1070, y=380, width=300, height=240)

# Etiquetas para indicar los canales R, G y B
LRed = tk.Label(ventana, text="R")
LRed.place(x=190, y=650, width=21, height=16)
LGreen = tk.Label(ventana, text="G")
LGreen.place(x=520, y=650, width=21, height=16)
LBlue = tk.Label(ventana, text="B")
LBlue.place(x=870, y=650, width=21, height=16)

# Botones para umbralizar los canales y fusionarlos
BRojo = tk.Button(ventana, text="Umbralizar en R", command=lambda: umbralizar(1))
BRojo.place(x=135, y=680, width=120, height=25)
BVerde = tk.Button(ventana, text="Umbralizar en G", command=lambda: umbralizar(2))
BVerde.place(x=465, y=680, width=120, height=25)
BAzul = tk.Button(ventana, text="Umbralizar en B", command=lambda: umbralizar(3))
BAzul.place(x=795, y=680, width=120, height=25)
BUmbralizar = tk.Button(ventana, text="Imagen Fusionada", command=lambda: umbralizar(4))
BUmbralizar.place(x=1155, y=640, width=120, height=25)

# Ejecución de la ventana principal
ventana.mainloop()
