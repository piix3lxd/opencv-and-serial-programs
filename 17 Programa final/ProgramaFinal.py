import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
import math

# Agregar a la foto recortada y umbralizada la misma función actualizada del código para guardarla
# Crea una ventana, define tamaño y título
ventana = tk.Tk()
ventana.geometry("1320x800")
ventana.resizable(0, 0)
ventana.title("Proyecto de procesamiento de imágenes con Webcam")

# Variables globales
global Captura, CapturaG

# Inicia la cámara web
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

def iniciar():
    global capture
    if capture is not None:
        BCapturar.place(x=250, y=330, width=91, height=23)
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagen.after(10, iniciar)
        else:
            LImagen.image = ""
            capture.release()

def Capturar():
    global valor, Captura, CapturaG
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    CapturaG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    imG = Image.fromarray(CapturaG)
    imgG = ImageTk.PhotoImage(image=imG)
    GImagenROI.configure(image=imgG)
    GImagenROI.image = imgG
    LImagenRecorte.configure(image=img)
    LImagenRecorte.image = img

def rgb():
    global img_mask, img_aux, bin_imagen
    Minimos = (int(SRedI.get()), int(SGreenI.get()), int(SBlueI.get()))
    maximos = (int(SRedD.get()), int(SGreenD.get()), int(SBlueD.get()))
    img_mask = cv2.inRange(ImgRec, Minimos, maximos)
    img_aux = img_mask
    img_mask = Image.fromarray(img_mask)
    img_mask = ImageTk.PhotoImage(image=img_mask)
    LImagenManchas.configure(image=img_mask)
    LImagenManchas.image = img_mask
    _, bin_imagen = cv2.threshold(img_aux, 0, 255, cv2.THRESH_BINARY_INV)

def umbralizar_escala_grises():
    global thresh1
    valor = int(numeroUmbra.get())
    ret, thresh1 = cv2.threshold(CapturaG, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(thresh1)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    UImagen.configure(image=Umbral)
    UImagen.image = Umbral

def umbralizar_rgb_a_escala_grises():
    global thresh2
    valor = int(numeroUmbraR.get())
    ret1, thresh2 = cv2.threshold(imagen_umbralizadaG, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(thresh2)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    LImagenManchas.configure(image=Umbral)
    LImagenManchas.image = Umbral

def contar_manchas_blancas(boton):

    if boton == 1:
        num_pixels_con_manchas_blancas = cv2.countNonZero(thresh1)
        porcentaje_manchas = 100 - (num_pixels_con_manchas_blancas / thresh1.size) * 100
        contornos_blancos, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cantidad_manchas_blancas = len(contornos_blancos)
        Cadena = f"Cantidad de manchas blancas: {cantidad_manchas_blancas}\nPorcentaje de área con manchas: {round(100 - porcentaje_manchas, 2)}%"
        CajaTexto1.configure(state='normal')
        CajaTexto1.delete(1.0, tk.END)
        CajaTexto1.insert(1.0, Cadena)
        CajaTexto1.configure(state='disabled')
    elif boton == 2:
        num_pixels_con_manchas_blancas = cv2.countNonZero(thresh2)
        porcentaje_manchas = 100 - (num_pixels_con_manchas_blancas / thresh2.size) * 100
        contornos_blancos, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cantidad_manchas_blancas = len(contornos_blancos)
        Cadena = f"Cantidad de manchas blancas: {cantidad_manchas_blancas}\nPorcentaje de área con manchas: {round(100 - porcentaje_manchas, 2)}%"
        CajaTexto3.configure(state='normal')
        CajaTexto3.delete(1.0, tk.END)
        CajaTexto3.insert(1.0, Cadena)
        CajaTexto3.configure(state='disabled')

def contar_manchas_negras(boton):

    if boton == 1:
        imagen_invertida = cv2.bitwise_not(thresh1)
        num_pixels_con_manchas_negras = cv2.countNonZero(imagen_invertida)
        porcentaje_manchas = 100 - (num_pixels_con_manchas_negras / thresh1.size) * 100
        contornos_negros, _ = cv2.findContours(imagen_invertida, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cantidad_manchas_negras = len(contornos_negros)
        Cadena = f"Cantidad de manchas negras: {cantidad_manchas_negras}\nPorcentaje de área con manchas: {round(100 - porcentaje_manchas, 2)}%"
        CajaTexto2.configure(state='normal')
        CajaTexto2.delete(1.0, tk.END)
        CajaTexto2.insert(1.0, Cadena)
        CajaTexto2.configure(state='disabled')
    if boton == 2:
        imagen_invertida = cv2.bitwise_not(thresh2)
        num_pixels_con_manchas_negras = cv2.countNonZero(imagen_invertida)
        porcentaje_manchas = 100 - (num_pixels_con_manchas_negras / thresh2.size) * 100
        contornos_negros, _ = cv2.findContours(imagen_invertida, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cantidad_manchas_negras = len(contornos_negros)
        Cadena = f"Cantidad de manchas negras: {cantidad_manchas_negras}\nPorcentaje de área con manchas: {round(100 - porcentaje_manchas, 2)}%"
        CajaTexto4.configure(state='normal')
        CajaTexto4.delete(1.0, tk.END)
        CajaTexto4.insert(1.0, Cadena)
        CajaTexto4.configure(state='disabled')

def umbralizar_rgb():
    # Dividimos la matriz en los 3 canales
    global imagen_umbralizada, imagen_umbralizadaG
    canal_r, canal_g, canal_b = cv2.split(ImgRec)
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
    imagen_umbralizadaG = cv2.cvtColor(imagen_umbralizada, cv2.COLOR_RGB2GRAY)
    im = Image.fromarray(imagen_umbralizada)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img

def mostrar_coordenadas(event):
    coordenadas['text'] = f'x = {event.x}    y = {event.y}'

def recortar():
    global ImgRec
    Vx1 = int(x1.get())
    Vy1 = int(y1.get())
    Vx2 = int(x2.get())
    Vy2 = int(y2.get())
    ImgRec = Captura[Vx1:Vx2, Vy1:Vy2]
    Im = Image.fromarray(ImgRec)
    ImRec = ImageTk.PhotoImage(image=Im)
    LImagenRecorte.configure(image=ImRec)
    LImagenRecorte.image = ImRec


# Botones
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=60, y=330, width=90, height=23)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=250, y=330, width=91, height=23)
BManchas = tk.Button(ventana, text="Umbralización", command=umbralizar_rgb_a_escala_grises)
BManchas.place(x=800, y=640, width=100, height=23)
ManchasRGB_B = tk.Button(ventana, text="Análisis de manchas blancas", command=lambda: contar_manchas_blancas(2))
ManchasRGB_B.place(x=1090, y=490, width=160, height=23)
ManchasRGB_N = tk.Button(ventana, text="Análisis de manchas negras", command=lambda: contar_manchas_negras(2))
ManchasRGB_N.place(x=1090, y=640, width=160, height=23)
BBinary = tk.Button(ventana, text="Umbralización", command=umbralizar_escala_grises)
BBinary.place(x=800, y=310, width=90, height=23)
BManchasN = tk.Button(ventana, text="Análisis de manchas negras", command=lambda: contar_manchas_negras(1))
BManchasN.place(x=1090, y=310, width=160, height=23)
BManchasB = tk.Button(ventana, text="Análisis de manchas blancas", command=lambda: contar_manchas_blancas(1))
BManchasB.place(x=1090, y=160, width=160, height=23)
BRecortar = tk.Button(ventana, text="Recortar", command=recortar)
BRecortar.place(x=155, y=765, width=80, height=23)
BUmbralizar = tk.Button(ventana, text="Umbralizar y fusionar", command=umbralizar_rgb)
BUmbralizar.place(x=465, y=750, width=130, height=25)

# SpinBox
numeroUmbra = tk.Spinbox(ventana, from_=0, to=255)
numeroUmbra.place(x=900, y=310, width=42, height=22)
numeroUmbraR = tk.Spinbox(ventana, from_=0, to=255)
numeroUmbraR.place(x=910, y=640, width=42, height=22)

x1 = tk.Spinbox(ventana, from_=0, to=298)
x1.place(x=140, y=700, width=42, height=22)
y1 = tk.Spinbox(ventana, from_=0, to=239)
y1.place(x=240, y=700, width=42, height=22)
x2 = tk.Spinbox(ventana, from_=1, to=298)
x2.place(x=140, y=730, width=42, height=22)
y2 = tk.Spinbox(ventana, from_=1, to=239)
y2.place(x=240, y=730, width=42, height=22)

# Label
LRed = tk.Label(ventana, text="R")
LRed.place(x=530, y=640, width=21, height=16)
LGreen = tk.Label(ventana, text="G")
LGreen.place(x=530, y=680, width=21, height=16)
LBlue = tk.Label(ventana, text="B")
LBlue.place(x=530, y=720, width=21, height=16)
coordenadasTitulo = tk.Label(ventana, text="Coordenadas")
coordenadasTitulo.place(x=160, y=630)
coordenadas = tk.Label(ventana, text="")
coordenadas.place(x=150, y=650)
Lx1 = tk.Label(ventana, text="x1")
Lx1.place(x=120, y=700)
Ly1 = tk.Label(ventana, text="y1")
Ly1.place(x=220, y=700)
Lx2 = tk.Label(ventana, text="x2")
Lx2.place(x=120, y=730)
Ly2 = tk.Label(ventana, text="y2")
Ly2.place(x=220, y=730)

# Logo Universidad
logo = tk.PhotoImage(file="LogoUBB.png")
logoUBB = ttk.Label(image=logo)
logoUBB.place(x=1250, y=635)

# Nombre alumno - carrera - profesor - Lab CIM
alumnas = tk.Label(ventana, text="Estudiantes practicantes\n\nLuis Pereira").place(x=1075, y=690)
carrera = tk.Label(ventana, text="Ingeniería Civil Informática").place(x=1060, y=760)
profesor = tk.Label(ventana, text="Profesor\nLuis Vera").place(x=1250, y=710)
LabCIM = tk.Label(ventana, text="Lab CIM").place(x=1250, y=760)

# Cuadros de Imagen grises
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=390, y=380, width=300, height=240)
GImagenROI = tk.Label(ventana, background="gray")
GImagenROI.place(x=390, y=50, width=300, height=240)
UImagen = tk.Label(ventana, background="gray")
UImagen.place(x=730, y=50, width=301, height=240)
LImagenManchas = tk.Label(ventana, background="gray")
LImagenManchas.place(x=730, y=380, width=301, height=240)
LImagenRecorte = tk.Label(ventana, background="gray")
LImagenRecorte.place(x=50, y=380, width=301, height=240)
LImagenRecorte.bind('<Button-1>', mostrar_coordenadas)

# Cuadro de Texto
CajaTexto1 = tk.Text(ventana, state="disabled")
CajaTexto1.place(x=1055, y=50, width=225, height=100)

CajaTexto2 = tk.Text(ventana, state="disabled")
CajaTexto2.place(x=1055, y=200, width=225, height=100)

CajaTexto3 = tk.Text(ventana, state="disabled")
CajaTexto3.place(x=1055, y=380, width=225, height=100)

CajaTexto4 = tk.Text(ventana, state="disabled")
CajaTexto4.place(x=1055, y=380+150, width=225, height=100)

# RGB se inicia en 1, ya que si no sale error de división por 0
SRedI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedI.place(x=400, y=620)
SGreenI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenI.place(x=400, y=660)
SBlueI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueI.place(x=400, y=700)

SRedD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SRedD.set(255)
SRedD.place(x=580, y=620)
SGreenD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SGreenD.set(255)
SGreenD.place(x=580, y=660)
SBlueD = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueD.set(255)
SBlueD.place(x=580, y=700)

# Pasos
paso1 = tk.Label(ventana, text="Iniciar la cámara y tomar una foto")
paso1.place(x=90, y=20)
paso2 = tk.Label(ventana, text="Visualización imagen en escala de grises")
paso2.place(x=420, y=20)
paso3 = tk.Label(ventana, text="Escribir las coordenadas para recortar la foto")
paso3.place(x=80, y=670)
paso4a = tk.Label(ventana, text="Elegir un número entre 0 y 255 para umbralizar la\nimagen en escala de grises")
paso4a.place(x=750, y=10)
paso4b = tk.Label(ventana, text="Elegir un rango de número entre 0 y 255 para \numbralizar la imagen\n\n Aquí se umbraliza la imagen fusionada\n de la izquierda covertida a gris")
paso4b.place(x=750, y=700)
paso5 = tk.Label(ventana, text="Analizar las manchas")
paso5.place(x=1130, y=20)

ventana.mainloop()
