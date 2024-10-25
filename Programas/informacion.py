import psutil
import tkinter as tk
from tkinter import font

def obtener_informacion_sistema():
    informacion = {
        "cpu": {
            "Número de núcleos físicos": psutil.cpu_count(logical=False),
            "Número de núcleos lógicos": psutil.cpu_count(logical=True),
            "Uso de la CPU (%)": psutil.cpu_percent(interval=1),
        },
        "memoria": {
            "Memoria total (GB)": round(psutil.virtual_memory().total / (1024**3), 2),
            "Memoria disponible (GB)": round(psutil.virtual_memory().available / (1024**3), 2),
            "Porcentaje de memoria en uso (%)": psutil.virtual_memory().percent,
        },
        "disco": []
    }
    
    # Obtener información de las particiones del disco
    particiones = psutil.disk_partitions()
    for particion in particiones:
        particion_info = {
            "Dispositivo": particion.device,
            "Punto de montaje": particion.mountpoint,
            "Tipo de sistema de archivos": particion.fstype,
            "Uso de disco (%)": psutil.disk_usage(particion.mountpoint).percent
        }
        informacion["disco"].append(particion_info)
    
    return informacion

def actualizar_informacion():
    informacion = obtener_informacion_sistema()
    
    # Actualizar información de la CPU
    cpu_info = informacion["cpu"]
    for idx, key in enumerate(cpu_info):
        etiquetas_cpu[idx].config(text=f"{key}: {cpu_info[key]}")
    
    # Actualizar información de la memoria
    memoria_info = informacion["memoria"]
    for idx, key in enumerate(memoria_info):
        etiquetas_memoria[idx].config(text=f"{key}: {memoria_info[key]}")
    
    # Actualizar información del disco
    particiones_actuales = informacion["disco"]

    # Ajustar el número de frames según las particiones actuales
    while len(frames_disco) < len(particiones_actuales):
        crear_frame_particion()
    while len(frames_disco) > len(particiones_actuales):
        frames_disco.pop().destroy()
    
    # Actualizar el contenido de cada frame de partición
    for idx, particion_info in enumerate(particiones_actuales):
        etiquetas = frames_disco[idx]
        for key, label in etiquetas.items():
            label.config(text=f"{key}: {particion_info[key]}")
    
    # Reprograma la actualización cada 1000 ms (1 segundo)
    ventana.after(1000, actualizar_informacion)

def crear_frame_particion():
    frame = tk.Frame(frame_disco, bg="white", bd=1, relief="solid")
    frame.pack(fill="x", padx=5, pady=2)
    
    etiquetas = {
        "Dispositivo": tk.Label(frame, anchor="w", font=fuente),
        "Punto de montaje": tk.Label(frame, anchor="w", font=fuente),
        "Tipo de sistema de archivos": tk.Label(frame, anchor="w", font=fuente),
        "Uso de disco (%)": tk.Label(frame, anchor="w", font=fuente),
    }
    
    for key, etiqueta in etiquetas.items():
        etiqueta.pack(fill="x", padx=5, pady=1)
    
    frames_disco.append(etiquetas)

def mostrar_interfaz():
    global ventana, etiquetas_cpu, etiquetas_memoria, frame_disco, frames_disco, fuente
    
    ventana = tk.Tk()
    ventana.title("Información del Sistema")
    ventana.configure(bg="white")
    
    fuente = font.Font(family="Courier", size=10)
    
    # Sección de información de la CPU
    frame_cpu = tk.Frame(ventana, bg="white", bd=2, relief="solid")
    frame_cpu.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_cpu, text="Información de la CPU", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=2)
    
    etiquetas_cpu = [
        tk.Label(frame_cpu, text="", anchor="w", font=fuente) for _ in range(3)
    ]
    for etiqueta in etiquetas_cpu:
        etiqueta.pack(fill="x", padx=5, pady=1)
    
    # Sección de información de la memoria
    frame_memoria = tk.Frame(ventana, bg="white", bd=2, relief="solid")
    frame_memoria.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_memoria, text="Información de la Memoria", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=2)
    
    etiquetas_memoria = [
        tk.Label(frame_memoria, text="", anchor="w", font=fuente) for _ in range(3)
    ]
    for etiqueta in etiquetas_memoria:
        etiqueta.pack(fill="x", padx=5, pady=1)
    
    # Sección de información del disco
    frame_disco = tk.Frame(ventana, bg="white", bd=2, relief="solid")
    frame_disco.pack(fill="x", padx=10, pady=5)
    tk.Label(frame_disco, text="Información del Disco", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=2)
    
    frames_disco = []
    
    # Iniciar la actualización periódica
    actualizar_informacion()
    
    ventana.mainloop()

mostrar_interfaz()
