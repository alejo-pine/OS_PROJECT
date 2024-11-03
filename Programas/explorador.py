import sys
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QVBoxLayout, QWidget
from PyQt5.QtCore import QModelIndex

class ExploradorArchivos(QWidget):
    def __init__(self, ruta_inicial=None):
        super().__init__()
        self.ruta_inicial = ruta_inicial if ruta_inicial else ''  
        self.inicializarGui()
    
    def inicializarGui(self):
        self.setWindowTitle('Explorador de archivos')
        self.setFixedSize(600, 600)

        self.modelo = QFileSystemModel()
        self.modelo.setRootPath(self.ruta_inicial)

        self.explorador = QTreeView()
        self.explorador.setModel(self.modelo)

        if self.ruta_inicial:
            self.explorador.setRootIndex(self.modelo.index(self.ruta_inicial))

        self.explorador.setAnimated(False)
        self.explorador.setIndentation(20)
        self.explorador.setSortingEnabled(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.explorador)

        self.setLayout(self.layout)

        self.show()

def main():
    app = QApplication(sys.argv)
    
    # Obtener ruta desde los argumentos
    ruta_usuario = sys.argv[1] if len(sys.argv) > 1 else None
    dialogo = ExploradorArchivos(ruta_usuario)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
