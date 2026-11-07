# main.py (Actualizado)
import sys
from PySide6.QtWidgets import QApplication

from ui.ventana_partenon import VentanaPartenon
# 1. Cambiamos el nombre de la clase a ControladorMain
from controllers.controlador_main import ControladorMain

def iniciar_sistema():
    app = QApplication(sys.argv)
    ventana = VentanaPartenon()
    
    # 2. Instanciamos con el nombre correcto
    controlador = ControladorMain(ventana)
    
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_sistema()