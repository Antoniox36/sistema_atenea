import sys
from PySide6.QtWidgets import QApplication

# Importación de la base de datos (al importar conexion se inicializa la BD)
import database.conexion
from ui.ventana_login import VentanaLogin
from ui.ventana_partenon import VentanaPartenon
from controllers.controlador_main import ControladorMain
from controllers.controlador_login import ControladorLogin

def iniciar_sistema():
    app = QApplication(sys.argv)
    
    # 1. Instanciamos la ventana de login y su respectiva vista
    ventana_login = VentanaLogin()
    
    # 2. Instanciamos el controlador de login, pasándole la ventana
    # Nota: El controlador de login debe encargarse de ocultar esta ventana 
    # y abrir la VentanaPartenon + ControladorMain al autenticar con éxito.
    controlador_login = ControladorLogin(ventana_login)
    
    # 3. Mostramos la ventana de inicio de sesión
    ventana_login.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_sistema()