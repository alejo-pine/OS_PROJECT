#Importaciones
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
ctk.set_appearance_mode("Sytem")
ctk.set_default_color_theme("blue")

class Login:
    def __init__(self):
        # Creación de la ventana principal
        self.root = ctk.CTk() # Instancia
        self.root.title("Hermes OS") # Título
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico")) # Icono
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

    # Configurar la geometría de la ventana para que ocupe toda la pantalla
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")  # Tamaño inicial de la ventana
        self.root.state('zoomed')  # Maximiza la ventana
        self.root.resizable(True, True)  # Permitir redimensión de ventana
        # Establecer el fondo de la ventana
        self.root.configure(bg="darkgray")
        
        # Contenido de la ventana principal
        # Carga de la imagen
        logo = ctk.CTkImage(
            light_image=Image.open((os.path.join(carpeta_imagenes, "Login.png"))), # Imagen modo claro
            dark_image=Image.open((os.path.join(carpeta_imagenes, "Login.png"))), # Imagen modo oscuro
            size=(500, 300)) # Tamaño de las imágenes
        
        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master=self.root,
                               image=logo,
                               text="")
    
        etiqueta.pack(pady=15)
        
 # Campos de texto
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
        
        # Botón de envío        
        self.boton_ingresar = ctk.CTkButton(self.root, text="Ingresar", width=150, height=40, fg_color="blue", hover_color="darkblue",  command=self.validar)
        self.boton_ingresar.pack(pady=10)
        
        # Crear botón de apagar en la esquina inferior derecha             
        self.icono_apagar = ctk.CTkImage(Image.open(os.path.join(carpeta_imagenes, "power-off.png")), size=(40, 40))
        etiqueta_apagar = ctk.CTkLabel(self, image=self.icono_apagar, text="")
        etiqueta_apagar.place(relx=0.98, rely=0.95, anchor='se')  # Posiciona en la esquina inferior derecha
        etiqueta_apagar.bind("<Button-1>", lambda e: self.apagar())  # Asocia la imagen con el evento de apagado
        
        # Bucle de ejecución
        self.root.mainloop() 
        
            # Función para validar el login
    def validar(self):
        # Se destruye la ventana de login
        self.root.destroy()
        # Se instancia la ventana de opciones
        ventana_opciones = Escritorio()
    
    # Función para apagar la aplicación       
    def apagar(self):
        self.root.destroy()  # Cierra la aplicación

# Clase para el Escritorio
class Escritorio:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Escritorio")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Configurar la geometría de la ventana para que ocupe toda la pantalla
        imagen_fondo = Image.open(os.path.join(carpeta_imagenes, "Escritorio.webp"))  # Cargar la imagen de fondo
        imagen_fondo = imagen_fondo.resize((ancho_pantalla, alto_pantalla), Image.LANCZOS )  # Redimensionar la imagen al tamaño de la pantalla
        fondo = ImageTk.PhotoImage(imagen_fondo)
        
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        # Crear un Label para el fondo y colocarlo en la ventana
        fondo_label = ctk.CTkLabel(self.root, image=fondo, text="")
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Establecer el fondo en toda la ventana

        # Crear un contenedor para los botones (un Frame)
        self.frame_botones = ctk.CTkFrame(self.root, corner_radius=1)
        self.frame_botones.configure(bg_color='#000000')
        self.frame_botones.pack(side="bottom")  # Ubicar el frame en la parte inferior de la ventana

        # Lista de tuplas con imágenes
        iconos = [
            (Image.open(os.path.join(carpeta_imagenes, 'aplicaciones.png')).resize((20, 20)), None),
            (Image.open(os.path.join(carpeta_imagenes, 'editor-de-texto.png')).resize((20, 20)), None),
            (Image.open(os.path.join(carpeta_imagenes, 'calculadora.png')).resize((20, 20)), None),
            (Image.open(os.path.join(carpeta_imagenes, 'configuraciones.png')).resize((20, 20)), None),
        ]

        # Escala las imágenes para que se ajusten a los botones
        imagenes_tk = [ImageTk.PhotoImage(imagen) for imagen, _ in iconos]

        # Crea los botones con íconos y sus acciones asociadas
        for index, (imagen_tk, accion) in enumerate(zip(imagenes_tk, (accion for _, accion in iconos))):
            button = ctk.CTkButton(
                master=self.frame_botones,
                image=imagen_tk,
                text='',
                command=accion,
                fg_color='white',
            )
            button.configure(width=imagen_tk.width(), height=imagen_tk.height())
            button.pack(side="left", padx=5, pady=5)  # Organizar los botones en una fila


        self.frame_reloj = ctk.CTkFrame(self.root, width=200, height=100, bg_color="black")
        self.frame_reloj.pack(side="bottom", anchor="se", padx=0, pady=0)  # Alinear en la parte inferior izquierda
        # Crear un label para mostrar la hora
        self.label_hora = ctk.CTkLabel(self.frame_reloj, font=("Whisper", 50))
        self.label_hora.pack()

        # Actualizar la hora cada segundo
        self.actualizar_hora()

    def actualizar_hora(self):
        # Obtener la hora actual
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        # Mostrar la hora en el label
        self.label_hora.configure(text=hora_actual)
        
        # Llamar a esta función nuevamente después de 1000 ms (1 segundo)
        self.root.after(1000, self.actualizar_hora)

        self.root.mainloop()


Login()
        
        
