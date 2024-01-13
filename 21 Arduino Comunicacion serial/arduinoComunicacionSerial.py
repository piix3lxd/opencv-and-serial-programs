import tkinter as tk
from tkinter import ttk, messagebox
import serial
import cv2
import imutils
from PIL import Image, ImageTk

def camara():
    global capture
    capture = cv2.VideoCapture(0)
    iniciar()

def iniciar():
    global capture
    if capture is not None:
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=440)
            frame = imutils.resize(frame, height=360)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagen.after(1, iniciar)
        else:
            LImagen.image = ""
            capture.release()

# Boton
ventana = tk.Tk()
ventana.geometry("1150x480")
ventana.title("Comunicacion Serial Arduino y Cámara")

# Variable global
tiempo_espera = 0
carrera_camara = None

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Funciones
def click_rojo():
    enviar_datos("rojo")

def click_verde():
    enviar_datos("azul")

def click_amarillo():
    enviar_datos("amarillo")

def click_temperatura():
    limpiar_datos()
    programar_envio("temperatura")

def click_humedad():
    limpiar_datos()
    programar_envio("humedad")

def click_conectar():
    if not SerialPort1.isOpen():
        SerialPort1.baudrate = 9600
        SerialPort1.bytesize = 8
        SerialPort1.parity = "N"
        SerialPort1.stopbits = serial.STOPBITS_ONE
        SerialPort1.port = comboBox1.get()
        SerialPort1.open()
        actualizar_estado("Conectado", "LIME")
        # Iniciar la función para mostrar la cámara

def click_desconectar():
    detener_camara()
    if SerialPort1.isOpen():
        SerialPort1.close()
        actualizar_estado("Desconectado", "red")

def click_enviar():
    msj = TextEnviar.get(1.0, tk.END).strip()
    if msj.lower() == "temperatura":
        # Enviar la solicitud de temperatura inmediatamente
        enviar_datos("temperatura")
    else:
        programar_envio(msj)

def enviar_rgb():
    r = str(int(r_spinbox.get()))
    g = str(int(g_spinbox.get()))
    b = str(int(b_spinbox.get()))
    mensaje = f"{r},{g},{b}"
    SerialPort1.write(mensaje.encode() + b"\r")


def detener_camara():
    global carrera_camara
    if carrera_camara is not None:
        ventana.after_cancel(carrera_camara)
        carrera_camara = None


def enviar_datos(mensaje):
    SerialPort1.write(mensaje.encode() + b"\r")
    datos = SerialPort1.read_all().decode()
    TextRecibidos.insert(1.0, datos)

def limpiar_datos():
    TextRecibidos.delete(1.0, tk.END)

def actualizar_estado(mensaje, color):
    TextoEstado["state"] = "normal"
    TextoEstado.delete(1.0, tk.END)
    TextoEstado.insert(1.0, mensaje)
    TextoEstado.configure(background=color)
    TextoEstado["state"] = "disabled"
    messagebox.showinfo(message=f"Puerto {mensaje}")

def actualizar_tiempo_espera(event):
    global tiempo_espera
    tiempo_espera = int(ComboBoxT.get())

def programar_envio(mensaje):
    ventana.after(tiempo_espera * 1000, lambda: enviar_datos(mensaje))

# Componentes de la interfaz gráfica
BotonConectar = tk.Button(ventana, text="Conectar", command=click_conectar)
BotonDesconectar = tk.Button(ventana, text="Desconectar", command=click_desconectar)
BotonRojo = tk.Button(ventana, text="Rojo", command=click_rojo)
BotonVerde = tk.Button(ventana, text="Azul", command=click_verde)
BotonAmarillo = tk.Button(ventana, text="Amarillo", command=click_amarillo)
BotonTemperatura = tk.Button(ventana, text="Temperatura", command=click_temperatura)
BotonHumedad = tk.Button(ventana, text="Humedad", command=click_humedad)

BotonConectar.place(x=70, y=40, width=75, height=23)
BotonDesconectar.place(x=310, y=40, width=75, height=23)
BotonRojo.place(x=40, y=100, width=75, height=23)
BotonVerde.place(x=40, y=130, width=75, height=23)
BotonAmarillo.place(x=40, y=160, width=75, height=23)
BotonTemperatura.place(x=40, y=190, width=75, height=23)
BotonHumedad.place(x=40, y=220, width=75, height=23)

# Marco para agrupar botones y etiqueta
MarcoBotones = tk.Frame(ventana, bd=2, relief=tk.GROOVE)
MarcoBotones.place(x=120, y=330, width=180, height=110)

# Botón para enviar RGB
BotonEnviarRGB = tk.Button(MarcoBotones, text="Enviar RGB", command=enviar_rgb)
BotonEnviarRGB.grid(row=0, column=0, padx=10, pady=10)

# Botón para enviar datos
BotonEnviarDatos = tk.Button(MarcoBotones, text="Enviar texto", command=click_enviar)
BotonEnviarDatos.grid(row=0, column=1, padx=10, pady=10)

# Etiqueta de doble clic
EtiquetaDobleClic = tk.Label(MarcoBotones, text="Hacer\n doble clic\n en botón", fg="blue")
EtiquetaDobleClic.grid(row=1, column=0, columnspan=2, pady=5)

comboBox1 = ttk.Combobox(
    state="readonly",
    values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"],
)
comboBox1.set("COM1")
comboBox1.place(x=160, y=40, width=140, height=22)

ComboBoxT = ttk.Combobox(
    state="readonly",
    values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 60, 3600, 84600]
)
ComboBoxT.set(0)
ComboBoxT.place(x=160, y=285, width=140, height=22)
ComboBoxT.bind("<<ComboboxSelected>>", actualizar_tiempo_espera)

LabelEnviar = tk.Label(ventana, text="Enviar datos")
LabelEnviar.place(x=140, y=100, width=160, height=15)

LabelRecibir = tk.Label(ventana, text="Recibir datos")
LabelRecibir.place(x=310, y=100, width=160, height=15)

LabelTemporizador = tk.Label(ventana, text="Temporizador\n en segundos:")
LabelTemporizador.place(x = 60, y = 275)


TextEnviar = tk.Text(ventana)
TextEnviar.place(x=140, y=120, width=160, height=60)

TextRecibidos = tk.Text(ventana)
TextRecibidos.place(x=310, y=120, width=160, height=140)

TextoEstado = tk.Text(ventana)
TextoEstado.place(x=170, y=10, width=110, height=20)
TextoEstado.insert(1.0, "DESCONECTADO")
TextoEstado["state"] = "disabled"
LabelRojo = tk.Label(ventana, text="Rojo:")
LabelRojo.place(x=150, y=190, width=75, height=23)
r_spinbox = ttk.Spinbox(ventana, from_=0, to=255)
r_spinbox.place(x=210, y=190, width=50, height=23)

LabelVerde = tk.Label(ventana, text="Verde:")
LabelVerde.place(x=150, y=220, width=75, height=23)
g_spinbox = ttk.Spinbox(ventana, from_=0, to=255)
g_spinbox.place(x=210, y=220, width=50, height=23)

LabelAzul = tk.Label(ventana, text="Azul:")
LabelAzul.place(x=150, y=250, width=75, height=23)
b_spinbox = ttk.Spinbox(ventana, from_=0, to=255)
b_spinbox.place(x=210, y=250, width=50, height=23)

# Botón para iniciar la cámara
BCamara = tk.Button(ventana, text="Iniciar Camara", command=camara)
BCamara.place(x=720, y=440, width=90, height=23)

# Cuadro de imagen gris, donde se reproducirá la webcam
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=550, y=50, width=450, height=360)


SerialPort1 = serial.Serial()
ventana.mainloop()
