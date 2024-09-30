# Importaciones
import customtkinter as ctk
import os
from PIL import Image, ImageTk
from datetime import datetime

# Configuraciones globales para la aplicación

# ---> Rutas
# Carpeta principal del proyecto
carpeta_principal = os.path.dirname(__file__)
# Carpeta de imágenes
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

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
        self.root.destroy()  # Cerrar ventana de login
        Escritorio()  # Abrir la ventana de escritorio

    def apagar(self):
        self.root.destroy()  # Cerrar la aplicación


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
            ("explorador.png", None),
            ("editor.png", None),
            ("calculator.png", None),
            ("configuraciones.png", None),
            ("tasks.png", None),
            ("calendar.png", None),
            ("musica.png", None),
        ]

        self.imagenes_tk = []  # Para almacenar las imágenes y evitar que el recolector de basura las elimine

        for nombre_imagen, accion in iconos:
            imagen = Image.open(os.path.join(carpeta_imagenes, nombre_imagen)).resize((40, 40))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.imagenes_tk.append(imagen_tk)

            # Crear un Label en lugar de un Button
            etiqueta = ctk.CTkLabel(self.frame_botones, image=imagen_tk, text='')
            etiqueta.pack(side="top", anchor="nw", padx=10, pady=10)  # Organizar los labels verticalmente desde la esquina superior izquierda
            
            # Asociar la acción a cada label con el evento de clic
            #etiqueta.bind("<Button-1>", lambda e, accion=accion: accion())


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
