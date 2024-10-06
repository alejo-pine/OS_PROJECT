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
            light_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            size=(500, 300)
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
        for usuario in datos_usuarios["usuarios"]:
            if usuario["usuario"] == usuario_ingresado and usuario["contrasena"] == contrasena_codificada:
                usuario_valido = True
                break

        if usuario_valido:
            self.root.destroy()  # Cerrar ventana de login
            Escritorio()  # Abrir la ventana de escritorio
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

            # Agregar el nuevo usuario al archivo JSON
            nuevo_usuario = {"usuario": usuario, "contrasena": contrasena_codificada}
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
    
    def __init__(self):
        pass

    def calculadora(self):
        ruta = os.path.join(carpeta_programas, "calculadora.py")
        subprocess.Popen(["python", ruta])

    def editor_texto(self):
        ruta = os.path.join(carpeta_programas, "editor.py")
        subprocess.Popen(["python", ruta])

    def explorador_archivos(self):
        ruta = os.path.join(carpeta_programas, "explorador.py")
        subprocess.Popen(["python", ruta])
        
    def reproductor_musica(self):
        ruta = os.path.join(carpeta_programas, "reproductor.py")
        subprocess.Popen(["python", ruta])

    # Agrega más funciones para otros programas


   
# Clase para la ventana de escritorio
class Escritorio:
    def __init__(self):
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
        
        #Crear las funciones de llamado a las aplicaciones
        self.aplicaciones = Aplicaciones()

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
            ("editor.png", self.aplicaciones.editor_texto),
            ("calculator.png", self.aplicaciones.calculadora),
            ("configuraciones.png", None),
            ("tasks.png", None),
            ("calendar.png", None),
            ("musica.png", self.aplicaciones.reproductor_musica),
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
