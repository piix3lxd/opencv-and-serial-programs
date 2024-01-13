import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import imutils
import cv2
from tkinter import filedialog
import os

# Crea ventana, define tamaño y título
ventana = tk.Tk()
ventana.geometry("1070x450")
ventana.resizable(0, 0)
ventana.title("Generador de templates")

# Funciones cámara web
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

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

# Función para tomar una foto
def Capturar():
    global Captura
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=280)
    frame = imutils.resize(frame, height=240)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img

def umbralizacion():
    global thresh1, umbralizacion_realizada
    valor = int(numeroUmbra.get())
    ret, thresh1 = cv2.threshold(Captura, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(thresh1)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    LImagenROI.configure(image=Umbral)
    LImagenROI.image = Umbral

    # Habilitar el botón "Recortar" después de realizar la umbralización
    umbralizacion_realizada = True
    BRecortar.config(state=tk.NORMAL)

def mostrar_coordenadas(event):
    coordenadas['text'] = f'x = {event.y}    y = {event.x}'

def guardar_imagen():
    global ImgRec
    global ruta_destino
    if thresh1 is not None and ruta_destino:
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        file_name = entrada_nombre_archivo.get() + ".png"  # Nombre de archivo en entry"
        ruta_guardar = os.path.join(ruta_destino, file_name)

        # Verificar si el archivo ya existe y agregar un número
        contador = 1

        while os.path.exists(ruta_guardar):
            contador += 1
            file_name = entrada_nombre_archivo.get() + f"({contador})" + ".png"
            ruta_guardar = os.path.join(ruta_destino, file_name)

        imagen_pil = Image.fromarray(ImgRec)
        imagen_pil.save(ruta_guardar)

        print(f"Fotografía guardada como {ruta_guardar}")

def seleccionar_carpeta():
    global ruta_destino
    ruta_destino = filedialog.askdirectory()  # Abre el cuadro de diálogo para seleccionar una carpeta
    if ruta_destino:
        guardar_boton.config(state=tk.NORMAL)  # Habilita el botón "Guardar Imagen"

        carpeta_seleccionada_label.config(text=f"Carpeta seleccionada: {ruta_destino}")

def recortar():
    global ImgRec
    Vx1 = int(x1.get())
    Vy1 = int(y1.get()) + 10
    Vx2 = int(x2.get())
    Vy2 = int(y2.get())
    ImgRec = thresh1[Vx1:Vx2, Vy1:Vy2]
    Im = Image.fromarray(ImgRec)
    ImRec = ImageTk.PhotoImage(image=Im)
    LImagenRecorte.configure(image=ImRec)
    LImagenRecorte.image = ImRec
    guardar_imagen()

# SpinBox
numeroUmbra = tk.Spinbox(ventana, from_=0, to=255)
numeroUmbra.place(x=450, y=331, width=42, height=23)
# Botones
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=80, y=330, width=90, height=23)
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar)
BCapturar.place(x=220, y=330, width=91, height=23)
BRecortar = tk.Button(ventana, text="Recortar", command=recortar, state=tk.DISABLED)
BRecortar.place(x=800, y=400, width=80, height=23)
Umbra = tk.Button(ventana, text="Umbralizacion", command=umbralizacion)
Umbra.place(x=500, y=330, width=80, height=23)

# Botón para seleccionar una carpeta para guardar las imágenes
carpeta_seleccionar_button = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
carpeta_seleccionar_button.pack(pady=10)
carpeta_seleccionar_button.place(x=570, y=380)

# Label para que el usuario ingrese el nombre del archivo
label_nombre_archivo = tk.Label(ventana, text="Nombre para la imagen recortada: ")
label_nombre_archivo.place(x=60, y=380)

# Entrada para el nombre del archivo
entrada_nombre_archivo = tk.Entry(ventana, width=50)
entrada_nombre_archivo.place(x=250, y=380)

# Botón para guardar la imagen
guardar_boton = tk.Button(ventana, text="Guardar Imagen", command=guardar_imagen, state=tk.DISABLED)
guardar_boton.pack(pady=10)
guardar_boton.place(x=580, y=420)

# Etiqueta para mostrar la carpeta seleccionada
carpeta_seleccionada_label = tk.Label(ventana, text="")
carpeta_seleccionada_label.pack()
carpeta_seleccionada_label.place(x=250, y=400)

# Cuadros de imagen gris
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=390, y=50, width=300, height=240)
LImagenRecorte = tk.Label(ventana, background="gray")
LImagenRecorte.place(x=730, y=50, width=300, height=240)

# Coordenadas x e y
LImagenROI.bind('<Button-1>', mostrar_coordenadas)

# Label - Texto
coordenadasTitulo = tk.Label(ventana, text="Coordenadas")
coordenadasTitulo.place(x=505, y=10)
coordenadas = tk.Label(ventana, text="")
coordenadas.place(x=495, y=25)
Lx1 = tk.Label(ventana, text="x1")
Lx1.place(x=790, y=330)
Ly1 = tk.Label(ventana, text="y1")
Ly1.place(x=890, y=330)
Lx2 = tk.Label(ventana, text="x2")
Lx2.place(x=790, y=360)
Ly2 = tk.Label(ventana, text="y2")
Ly2.place(x=890, y=360)

# Spinbox - Escoger número coordenadas para recortar la foto
x1 = tk.Spinbox(ventana, from_=0, to=298)
x1.place(x=810, y=330, width=42, height=22)
y1 = tk.Spinbox(ventana, from_=0, to=239)
y1.place(x=910, y=330, width=42, height=22)
x2 = tk.Spinbox(ventana, from_=1, to=298)
x2.place(x=810, y=360, width=42, height=22)
y2 = tk.Spinbox(ventana, from_=1, to=239)
y2.place(x=910, y=360, width=42, height=22)
ventana.mainloop()
