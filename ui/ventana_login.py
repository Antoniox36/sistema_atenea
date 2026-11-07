import sys

from PySide6.QtCore import Qt  # pyright: ignore[reportMissingImports]
from PySide6.QtWidgets import (  # pyright: ignore[reportMissingImports]
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class VentanaLogin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Atenea | Ingreso")
        self.setFixedSize(760, 440)
        
        # Elimina la barra de título y los marcos nativos de Windows
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.centrar_en_pantalla()

        central = QWidget()
        central.setObjectName("loginWindow")
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tarjeta principal con bordes redondeados limpios
        card = QFrame()
        card.setObjectName("loginCard")
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Panel izquierdo: Marca / Identidad Atenea
        brand_panel = QFrame()
        brand_panel.setObjectName("brandPanel")
        brand_layout = QVBoxLayout(brand_panel)
        brand_layout.setContentsMargins(40, 40, 40, 40)
        brand_layout.setSpacing(10)

        emblem = QLabel("A")
        emblem.setObjectName("emblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setFixedSize(52, 52)

        brand_name = QLabel("ATENEA")
        brand_name.setObjectName("brandName")
        subtitle = QLabel("SISTEMA ACADÉMICO")
        subtitle.setObjectName("brandSubtitle")
        welcome = QLabel("El conocimiento\nconstruye el futuro.")
        welcome.setObjectName("brandMessage")

        brand_layout.addWidget(emblem, alignment=Qt.AlignmentFlag.AlignLeft)
        brand_layout.addSpacing(10)
        brand_layout.addWidget(brand_name)
        brand_layout.addWidget(subtitle)
        brand_layout.addSpacing(14)
        brand_layout.addWidget(welcome)
        brand_layout.addStretch()

        # Panel derecho: Formulario de ingreso
        form_panel = QFrame()
        form_panel.setObjectName("formPanel")
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(40, 25, 40, 40)
        form_layout.setSpacing(8)

        # Barra superior con botón de cierre personalizado (ya que no hay barra de Windows)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.addStretch()
        
        self.btn_cerrar = QPushButton("×")
        self.btn_cerrar.setObjectName("closeButton")
        self.btn_cerrar.setFixedSize(28, 28)
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.clicked.connect(self.close)
        top_bar_layout.addWidget(self.btn_cerrar)

        eyebrow = QLabel("ACCESO")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Bienvenido")
        title.setObjectName("formTitle")
        description = QLabel("Credenciales para continuar.")
        description.setObjectName("formDescription")
        description.setWordWrap(True)

        user_label = QLabel("Usuario")
        self.usuario = QLineEdit()
        self.usuario.setObjectName("usuarioInput")
        self.usuario.setPlaceholderText("Escribe tu usuario")
        self.usuario.setClearButtonEnabled(True)

        password_label = QLabel("Contraseña")
        self.contrasena = QLineEdit()
        self.contrasena.setObjectName("contrasenaInput")
        self.contrasena.setPlaceholderText("Escribe tu contraseña")
        self.contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.setObjectName("primaryButton")
        self.boton_ingresar.setMinimumHeight(40)
        self.boton_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)

        form_layout.addLayout(top_bar_layout)
        form_layout.addWidget(eyebrow)
        form_layout.addWidget(title)
        form_layout.addWidget(description)
        form_layout.addSpacing(4)
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.usuario)
        form_layout.addSpacing(4)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.contrasena)
        form_layout.addSpacing(12)
        form_layout.addWidget(self.boton_ingresar)
        form_layout.addStretch()

        card_layout.addWidget(brand_panel, 5)
        card_layout.addWidget(form_panel, 6)

        main_layout.addWidget(card)

        # Estilos visuales limpios sin marcos del sistema operativo
        self.setStyleSheet(
            """
            QWidget#loginWindow {
                background-color: transparent;
            }
            QFrame#loginCard {
                background-color: #FFFFFF;
                border-radius: 14px;
                border: 1px solid #DCDDD8;
            }
            QFrame#brandPanel {
                background-color: #14243A;
                border-top-left-radius: 14px;
                border-bottom-left-radius: 14px;
            }
            QFrame#formPanel {
                background-color: #FFFFFF;
                border-top-right-radius: 14px;
                border-bottom-right-radius: 14px;
            }
            QPushButton#closeButton {
                background-color: transparent;
                border: none;
                color: #8A94A0;
                font-size: 20px;
                font-weight: 700;
                border-radius: 4px;
            }
            QPushButton#closeButton:hover {
                background-color: #F0F2F5;
                color: #C0392B;
            }
            QLabel#emblem {
                background-color: #1D334D;
                border-radius: 26px;
                color: #FFFFFF;
                font-family: Georgia;
                font-size: 26px;
                font-weight: 700;
            }
            QLabel#brandName {
                color: #FFFFFF;
                font-size: 20px;
                font-weight: 700;
                letter-spacing: 3px;
            }
            QLabel#brandSubtitle {
                color: #A2B4C8;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 1.5px;
            }
            QLabel#brandMessage {
                color: #E8ECEF;
                font-family: Georgia;
                font-size: 16px;
                line-height: 1.3;
            }
            QLabel#eyebrow {
                color: #8A7135;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1.5px;
            }
            QLabel#formTitle {
                color: #18283E;
                font-size: 22px;
                font-weight: 700;
            }
            QLabel#formDescription {
                color: #737B84;
                font-size: 11px;
                padding-bottom: 2px;
            }
            QLabel {
                color: #263447;
                font-size: 11px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #FAFAF8;
                border: 1px solid #DCDDD8;
                border-radius: 6px;
                color: #202B3A;
                font-size: 12px;
                min-height: 18px;
                padding: 8px 10px;
                selection-background-color: #52657A;
            }
            QLineEdit:focus {
                border: 1px solid #68798B;
                background-color: #FFFFFF;
            }
            QLineEdit::placeholder {
                color: #A0A5A9;
            }
            QPushButton#primaryButton {
                background-color: #D7B45A;
                border: none;
                border-radius: 6px;
                color: #17263A;
                font-size: 12px;
                font-weight: 700;
            }
            QPushButton#primaryButton:hover {
                background-color: #E1C574;
            }
            QPushButton#primaryButton:pressed {
                background-color: #C6A348;
            }
            """
        )

    def centrar_en_pantalla(self):
        screen_center = self.screen().availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(screen_center)
        self.move(geo.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaLogin()
    window.show()
    sys.exit(app.exec())