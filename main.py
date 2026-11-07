import sys
from PySide6.QtWidgets import QApplication

# Importación de la base de datos (al importar conexion se ejecuta inicializar_bd)
import database.conexion
from ui.ventana_partenon import VentanaPartenon
from controllers.controlador_main import ControladorMain

def iniciar_sistema():
    app = QApplication(sys.argv)
    
    # 1. Instanciamos la ventana visual de Gabriel
    ventana = VentanaPartenon()
    
    # 2. Conectamos la ventana con el controlador de Pablo y la BD
    controlador = ControladorMain(ventana)
    
    # 3. Mostramos la interfaz gráfica
    ventana.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_sistema()