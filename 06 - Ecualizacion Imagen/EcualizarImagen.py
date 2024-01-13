import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ventana
ventana = tk.Tk()
ventana.geometry("1050x800")
ventana.title("Ecualizacion")

def ecualizar_imagen():
    try:
        path_image = filedialog.askopenfilename(filetypes=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")
        ])
        if len(path_image) > 0:
            # Lee la imagen
            imagenFile = cv2.imread(path_image)
            imagenFile = cv2.cvtColor(imagenFile, cv2.COLOR_BGR2RGB)
            imagenFile = cv2.resize(imagenFile, (360, 360))
            
            # Visualiza la imagen original en la ventana
            imOriginal = Image.fromarray(imagenFile)
            imgOriginal = ImageTk.PhotoImage(image=imOriginal)
            lblInputImagen1.configure(image=imgOriginal)
            lblInputImagen1.image = imgOriginal

            
            # Muestra el histograma de la imagen original
            fig_original, ax_original = plt.subplots()
            ax_original.hist(imagenFile.ravel(), 256, [0, 255], color='blue')
            ax_original.set_title('Histograma original')
            canvasOriginal = FigureCanvasTkAgg(fig_original, master=ventana)
            canvasOriginal.draw()
            canvasOriginal.get_tk_widget().place(x=60, y=480, width=500, height=300)

            # Ecualiza la imagen
            gray = cv2.cvtColor(imagenFile, cv2.COLOR_RGB2GRAY)
            equ = cv2.equalizeHist(gray)
            
            # Visualiza la imagen ecualizada en la ventana
            imEcualizada = Image.fromarray(cv2.cvtColor(equ, cv2.COLOR_GRAY2RGB))
            imgEcualizada = ImageTk.PhotoImage(image=imEcualizada)
            lblInputImagen2.configure(image=imgEcualizada)
            lblInputImagen2.image = imgEcualizada

            # Muestra el histograma de la imagen ecualizada
            fig_ecualizada, ax_ecualizada = plt.subplots()
            ax_ecualizada.hist(equ.ravel(), 255, [0, 255], color='red')
            ax_ecualizada.set_title('Histograma ecualizado')
            canvasEcualizado = FigureCanvasTkAgg(fig_ecualizada, master=ventana)
            canvasEcualizado.draw()
            canvasEcualizado.get_tk_widget().place(x=580, y=480, width=500, height=300)

    except Exception as e:
        messagebox.showerror(message=f"Error: {str(e)}")

def boton_salir():
    ventana.destroy()

# Cuadros de las Imagenes
lblInputImagen1 = tk.Label(ventana)
lblInputImagen1.place(x=60, y=100, width=360, height=360)
lblInputImagen1.configure(bg='gray')

lblInputImagen2 = tk.Label(ventana)
lblInputImagen2.place(x=580, y=100, width=360, height=360)
lblInputImagen2.configure(bg="gray")
# Crear una etiqueta de texto con fuente más grande y negrita
etiqueta_texto = tk.Label(ventana, text="Imagen original", font=("Arial", 14, "bold"))
etiqueta_texto.place(x=160, y=70)

# Crear otra etiqueta de texto con fuente más grande y negrita
etiqueta_texto2 = tk.Label(ventana, text="Imagen ecualizada", font=("Arial", 14, "bold"))
etiqueta_texto2.place(x=670, y=70)

# Botones
CImagen = tk.Button(ventana, text="Cargar Imagen", command=ecualizar_imagen)
CImagen.place(x=0, y=0, width=160, height=50)
salir = tk.Button(ventana, text="Salir", command=boton_salir)
salir.place(x=170, y=0, width=110, height=50)

ventana.mainloop()
