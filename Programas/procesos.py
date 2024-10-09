import psutil
import tkinter as tk

def obtener_informacion_sistema():
    informacion = ""
    
    # Obtener información de la CPU
    informacion += "Información de la CPU:\n"
    informacion += f"  - Número de núcleos físicos: {psutil.cpu_count(logical=False)}\n"
    informacion += f"  - Número de núcleos lógicos: {psutil.cpu_count(logical=True)}\n"
    informacion += f"  - Uso de la CPU (%): {psutil.cpu_percent(interval=1)}\n"
    
    # Obtener información de la memoria
    informacion += "\nInformación de la memoria:\n"
    memoria = psutil.virtual_memory()
    informacion += f"  - Memoria total (GB): {round(memoria.total / (1024**3), 2)}\n"
    informacion += f"  - Memoria disponible (GB): {round(memoria.available / (1024**3), 2)}\n"
    informacion += f"  - Porcentaje de memoria en uso (%): {memoria.percent}\n"
    
    # Obtener información del disco
    informacion += "\nInformación del disco:\n"
    particiones = psutil.disk_partitions()
    for particion in particiones:
        informacion += f"  - Dispositivo: {particion.device}\n"
        informacion += f"    - Punto de montaje: {particion.mountpoint}\n"
        informacion += f"    - Tipo de sistema de archivos: {particion.fstype}\n"
        informacion += f"    - Uso de disco (%): {psutil.disk_usage(particion.mountpoint).percent}\n"
    
    return informacion

def mostrar_interfaz():
    ventana = tk.Tk()
    ventana.title("Información del Sistema")
    
    etiqueta = tk.Label(ventana, text=obtener_informacion_sistema(), justify=tk.LEFT)
    etiqueta.pack(padx=10, pady=10)
    
    ventana.mainloop()

mostrar_interfaz()

