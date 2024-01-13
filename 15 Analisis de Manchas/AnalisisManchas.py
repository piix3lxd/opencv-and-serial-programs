# Importación de bibliotecas necesarias
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import cv2

# Creación de la ventana principal
ventana = tk.Tk()
ventana.geometry("1320x470")
ventana.resizable(0, 0)
ventana.title("Análisis de Manchas")

# Funciones de la cámara web
def camara():
    global capture
    # Iniciar la cámara
    capture = cv2.VideoCapture(0)
    iniciar()

def iniciar():
    global capture
    # Mostrar la captura en tiempo real
    if capture is not None:
        ret, frame = capture.read()
        if ret:
            # Redimensionar el marco para mostrarlo en la ventana
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

# Función para capturar una imagen
def Capturar():
    global CapturaG
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    CapturaG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imG = Image.fromarray(CapturaG)
    imgG = ImageTk.PhotoImage(image=imG)
    LImagenROI.configure(image=imgG)
    LImagenROI.image = imgG

# Función para umbralizar en escala de grises
def umbralizar_escala_grises():
    global bin_image
    valor = int(numeroUmbra.get())
    ret, bin_image = cv2.threshold(CapturaG, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(bin_image)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    ImagenUmbra.configure(image=Umbral)
    ImagenUmbra.image = Umbral

# Función para contar manchas negras en la imagen
def contar_manchas_negras():
    # Invertir la imagen para contar manchas negras
    imagen_invertida = cv2.bitwise_not(bin_image)
    
    # Contar el número de píxeles con manchas negras
    num_pixels_con_manchas_negras = cv2.countNonZero(imagen_invertida)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = (num_pixels_con_manchas_negras / bin_image.size) * 100

    # Contar manchas negras
    contornos_negros, _ = cv2.findContours(imagen_invertida, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cantidad_manchas_negras = len(contornos_negros)
    Cadena = f"Cantidad de manchas negras: {cantidad_manchas_negras}\nPorcentaje área con manchas: {round(porcentaje_manchas, 2)}%"
    CajaTextoNegro.configure(state='normal')
    CajaTextoNegro.delete(1.0, tk.END)
    CajaTextoNegro.insert(1.0, Cadena)
    CajaTextoNegro.configure(state='disabled')

# Función para contar manchas blancas en la imagen
def contar_manchas_blancas():
    # Contar el número de píxeles con manchas blancas
    num_pixels_con_manchas_blancas = cv2.countNonZero(bin_image)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = (num_pixels_con_manchas_blancas / bin_image.size) * 100

    # Contar manchas blancas
    contornos_blancos, _ = cv2.findContours(bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cantidad_manchas_blancas = len(contornos_blancos)

    Cadena = f"Cantidad de manchas blancas: {cantidad_manchas_blancas}\nPorcentaje área con manchas: {round(porcentaje_manchas, 2)}%"
    CajaTextoBlanco.configure(state='normal')
    CajaTextoBlanco.delete(1.0, tk.END)
    CajaTextoBlanco.insert(1.0, Cadena)
    CajaTextoBlanco.configure(state='disabled')

# Botones para controlar las funciones
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=150, y=330, width=90, height=23)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=500, y=330, width=91, height=23)
Umbra = tk.Button(ventana, text="Umbralización", command=umbralizar_escala_grises)
Umbra.place(x=840, y=380, width=80, height=23)
ManchasNegras = tk.Button(ventana, text="Análisis de manchas negras", command=contar_manchas_negras)
ManchasNegras.place(x=1090, y=170, width=160, height=23)
ManchasBlancas = tk.Button(ventana, text="Análisis de manchas blancas", command=contar_manchas_blancas)
ManchasBlancas.place(x=1090, y=325, width=160, height=23)

# Cuadros de imagen para mostrar la cámara web, la captura y la imagen umbralizada
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=390, y=50, width=300, height=240)
ImagenUmbra = tk.Label(ventana, background="gray")
ImagenUmbra.place(x=730, y=50, width=300, height=240)

# Cuadros de texto para mostrar resultados
CajaTextoBlanco = tk.Text(ventana, state="disabled")
CajaTextoBlanco.place(x=1055, y=210, width=225, height=100)

CajaTextoNegro = tk.Text(ventana, state="disabled")
CajaTextoNegro.place(x=1055, y=50, width=225, height=100)

# SpinBox para seleccionar el umbral en escala de grises
numeroUmbra = tk.Spinbox(ventana, from_=0, to=255)
numeroUmbra.place(x=850, y=331, width=42, height=23)

# Ejecución de la ventana principal
ventana.mainloop()
