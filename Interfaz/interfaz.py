# Importaciones
import customtkinter as ctk
import os
from PIL import Image, ImageTk
from datetime import datetime
import json
import hashlib
import subprocess #Para manejar procesos


# Configuraciones globales para la aplicación

# ---> Rutas
# Carpeta principal del proyecto
carpeta_principal = os.path.dirname(__file__)
# Carpeta de imágenes
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")
carpeta_programas = os.path.join(carpeta_principal, "../Programas")
BASE_PATH = "C:/HermesOS/Usuarios"

#Función para codificar la contraseña
def codificar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

# Modo de color y tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Login:
    def __init__(self):
        # Creación de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Hermes OS")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))

        # Obtener tamaño de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Configurar la geometría de la ventana
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state('zoomed')  # Maximizar la ventana
        self.root.resizable(True, True)
        self.root.configure(bg="darkgray")

        # Cargar la imagen del logo
        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "usuario.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "usuario.png")),
            size=(250, 250)
        )

        # Etiqueta para mostrar el logo
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.pack(pady=15)

        # Campos de texto
        self.crear_campos_texto()

        # Botón de envío
        self.boton_ingresar = ctk.CTkButton(self.root, text="Ingresar", width=150, height=40, fg_color="blue",
                                            hover_color="darkblue", command=self.validar)
        self.boton_ingresar.pack(pady=10)
        
        # Botón para crear usuario
        self.boton_crear_usuario = ctk.CTkButton(self.root, text="Crear Usuario", width=150, height=40, fg_color="green",
                                                hover_color="darkgreen", command=self.abrir_ventana_crear_usuario)
        self.boton_crear_usuario.pack(pady=10)

        # Botón de apagar
        self.crear_boton_apagar()

        # Bucle de ejecución
        self.root.mainloop()

    def crear_campos_texto(self):
        # Usuario
        ctk.CTkLabel(self.root, text="Usuario").pack(pady=(10, 0))
        self.usuario = ctk.CTkEntry(self.root, width=300, height=40)
        self.usuario.insert(0, "Nombre de usuario")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack(pady=(0, 10))

        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack(pady=(10, 0))
        self.contrasena = ctk.CTkEntry(self.root, show="*", width=300, height=40)
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack(pady=(0, 20))

    def crear_boton_apagar(self):
        icono_apagar = ctk.CTkImage(Image.open(os.path.join(carpeta_imagenes, "power.png")), size=(40, 40))
        etiqueta_apagar = ctk.CTkLabel(self.root, image=icono_apagar, text="")
        etiqueta_apagar.place(relx=0.98, rely=0.95, anchor='se')
        etiqueta_apagar.bind("<Button-1>", lambda e: self.apagar())
        
        
    def validar(self):
        # Obtener los valores ingresados por el usuario
        usuario_ingresado = self.usuario.get()
        contrasena_ingresada = self.contrasena.get()

        # Codificar la contraseña ingresada
        contrasena_codificada = codificar_contrasena(contrasena_ingresada)

        # Cargar el archivo JSON con las credenciales
        with open(os.path.join(carpeta_principal, 'usuarios.json'), 'r') as archivo:
            datos_usuarios = json.load(archivo)

        # Verificar si el usuario y la contraseña coinciden
        usuario_valido = False
        ruta_usuario = None
        
        for usuario in datos_usuarios["usuarios"]:
            if usuario["usuario"] == usuario_ingresado and usuario["contrasena"] == contrasena_codificada:
                usuario_valido = True
                ruta_usuario = usuario["ruta"]  # Obtener la ruta directamente del JSON
                break

        if usuario_valido:
            self.root.destroy()  # Cerrar ventana de login
            Escritorio(ruta_usuario)  # Abrir la ventana de escritorio
        else:
            # Mostrar un mensaje de error si las credenciales son incorrectas
            error_label = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos", fg_color="red")
            error_label.pack(pady=10)

    def abrir_ventana_crear_usuario(self):
        # Crear una nueva ventana para registrar usuarios
        self.ventana_crear_usuario = ctk.CTkToplevel(self.root)
        self.ventana_crear_usuario.title("Crear Usuario")
        self.ventana_crear_usuario.geometry("400x400")

        # Etiqueta para el usuario
        ctk.CTkLabel(self.ventana_crear_usuario, text="Nuevo Usuario").pack(pady=(10, 0))
        self.nuevo_usuario = ctk.CTkEntry(self.ventana_crear_usuario, width=300, height=40)
        self.nuevo_usuario.pack(pady=(0, 10))

        # Contraseña
        ctk.CTkLabel(self.ventana_crear_usuario, text="Contraseña").pack(pady=(10, 0))
        self.nueva_contrasena = ctk.CTkEntry(self.ventana_crear_usuario, show="*", width=300, height=40)
        self.nueva_contrasena.pack(pady=(0, 10))

        # Confirmar contraseña
        ctk.CTkLabel(self.ventana_crear_usuario, text="Confirmar Contraseña").pack(pady=(10, 0))
        self.confirmar_contrasena = ctk.CTkEntry(self.ventana_crear_usuario, show="*", width=300, height=40)
        self.confirmar_contrasena.pack(pady=(0, 20))

        # Botón para guardar el nuevo usuario
        self.boton_guardar_usuario = ctk.CTkButton(self.ventana_crear_usuario, text="Guardar", width=150, height=40,
                                                fg_color="blue", hover_color="darkblue",
                                                command=self.guardar_nuevo_usuario)
        self.boton_guardar_usuario.pack(pady=10)
        
    def crear_estructura_usuario(self, username):
        # Ruta específica para el usuario
        user_path = os.path.join(BASE_PATH, username)
        os.makedirs(user_path, exist_ok=True)
        
        # Crea carpetas de Documentos, Música, Imágenes y Videos
        subcarpetas = ["Documentos", "Musica", "Imagenes", "Videos"]
        for carpeta in subcarpetas:
            os.makedirs(os.path.join(user_path, carpeta), exist_ok=True)
        
        return os.path.normpath(user_path)  # Devolvemos la ruta del usuario para almacenarla en el archivo JSON
        
    def guardar_nuevo_usuario(self):
        # Obtener los datos ingresados
        usuario = self.nuevo_usuario.get()
        contrasena = self.nueva_contrasena.get()
        confirmar_contrasena = self.confirmar_contrasena.get()

        # Validar que las contraseñas coincidan
        if contrasena != confirmar_contrasena:
            error_label = ctk.CTkLabel(self.ventana_crear_usuario, text="Las contraseñas no coinciden", fg_color="red")
            error_label.pack(pady=10)
            return

        # Codificar la contraseña
        contrasena_codificada = codificar_contrasena(contrasena)

        # Cargar los usuarios existentes del archivo JSON
        with open(os.path.join(carpeta_principal, 'usuarios.json'), 'r+') as archivo:
            datos_usuarios = json.load(archivo)

            # Verificar que el usuario no exista ya
            for usuario_existente in datos_usuarios["usuarios"]:
                if usuario_existente["usuario"] == usuario:
                    error_label = ctk.CTkLabel(self.ventana_crear_usuario, text="El usuario ya existe", fg_color="red")
                    error_label.pack(pady=10)
                    return
                
            # Crea la estructura de carpetas para el nuevo usuario y obtener su ruta
            ruta_usuario = self.crear_estructura_usuario(usuario)

            # Agregar el nuevo usuario al archivo JSON
            nuevo_usuario = {
                "usuario": usuario,
                "contrasena": contrasena_codificada,
                "ruta": ruta_usuario  # Agregar la ruta de la carpeta del usuario
            }
            datos_usuarios["usuarios"].append(nuevo_usuario)

            # Guardar los cambios en el archivo
            archivo.seek(0)
            json.dump(datos_usuarios, archivo, indent=4)
            archivo.truncate()

        # Mostrar un mensaje de éxito
        exito_label = ctk.CTkLabel(self.ventana_crear_usuario, text="Usuario creado con éxito", fg_color="green")
        exito_label.pack(pady=10)

        # Cerrar la ventana de creación de usuarios
        self.ventana_crear_usuario.after(2000, self.ventana_crear_usuario.destroy)

    def apagar(self):
        self.root.destroy()  # Cerrar la aplicación

#Clase para agregar todas las aplicaciones

class Aplicaciones:
    
    def __init__(self, ruta_usuario):
        self.running_apps = []
        self.ruta_usuario = ruta_usuario

    def calculadora(self):
        ruta = os.path.join(carpeta_programas, "calculadora.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Calculadora', 'process': proceso})

    def editor_texto(self):
        ruta = os.path.join(carpeta_programas, "editor.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Editor', 'process': proceso})
        
    def explorador_archivos(self):
        ruta = os.path.join(carpeta_programas, "explorador.py")
        proceso = subprocess.Popen(["python", ruta, self.ruta_usuario])
        self.running_apps.append({'name': 'Explorador', 'process': proceso})
            
    def reproductor_musica(self):
        ruta = os.path.join(carpeta_programas, "reproductor.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Reproductor', 'process': proceso})
        
    def navegador(self):
        ruta = os.path.join(carpeta_programas, "navegador.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Navegador', 'process': proceso})
             
    def calendario(self):
        ruta = os.path.join(carpeta_programas, "calendario.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Calendario', 'process': proceso})
        
    def informacion(self):
        ruta = os.path.join(carpeta_programas, "informacion.py")
        proceso = subprocess.Popen(["python", ruta])
        self.running_apps.append({'name': 'Info', 'process': proceso})
        
    def admin_tareas(self):
        AdministradorTareas(self.running_apps)
        
    def getRunning_apps(self):
        return self.running_apps

#Administrador de tareas
class AdministradorTareas:
    def __init__(self, running_apps):
        self.running_apps = running_apps
        self.root = ctk.CTk()
        self.root.title("Administrador de Tareas")
        self.root.geometry("400x200")

        # Diccionario para mantener referencias a los widgets
        self.app_widgets = {}

        self.table = ctk.CTkScrollableFrame(self.root)
        self.table.pack(pady=10, padx=10, fill="both", expand=True)

        self.update_table()  # Llama a la primera actualización
        self.root.mainloop()

    def update_table(self):
        self.remove_closed_processes()

        # Iterar sobre las aplicaciones en ejecución
        for app in self.running_apps:
            if app['name'] not in self.app_widgets:
                # Si la aplicación no está en los widgets, agregarla
                frame = ctk.CTkFrame(self.table)
                frame.pack(pady=5)

                nombre_label = ctk.CTkLabel(frame, text=app['name'])
                nombre_label.pack(side="left")

                estado_label = ctk.CTkLabel(frame, text="En ejecución")
                estado_label.pack(side="left", padx=10)

                btn_terminar = ctk.CTkButton(frame, text="Terminar", command=lambda p=app: self.terminar_proceso(p))
                btn_terminar.pack(side="right")

                # Guardar referencias a los widgets en el diccionario
                self.app_widgets[app['name']] = {
                    'frame': frame,
                    'estado_label': estado_label
                }
            else:
                # Si la aplicación ya está en los widgets, solo actualizar el estado si es necesario
                estado_label = self.app_widgets[app['name']]['estado_label']
                estado_label.configure(text="En ejecución")

        # Eliminar widgets de aplicaciones que ya no están en ejecución
        self.cleanup_widgets()

        # Configurar la siguiente actualización en 1000 ms (1 segundo)
        self.root.after(1000, self.update_table)

    def terminar_proceso(self, app):
        app['process'].terminate()  # Terminar el proceso
        self.running_apps.remove(app)  # Eliminar de la lista
        self.update_table()  # Actualizar la tabla inmediatamente después de terminar un proceso

    def remove_closed_processes(self):
        # Elimina los procesos que hayan terminado de la lista
        self.running_apps = [app for app in self.running_apps if app['process'].poll() is None]

    def cleanup_widgets(self):
        # Limpiar widgets de procesos que ya no están en ejecución
        active_apps = {app['name'] for app in self.running_apps}
        for app_name in list(self.app_widgets.keys()):
            if app_name not in active_apps:
                # Eliminar el widget y borrar la referencia
                self.app_widgets[app_name]['frame'].destroy()
                del self.app_widgets[app_name]

   
# Clase para la ventana de escritorio
class Escritorio():
    def __init__(self, ruta_usuario):
        self.root = ctk.CTk()
        self.root.title("Escritorio")

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Cargar la imagen de fondo
        imagen_fondo = Image.open(os.path.join(carpeta_imagenes, "escritorio.webp"))
        imagen_fondo = imagen_fondo.resize((ancho_pantalla, alto_pantalla), Image.LANCZOS)
        self.fondo = ImageTk.PhotoImage(imagen_fondo)

        # Configurar la geometría
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state('zoomed')  # Maximizar la ventana
        self.root.resizable(True, True)
        fondo_label = ctk.CTkLabel(self.root, image=self.fondo, text="")
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.ruta_usuario = ruta_usuario
        #Crear las funciones de llamado a las aplicaciones
        self.aplicaciones = Aplicaciones(self.ruta_usuario)

        # Crear frame para los botones
        self.crear_botones()

        # Crear el reloj
        self.crear_reloj()

        # Bucle principal
        self.root.mainloop()

    def crear_botones(self):
        
        self.frame_botones = ctk.CTkFrame(self.root, corner_radius=1)
        self.frame_botones.pack(side="top", anchor="nw")

        # Lista de imágenes para los labels
        iconos = [
            ("explorador.png", self.aplicaciones.explorador_archivos),
            ("navegador.png", self.aplicaciones.navegador),
            ("text.png", self.aplicaciones.editor_texto),
            ("calculator.png", self.aplicaciones.calculadora),
            ("tasks.png", self.aplicaciones.admin_tareas),
            ("calendar.png", self.aplicaciones.calendario),
            ("musica.png", self.aplicaciones.reproductor_musica),
            ("informacion.png", self.aplicaciones.informacion),
            ("configuraciones.png", None),
        ]

        self.imagenes_tk = []  # Para almacenar las imágenes y evitar que el recolector de basura las elimine

        for nombre_imagen, accion in iconos:
            imagen = Image.open(os.path.join(carpeta_imagenes, nombre_imagen)).resize((40, 40))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagenes_tk.append(imagen_tk)

            etiqueta = ctk.CTkLabel(self.frame_botones, image=imagen_tk, text='')
            etiqueta.pack(side="top", anchor="nw", padx=10, pady=10)  # Organizar los labels verticalmente desde la esquina superior izquierda
            
            # Asociar la acción a cada label con el evento de clic
            etiqueta.bind("<Button-1>", lambda e, accion=accion: accion())
            

    def crear_reloj(self):
        self.frame_reloj = ctk.CTkFrame(self.root, width=150, height=85, bg_color="black")
        self.frame_reloj.pack(side="bottom", anchor="sw", padx=10, pady=10)

        # Label para mostrar la hora y fecha
        self.label_hora = ctk.CTkLabel(self.frame_reloj, font=("Whisper", 20))
        self.label_hora.pack()

        self.actualizar_hora()

    def actualizar_hora(self):
        # Obtener la hora y la fecha actual
        hora_actual = datetime.now().strftime("%H:%M:%S")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato de la fecha

        # Unificar la fecha y la hora en un solo string
        fecha_hora = f"{fecha_actual}\n{hora_actual}"
        
        # Actualizar el Label con la fecha y la hora
        self.label_hora.configure(text=fecha_hora)
        
        # Llamar a esta función nuevamente después de 1000 ms (1 segundo)
        self.root.after(1000, self.actualizar_hora)



Login()
