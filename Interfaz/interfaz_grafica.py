import customtkinter as ctk
import os
from PIL import Image

# Carpeta de imágenes
carpeta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

# Configuración de la apariencia de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme('blue')

class Login(ctk.CTk):
    
    def __init__(self):
        # Creación de la ventana principal
        self.root = ctk.CTk()  # Instancia
        self.root.title("Hermes OS")  # Título
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))  # Icono
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Configurar la geometría de la ventana
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        self.root.resizable(False, False)  # Bloqueo de redimensión de ventana

        # Contenido de la ventana principal
        # Carga de la imagen
        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            size=(540, 420)  # Tamaño de las imágenes
        )

        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.pack(pady=15)

        # Campos de texto
        # Usuario
        ctk.CTkLabel(self.root, text="Usuario").pack(pady=(10, 0))
        self.usuario = ctk.CTkEntry(self.root, width=300, height=40)  
        self.usuario.insert(0, "Nombre de usuario")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack(pady=(0, 10))  # Añadir espacio

        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack(pady=(10, 0))
        self.contrasena = ctk.CTkEntry(self.root, show="*", width=300, height=40)  
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack(pady=(0, 20))  # Añadir espacio

        # Botón de envío
        self.boton_ingresar = ctk.CTkButton(self.root, text="Ingresar", width=150, height=40, fg_color="blue", hover_color="darkblue")
        self.boton_ingresar.pack(pady=10)

        # Bucle de ejecución
        self.root.mainloop() 

Login()
