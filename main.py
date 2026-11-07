import sys
from PySide6.QtWidgets import QApplication

# Importamos la ventana de Gabriel y el controlador de Pablo
from ui.ventana_partenon import VentanaPartenon
from controllers.controlador_main import ControladorPartenon

def iniciar_sistema():
    app = QApplication(sys.argv)
    
    # 1. Creamos la interfaz visual (Gabriel)
    ventana = VentanaPartenon()
    
    # 2. Le inyectamos la lógica y conexión a BD (Pablo y Antonio)
    controlador = ControladorPartenon(ventana)
    
    # 3. Mostramos la ventana
    ventana.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_sistema()