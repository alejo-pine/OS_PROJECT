import customtkinter as ctk
import pygame
from tkinter.filedialog import askopenfilename

# Inicializa pygame para gestionar el audio
pygame.mixer.init()

class ReproductorAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Audio")
        self.root.geometry("400x200")

        self.esta_pausado = False  # Estado del audio (pausado o no)

        # Controles del reproductor
        self.boton_abrir = ctk.CTkButton(self.root, text="Abrir archivo", command=self.abrir_archivo)
        self.boton_abrir.pack(pady=10)

        self.boton_reproducir = ctk.CTkButton(self.root, text="Reproducir", command=self.reproducir_audio, state="disabled")
        self.boton_reproducir.pack(pady=5)

        self.boton_pausar = ctk.CTkButton(self.root, text="Pausar", command=self.pausar_audio, state="disabled")
        self.boton_pausar.pack(pady=5)

        self.boton_detener = ctk.CTkButton(self.root, text="Detener", command=self.detener_audio, state="disabled")
        self.boton_detener.pack(pady=5)

        self.volumen = ctk.CTkSlider(self.root, from_=0, to=1, command=self.ajustar_volumen)
        self.volumen.set(1)  # Volumen por defecto
        self.volumen.pack(pady=10)

        self.archivo_seleccionado = None

    def abrir_archivo(self):
        # Abrir el diálogo para seleccionar un archivo de audio
        archivo = askopenfilename(filetypes=[("Archivos de audio", "*.mp3 *.wav")])
        if archivo:
            self.archivo_seleccionado = archivo
            self.boton_reproducir.configure(state="normal")
            self.boton_pausar.configure(state="normal")
            self.boton_detener.configure(state="normal")

    def reproducir_audio(self):
        if self.archivo_seleccionado:
            pygame.mixer.music.load(self.archivo_seleccionado)
            pygame.mixer.music.play()
            self.esta_pausado = False  # Reiniciar estado

    def pausar_audio(self):
        if pygame.mixer.music.get_busy():  # Si hay audio en reproducción
            if self.esta_pausado:
                pygame.mixer.music.unpause()  # Despausar el audio
                self.boton_pausar.configure(text="Pausar")
                self.esta_pausado = False
            else:
                pygame.mixer.music.pause()  # Pausar el audio
                self.boton_pausar.configure(text="Reanudar")
                self.esta_pausado = True

    def detener_audio(self):
        pygame.mixer.music.stop()
        self.esta_pausado = False
        self.boton_pausar.configure(text="Pausar")  # Restablecer el texto del botón

    def ajustar_volumen(self, valor):
        pygame.mixer.music.set_volume(float(valor))

if __name__ == "__main__":
    root = ctk.CTk()
    app = ReproductorAudio(root)
    root.mainloop()
