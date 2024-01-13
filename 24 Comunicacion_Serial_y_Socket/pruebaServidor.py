import socket
import sys
import threading
import tkinter as tk

HOST = ''  # Significa que escucha en todas las interfaces de red
PORT = 8888  # Puerto para escuchar
MAX_CONNECTIONS = 8  # Número máximo de conexiones simultáneas

class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title('Servidor')

        self.status_label = tk.Label(master, text='Servidor detenido')
        self.status_label.pack()

        self.log_text = tk.Text(master, height=10, width=50)
        self.log_text.pack()

        self.start_button = tk.Button(master, text='Iniciar', command=self.start_server)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text='Detener', command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack()

        self.message_text = tk.Text(master, height=3, width=50)
        self.message_text.pack()

        self.send_button = tk.Button(master, text='Enviar', command=self.send_message, state=tk.DISABLED)
        self.send_button.pack()

    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.message_text.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

        self.status_label.config(text='Servidor corriendo')

    def stop_server(self):
        self.server_socket.close()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.message_text.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        self.status_label.config(text='Servidor detenido')

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    def handle_connection(self, conn, addr, name):
        self.log(f'{name} conectado por {addr}')

        while True:
            # Recibir los datos enviados por el cliente
            data = conn.recv(1024)
            message = data.decode().strip()

            if not message:
                # El cliente ha terminado de enviar mensajes
                break

            self.log(f'Datos recibidos de {name}: {message}')

            # Procesar el mensaje del cliente
            response = f'Recibido: {message}'.encode()

            # Enviar una respuesta al cliente
            conn.sendall(response)

        # Cerrar la conexión
        conn.close()
        self.log(f'Conexión cerrada con {name}')

    def send_message(self):
        message = self.message_text.get(1.0, tk.END).strip()
        self.message_text.delete(1.0, tk.END)
        self.log(f'Mensaje enviado a los clientes: {message}')
        for conn in self.connections:
            conn.sendall(message.encode())

    def run_server(self):
        # Crear un objeto de socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular el socket a una dirección y puerto específicos
        self.server_socket.bind((HOST, PORT))
        self.log(f'Servidor corriendo en el puerto {PORT}')

        # Escuchar en el socket para conexiones entrantes
        self.server_socket.listen(MAX_CONNECTIONS)

        self.connections = []
        self.names = []

        # Ciclo infinito para manejar conexiones entrantes
        while True:
            # Aceptar una conexión entrante
            conn, addr = self.server_socket.accept()
            self.connections.append(conn)

            # Recibir el nombre del cliente
            data = conn.recv(1024)
            name = data.decode().strip()
            self.names.append(name)

            # Crear un hilo para manejar la conexión entrante
            t = threading.Thread(target=self.handle_connection, args=(conn, addr, name))
            t.start()

root = tk.Tk()
server_gui = ServerGUI(root)
root.mainloop()