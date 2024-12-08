import tkinter as tk
from tkinter import messagebox
import threading
import time
from plyer import notification
from tkinter import ttk
import customtkinter as ctk

# Variables globales
ejecutando = False
tiempo_restante = 25 * 60  # 25 minutos en segundos
tiempo_inicial = 25  # Tiempo inicial en minutos

# Funciones principales
def iniciar_temporizador():
    global ejecutando, tiempo_restante, tiempo_inicial
    if not ejecutando:
        try:
            tiempo_inicial = int(entrada_tiempo.get())
            if tiempo_inicial <= 0:
                messagebox.showerror("Error", "Por favor ingrese un número positivo de minutos")
                return
            ejecutando = True
            estado_label.configure(text="Estado: Activo", text_color="green")
            tiempo_restante = tiempo_inicial * 60  # Convertir minutos a segundos
            threading.Thread(target=temporizador).start()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido de minutos")

def detener_temporizador():
    global ejecutando
    ejecutando = False
    estado_label.configure(text="Estado: Inactivo", text_color="red")

def temporizador():
    global tiempo_restante, ejecutando
    while ejecutando and tiempo_restante > 0:
        minutos, segundos = divmod(tiempo_restante, 60)
        contador_label.configure(text=f"Tiempo restante: {minutos:02}:{segundos:02}")
        time.sleep(1)  # Esperar un segundo
        tiempo_restante -= 1
    if tiempo_restante == 0 and ejecutando:
        mostrar_notificacion()

def mostrar_notificacion():
    detener_temporizador()  # Detener después de una notificación
    notification.notify(
        title="¡Hora de levantarte!",
        message="Es importante moverte para cuidar tu salud.",
        timeout=10  # La notificación desaparecerá en 10 segundos
    )
    messagebox.showinfo("¡Hora de levantarte!", "Es importante moverte para cuidar tu salud.")

# Configuración del tema
ctk.set_appearance_mode("dark")  # Modos: dark, light
ctk.set_default_color_theme("blue")  # Temas: blue, dark-blue, green

# Crear la interfaz gráfica
ventana = ctk.CTk()
ventana.title("Recordatorio de Pausas")
ventana.geometry("500x400")


# Frame principal
frame_principal = ctk.CTkFrame(ventana)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

# Título
titulo = ctk.CTkLabel(frame_principal, text="Temporizador de Pausas Activas", 
                      font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=20)

# Frame para entrada de tiempo
frame_entrada = ctk.CTkFrame(frame_principal)
frame_entrada.pack(pady=10)

# Etiqueta y entrada para el tiempo
tiempo_label = ctk.CTkLabel(frame_entrada, text="Minutos para la pausa:", 
                           font=ctk.CTkFont(size=16))
tiempo_label.pack(side="left", padx=5)

entrada_tiempo = ctk.CTkEntry(frame_entrada, width=60, 
                            font=ctk.CTkFont(size=16))
entrada_tiempo.insert(0, "25")  # Valor predeterminado
entrada_tiempo.pack(side="left", padx=5)

# Etiqueta del estado
estado_label = ctk.CTkLabel(frame_principal, text="Estado: Inactivo", 
                           font=ctk.CTkFont(size=18), text_color="red")
estado_label.pack(pady=15)

# Etiqueta del contador
contador_label = ctk.CTkLabel(frame_principal, text="Tiempo restante: 25:00", 
                             font=ctk.CTkFont(size=36))
contador_label.pack(pady=20)

# Frame para botones
frame_botones = ctk.CTkFrame(frame_principal)
frame_botones.pack(pady=20)

# Botones de control
boton_iniciar = ctk.CTkButton(frame_botones, text="Iniciar Temporizador", 
                             font=ctk.CTkFont(size=16),
                             command=iniciar_temporizador,
                             width=200,
                             height=40)
boton_iniciar.pack(pady=10)

boton_detener = ctk.CTkButton(frame_botones, text="Detener Temporizador", 
                             font=ctk.CTkFont(size=16),
                             command=detener_temporizador,
                             width=200,
                             height=40)
boton_detener.pack(pady=10)

# Iniciar la aplicación
ventana.mainloop()
