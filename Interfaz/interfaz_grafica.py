import customtkinter as ctk
import os
from PIL import Image

# Carpeta de imágenes
carpeta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

# Configuración de la apariencia de la interfaz gráfica
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('green')

class Login(ctk.CTk):
    
    def __init__(self):
        super().__init__()  # Instancia de CTk
        self.title("Hermes OS")  # Título
        self.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))  # Icono
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        self.geometry(f"{ancho_pantalla}x{alto_pantalla}")  # Tamaño inicial de la ventana
        self.state('zoomed')  # Maximiza la ventana
        self.resizable(True, True)  # Permitir redimensión de ventana

        # Establecer el fondo de la ventana
        self.configure(bg="darkgray")

        # Contenido de la ventana principal
        # Carga de la imagen
        logo = ctk.CTkImage(
            light_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            dark_image=Image.open(os.path.join(carpeta_imagenes, "Login.png")),
            size=(500, 300)  # Tamaño de las imágenes
        )

        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master=self, image=logo, text="")
        etiqueta.pack(pady=15)

        # Campos de texto
        ctk.CTkLabel(self, text="Usuario").pack(pady=(10, 0))
        self.usuario = ctk.CTkEntry(self, width=300, height=40)  # Tamaño aumentado
        self.usuario.insert(0, "Nombre de usuario")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Contraseña").pack(pady=(10, 0))
        self.contrasena = ctk.CTkEntry(self, show="*", width=300, height=40)  # Tamaño aumentado
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack(pady=(0, 20))

        self.boton_ingresar = ctk.CTkButton(self, text="Ingresar", width=150, height=40, fg_color="blue", hover_color="darkblue")
        self.boton_ingresar.pack(pady=10)

        # Crear botón de apagar en la esquina inferior derecha             
        icono_apagar = ctk.CTkImage(Image.open(os.path.join(carpeta_imagenes, "power-off.png")), size=(40, 40))
        etiqueta_apagar = ctk.CTkLabel(self, image=icono_apagar, text="")
        etiqueta_apagar.place(relx=0.98, rely=0.95, anchor='se')  # Posiciona en la esquina inferior derecha
        etiqueta_apagar.bind("<Button-1>", lambda e: self.apagar())  # Asocia la imagen con el evento de apagado

        
    def apagar(self):
        self.destroy()  # Cierra la aplicación

# Ejecutar la ventana
if __name__ == "__main__":
    app = Login()
    app.mainloop() 