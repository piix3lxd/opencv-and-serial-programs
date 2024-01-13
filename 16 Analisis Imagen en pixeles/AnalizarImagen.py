import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np

# Función para cargar una imagen desde un archivo
def cargar_imagen():
    global imagen
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")])
    if ruta_archivo:
        imagen = cv2.imread(ruta_archivo, cv2.IMREAD_GRAYSCALE)  # Cargar la imagen en escala de grises
        if imagen is not None:
            messagebox.showinfo("Éxito", "Imagen cargada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo cargar la imagen")

# Función para analizar la imagen
def analizar_imagen():
    global imagen
    if imagen is not None:
        # Realizar análisis de la matriz de intensidad
        umbral = int(numeroUmbra.get())  # Umbral de ejemplo (ajusta según tus necesidades)
        matriz_binaria = np.where(imagen > umbral, 1, 0)  # Umbralización
        recurrencia = np.count_nonzero(matriz_binaria) / (matriz_binaria.shape[0] * matriz_binaria.shape[1])
        mensaje = f"Recurrencia de intensidad (umbral {umbral}): {recurrencia * 100:.2f}%\n"
        mensaje += f"Celdas con valor 1 (Blanco): {np.count_nonzero(matriz_binaria)}\n"

        mensaje += f"Celdas con valor 0 (Negro): {matriz_binaria.size - np.count_nonzero(matriz_binaria)}"

        # Mostrar el resultado en un cuadro de texto
        resultado_text.config(state=tk.NORMAL)
        resultado_text.delete(1.0, tk.END)  # Borrar contenido anterior
        resultado_text.insert(tk.END, mensaje)
        resultado_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Primero carga una imagen")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Imágenes")
ventana.geometry("500x300")
ventana.resizable(0,0)

# Variables globales
imagen = None

# Botones
btn_cargar_imagen = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
btn_analizar = tk.Button(ventana, text="Analizar Imagen", command=analizar_imagen)

# Cuadro de texto para mostrar el resultado
resultado_text = tk.Text(ventana, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)

explicacion = tk.Label(ventana, text="Este programa carga la imagen como una matriz y analiza celda a celda")
explicacion.place(x=60,y=230)
# Colocar widgets en la ventana
btn_cargar_imagen.pack()
btn_analizar.pack()
resultado_text.pack()

#SpinBox
numeroUmbra = tk.Spinbox(ventana, from_=0,to=255)
numeroUmbra.place(x=150, y=20, width=42, height=22)
LabelUmbral = tk.Label(ventana, text="Umbral: ")
LabelUmbral.place(x=100, y = 20)
# Iniciar la aplicación
ventana.mainloop()

