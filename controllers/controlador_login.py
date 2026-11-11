from PySide6.QtWidgets import QMessageBox

from ui.ventana_partenon import VentanaPartenon
from controllers.controlador_main import ControladorMain
from security.auth_manager import verificar_credenciales


class ControladorLogin:
    def __init__(self, ventana_login):
        self.ventana_login = ventana_login

        # Clic en el botón "Ingresar"
        self.ventana_login.boton_ingresar.clicked.connect(self.procesar_login)

        # Enter en cualquiera de los dos campos también inicia sesión
        self.ventana_login.usuario.returnPressed.connect(self.procesar_login)
        self.ventana_login.contrasena.returnPressed.connect(self.procesar_login)

    def procesar_login(self):
        usuario = self.ventana_login.usuario.text().strip()
        contrasena = self.ventana_login.contrasena.text().strip()

        try:
            if not usuario or not contrasena:
                raise ValueError("Los campos de usuario y contraseña no pueden estar vacíos.")

            # Autenticación mediante el módulo de seguridad (SHA-256 + HMAC)
            if verificar_credenciales(usuario, contrasena):
                self.iniciar_sesion()
            else:
                raise ValueError("Credenciales incorrectas. Verifica tus datos.")

        except ValueError as e:
            # Antes solo se imprimía en consola; ahora el usuario ve el error
            QMessageBox.warning(self.ventana_login, "Error de acceso", str(e))
            self.ventana_login.contrasena.clear()
            self.ventana_login.contrasena.setFocus()

    def iniciar_sesion(self):
        # Se guardan en self para evitar que el recolector de basura cierre la ventana
        self.ventana_partenon = VentanaPartenon()
        self.controlador_partenon = ControladorMain(self.ventana_partenon)

        self.ventana_partenon.show()
        self.ventana_login.close()