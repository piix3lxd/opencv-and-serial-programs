import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
import os

# Crear ventana, definir tamaño y título
ventana = tk.Tk()
ventana.geometry("740x460")
ventana.resizable(0, 0)
ventana.title("Tomar foto webcam")

# Variables globales
capture = None
Captura = None
ruta_destino = None
ejecutar_solo_una_vez = True

# Funciones relacionadas con la cámara web
def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

def iniciar():
    global capture
    if capture is not None:
        ret, frame = capture.read()
        if ret:
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

# Función para tomar una foto única
def CapturarG():
    global Captura
    cam = capture
    ret, image = cam.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img

# Función para tomar fotos con temporización
def capturarG_con_temporizacion():
    global ejecutar_solo_una_vez
    if ejecutar_solo_una_vez:
        messagebox.showwarning("Advertencia", "Se están guardando fotogramas en un ciclo infinito, no olvides cerrar el programa o tu disco duro colapsará")
    ejecutar_solo_una_vez = False

    global Captura
    cam = capture
    ret, image = cam.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img
    # Programa la próxima captura
    guardar_imagen()
    ventana.after(1000 * int(numeroTemp.get()), capturarG_con_temporizacion)

# Función para seleccionar una carpeta de destino
def seleccionar_carpeta():
    global ruta_destino
    ruta_destino = filedialog.askdirectory()
    if ruta_destino:
        guardar_boton.config(state=tk.NORMAL)
        carpeta_seleccionada_label.config(text=f"Carpeta seleccionada: {ruta_destino}")

# Función para guardar una imagen en la carpeta seleccionada
def guardar_imagen():
    global Captura, ruta_destino
    if Captura is not None and ruta_destino:
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
        
        file_name = entrada_nombre_archivo.get() + ".png"
        ruta_guardar = os.path.join(ruta_destino, file_name)
        
        contador = 1
        while os.path.exists(ruta_guardar):
            contador += 1
            file_name = entrada_nombre_archivo.get() + f"({contador})" + ".png"
            ruta_guardar = os.path.join(ruta_destino, file_name)

        imagen_pil = Image.fromarray(Captura)
        imagen_pil.save(ruta_guardar)
        
        print(f"Fotografía guardada como {ruta_guardar}")

# Etiqueta para mostrar la imagen de la cámara web
etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.pack()

# Cuadro de imagen gris, donde se reproducirá la webcam
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)

# Cuadro de imagen gris, donde se mostrará la imagen capturada
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=390, y=50, width=300, height=240)

# Label instructivo para indicar que antes de tomar una foto temporizada se debe seleccionar una carpeta para que se guarde la imagen
labelInstructivo = tk.Label(ventana, text="Antes de tomar una foto con temporización, seleccione una carpeta y elija un nombre para el archivo.")
labelInstructivo.place(x =30, y = 420)

# Etiqueta para mostrar la carpeta seleccionada
carpeta_seleccionada_label = tk.Label(ventana, text="")
carpeta_seleccionada_label.pack()
carpeta_seleccionada_label.place(x=250, y=400)

# Botón para seleccionar carpeta de destino
carpeta_seleccionar_button = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
carpeta_seleccionar_button.pack(pady=10)
carpeta_seleccionar_button.place(x=570, y=380)

# Botón para guardar la imagen
guardar_boton = tk.Button(ventana, text="Guardar Imagen", command=guardar_imagen, state=tk.DISABLED)
guardar_boton.pack(pady=10)
guardar_boton.place(x=580, y=420)

# Botón para iniciar la cámara web
BCamara = tk.Button(ventana, text="Iniciar cámara", command=camara)
BCamara.place(x=150, y=330, width=90, height=23)

# Botón para capturar una foto única
BCapturarUnica = tk.Button(ventana, text="Tomar foto única", command=CapturarG)
BCapturarUnica.place(x=500, y=305, width=100, height=23)

# Botón para capturar imágenes con temporización
BCapturarTemporizada = tk.Button(ventana, text="Tomar foto temporizada", command=capturarG_con_temporizacion)
BCapturarTemporizada.place(x=500, y=345, width=150, height=23)

# Etiqueta y entrada para el nombre del archivo
label_nombre_archivo = tk.Label(ventana, text="Nombre para la imagen: ")
label_nombre_archivo.place(x=100, y=380)
entrada_nombre_archivo = tk.Entry(ventana, width=50)
entrada_nombre_archivo.place(x=250, y=380)

# SpinBox para seleccionar los segundos de la temporización
numeroTemp = tk.Spinbox(ventana, from_=1, to=60)
numeroTemp.place(x=450, y=345, width=42, height=23)

# Iniciar la interfaz gráfica
ventana.mainloop()
