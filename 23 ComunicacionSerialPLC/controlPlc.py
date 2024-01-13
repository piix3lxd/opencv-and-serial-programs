import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time

class ScorbotController:
    def __init__(self):
        self.serial_port = None
        self.thread_leer_datos = None
        self.response_buffer = ""  # Variable para almacenar la respuesta parcial


    def conectar_robot(self, port):
        try:
            self.serial_port = serial.Serial(port, baudrate=9600, timeout=1, bytesize=7, parity="E", stopbits=2)
            self.thread_leer_datos = threading.Thread(target=self.leer_datos_continuamente, daemon=True)
            self.thread_leer_datos.start()
            messagebox.showinfo(message="Conexión exitosa con el robot.")
        except Exception as e:
            messagebox.showerror(message=f"Error al conectar con el robot: {e}")

    def desconectar_robot(self):
        try:
            if self.thread_leer_datos and self.thread_leer_datos.is_alive():
                self.thread_leer_datos.join()
            if self.serial_port and self.serial_port.isOpen():
                self.serial_port.close()
                messagebox.showinfo(message="Desconexión exitosa del robot.")
        except Exception as e:
            messagebox.showerror(message=f"Error al desconectar el robot: {e}")

    def enviar_instruccion(self, instruccion):
        try:
            if self.serial_port and self.serial_port.isOpen():
                # Limpiar el búfer antes de enviar una nueva instrucción
                self.response_buffer = ""

                # Agregar un carácter de retorno de carro al final de la instrucción
                instruccion = f"{instruccion}\r"
                self.serial_port.write(instruccion.encode())
                messagebox.showinfo(message="Instrucción enviada correctamente.")

                # Agregar una pausa antes de leer los datos
                time.sleep(0.23)

                # Leer datos después de la pausa
                datos = self.serial_port.read_all().decode()
                time.sleep(0.15)
                if datos:
                    TextRecibidos.insert(tk.END, datos)
                    if "Done" in datos or "OK" in datos:
                        TextInterpretacion.insert(tk.END,"Se recibio un Done o un OK en los datos recibidos" + "\n")
        except Exception as e:
            messagebox.showerror(message=f"Error al enviar la instrucción al robot Scorbot: {e}")
    def leer_datos_continuamente(self):
        global TextInterpretacion

        while True:
            try:
                if self.serial_port and self.serial_port.isOpen():
                    datos = self.serial_port.read_all().decode()

                    if datos:
                        # Agregar datos al búfer de respuesta
                        self.response_buffer += datos

                        # Buscar "Done." y "OK" en el búfer de respuesta
                        if "Done." in self.response_buffer:
                            TextInterpretacion.insert(tk.END, "Se recibió un Done." + "\n")
                            TextRecibidos.insert(tk.END, "> " + self.response_buffer + "\n")
                            self.response_buffer = ""  # Limpiar el búfer
                        elif "ok" in self.response_buffer:
                            TextInterpretacion.insert(tk.END, "Se recibió un ok" + "\n")
                            TextRecibidos.insert(tk.END, self.response_buffer + "\n")
                            self.response_buffer = ""  # Limpiar el búfer
                        elif "OK" in self.response_buffer:
                            TextInterpretacion.insert(tk.END, "Se recibió un OK" + "\n")
                            TextRecibidos.insert(tk.END, self.response_buffer + "\n")
                            self.response_buffer = ""  # Limpiar el búfer
                        else:
                            # Usar after para actualizar la interfaz gráfica en el hilo principal
                            ventana.after(0, self.actualizar_interfaz)
            except Exception as e:
                print(f"Error al leer datos desde el puerto serie: {e}")
                break

    def actualizar_interfaz(self):
        global TextInterpretacion
        # Obtener el palette y la estación del buffer
        print(self.response_buffer)
        estacion = self.response_buffer[7:9]
        palette = self.response_buffer[11:13]
        TextInterpretacion.insert(tk.END, f"El palette {palette} se encuentra en la estación {estacion}" + "\n")
        self.response_buffer = ""
# Funciones de la interfaz gráfica
def conectar():
    port = comboBox1.get()
    scorbot_controller.conectar_robot(port)

def desconectar():
    scorbot_controller.desconectar_robot()

def enviar_instruccion():
    instruccion = TextEnviar.get("1.0", tk.END).strip()
    scorbot_controller.enviar_instruccion(instruccion)

# Crear la instancia del controlador Scorbot
scorbot_controller = ScorbotController()

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.geometry("900x700")
ventana.title("Controlador Scorbot")
ventana.resizable(0, 0)


# Botones y cajas de texto...
BotonConectar = tk.Button(ventana, text="Conectar", command=conectar)
BotonDesconectar = tk.Button(ventana, text="Desconectar", command=desconectar)
BotonEnviar = tk.Button(ventana, text="Enviar Instrucción", command=enviar_instruccion)

# Combobox y otros elementos...
comboBox1 = ttk.Combobox(ventana, state="readonly", values=["COM1", "COM2", "COM3", "COM4", "COM5"])
comboBox1.set("COM1")
TextEnviar = tk.Text(ventana, height=5, width=40)
TextRecibidos = tk.Text(ventana, height=15, width=40)
TextInterpretacion = tk.Text(ventana, height=15, width=40)

# Posicionamiento de elementos
BotonConectar.pack(pady=10)
BotonConectar.place(x=260, y = 30)
BotonDesconectar.pack(pady=5)
BotonDesconectar.place(x=250, y = 80)
comboBox1.pack(pady=5)
comboBox1.place(x=220, y=130)
TextEnviar.pack(pady=10)
TextEnviar.place(x = 130, y = 200)
BotonEnviar.place(x = 230, y = 300)
TextRecibidos.pack(pady=10)
TextRecibidos.place(x = 130, y = 380)
TextInterpretacion.pack(pady = 10)
TextInterpretacion.place(x = 500, y = 300)
etiquetaInterpretacion = tk.Label(ventana, text="Interpretación de instruccion enviada")
etiquetaInterpretacion.place(x=560, y=270)
etiquetaTextoRecibido = tk.Label(ventana, text="Mensaje Recibido del robot")
etiquetaTextoRecibido.place(x= 190, y = 350)
etiquetaTextoEnviado = tk.Label(ventana, text="Instrucción a enviar:")
etiquetaTextoEnviado.place(x=220, y = 170)


# Iniciar la aplicación
ventana.mainloop()
