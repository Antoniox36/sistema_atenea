from ui.ventana_partenon import VentanaPartenon
from controllers.controlador_main import ControladorMain
from security.auth_manager import verificar_credenciales

class ControladorLogin:
    def __init__(self, ventana_login):
        self.ventana_login = ventana_login
        
        # 1. Capturar la interacción: Enlazar el botón de la ventana de login
        self.ventana_login.boton_ingresar.clicked.connect(self.procesar_login)

    def procesar_login(self):
        # Extraer el texto ingresado en los campos de usuario y contraseña
        usuario = self.ventana_login.usuario.text().strip()
        contrasena = self.ventana_login.contrasena.text().strip()

        # 2. Lógica de autenticación y validación
        try:
            if not usuario or not contrasena:
                raise ValueError("Los campos de usuario y contraseña no pueden estar vacíos.")
            
            # Evaluación segura mediante el módulo de seguridad de Samuel (SHA-256 + HMAC)
            if verificar_credenciales(usuario, contrasena):
                print("Acceso exitoso con SHA-256. Preparando el sistema...")
                self.iniciar_sesion()
            else:
                raise ValueError("Credenciales incorrectas. Verifica tus datos.")
                
        except ValueError as e:
            # Atrapa la excepción y notifica el fallo en consola
            print(f"Error de acceso: {e}")

    def iniciar_sesion(self):
        # 3. Gestionar la transición entre ventanas
        
        # Instanciar la nueva ventana del Partenón (se guarda en self para evitar recolección de basura)
        self.ventana_partenon = VentanaPartenon()
        
        # Conectar la ventana del Partenón al controlador principal
        self.controlador_partenon = ControladorMain(self.ventana_partenon)
        
        # Hacer visible el Partenón
        self.ventana_partenon.show()
        
        # Cerrar la pantalla de Login
        self.ventana_login.close()