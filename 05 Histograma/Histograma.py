import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
#Ventana
ventana = tk.Tk()
ventana.geometry("485x354")
ventana.title("Comunicacion Serial Arduino")
#Funciones
def click_rojo():
    SerialPort1.write(b"rojo")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_verde():
    SerialPort1.write(b"verde")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_amarillo():
    SerialPort1.write(b"amarillo")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_conectar():
    if SerialPort1.isOpen() == False:
        SerialPort1.baudrate = 9600
        SerialPort1.bytesize = 8
        SerialPort1.parity = "N"
        SerialPort1.stopbits = serial.STOPBITS_ONE
        SerialPort1.port = comboBox1.get()
        SerialPort1.open()
        TextoEstado["state"] = "normal"
        TextoEstado.delete(1.0, tk.END)
        TextoEstado.insert(1.0, "Conectado")
        TextoEstado.configure(background="LIME")
        messagebox.showinfo(message="Puerto Conectado ")
        TextoEstado["state"] = "disabled"     
def click_desconectar():
    if SerialPort1.isOpen() == True:
        SerialPort1.close()
        TextoEstado["state"] = "normal"
        TextoEstado.delete(1.0, tk.END)
        TextoEstado.insert(1.0 , "Desconectado")
        TextoEstado.configure(background="red")
        messagebox.showinfo(message="Puerto Desconectado")
        TextoEstado["state"] = "disabled"
def click_enviar():
    msj = TextEnviar.get(1.0, tk.END)
    lista = msj.split("\n")
    for x in lista:
        a = 0
        if x == "":
            pass
        elif x.__contains__("Run"):
            SerialPort1.write(x.encode()+b"\r")
            while(a == 0):
                aux = SerialPort1.read_all()
                if b"ok" in aux:
                    a = 1
                    TextRecibidos.insert(1.0, b"Done.\n")
                    messagebox.showinfo(message="Enviado Correctamente", title="Resultado")
                time.sleep(1)
        else:
            SerialPort1.write(x.encode()+b"\r")
            time.sleep(2+int(ComboBoxT.get()))
            TextEnviar.delete(1.0, tk.END)
            TextRecibidos.delete(1.0, tk.END)
            aux = SerialPort1.read_all()
            if b"Done." in aux:
                TextRecibidos.insert(1.0, b"Done.\n")
                
    messagebox.showinfo(message="Enviado Correctamente", title="Resultado")

#Label
LDatosEnviados = tk.Label(ventana, text="Datos Enviados")
LDatosEnviados.place(x= 180, y=100, width=80, height=15)
LDatosRecibidos = tk.Label(ventana, text="Datos Recibidos")
LDatosRecibidos.place(x= 345, y=100, width=85, height=16)
LNota = tk.Label(ventana, text="NOTA: Recuerde seleccionar\nun valor para el temporizador")
LNota.place(x = 120, y= 250)
#Botones
BotonConectar = tk.Button(ventana, text="Conectar", command=click_conectar)
BotonDesconectar = tk.Button(ventana, text="Desconectar", command=click_desconectar)
BotonEnviar = tk.Button(ventana, text="Enviar", command=click_enviar)
BotonRojo = tk.Button(ventana, text="Rojo", command=click_rojo)
BotonVerde = tk.Button(ventana, text="Verde", command=click_verde)
BotonAmarillo = tk.Button(ventana, text="Amarillo",command=click_amarillo)
BotonConectar.place(x = 70, y=40, width=75, height=23)
BotonDesconectar.place(x = 310, y= 40, width=75, height=23)
BotonRojo.place(x = 40, y= 100, width=75, height=23)
BotonVerde.place(x = 40, y= 130, width=75, height=23)
BotonAmarillo.place(x = 40, y= 160, width=75, height=23)
BotonEnviar.place(x = 170, y= 190, width=75, height=23)
#Combobox
comboBox1 = ttk.Combobox(
    state="readonly",
    values = ["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8"],
    )
comboBox1.set("COM1")
comboBox1.place(x = 160, y=40, width=140, height=22)
ComboBoxT = ttk.Combobox(
    state="readonly",
    values=[0,1,2,3,4,5,6,7,8,9]
)
ComboBoxT.set(0)
ComboBoxT.place(x = 160, y=60, width=140, height=22)
#Text
TextEnviar = tk.Text(ventana)
TextEnviar.place(x = 140, y=120, width=160, height=60)
TextRecibidos = tk.Text(ventana)
TextRecibidos.place(x = 310, y=120, width=160, height=140)
TextoEstado = tk.Text(ventana)
TextoEstado.place(x= 170, y= 10, width=110, height=20)
TextoEstado.insert(1.0,"DESCONECTADO")
TextoEstado["state"] = "disabled"
#Serial
SerialPort1 = serial.Serial()
ventana.mainloop()