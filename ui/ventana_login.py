import sys

from PySide6.QtCore import Qt  # pyright: ignore[reportMissingImports]
from PySide6.QtWidgets import (  # pyright: ignore[reportMissingImports]
    QApplication,
    QFrame,
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
        self.setMinimumSize(760, 560)
        self.resize(960, 620)

        central = QWidget()
        central.setObjectName("loginWindow")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 28, 28, 28)

        card = QFrame()
        card.setObjectName("loginCard")
        layout.addWidget(card)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        brand_panel = QFrame()
        brand_panel.setObjectName("brandPanel")
        brand_layout = QVBoxLayout(brand_panel)
        brand_layout.setContentsMargins(48, 48, 48, 48)
        brand_layout.setSpacing(14)

        emblem = QLabel("A")
        emblem.setObjectName("emblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setFixedSize(66, 66)

        brand_name = QLabel("ATENEA")
        brand_name.setObjectName("brandName")
        subtitle = QLabel("SISTEMA ACADEMICO")
        subtitle.setObjectName("brandSubtitle")
        welcome = QLabel("El conocimiento\nconstruye el futuro.")
        welcome.setObjectName("brandMessage")

        brand_layout.addWidget(emblem, alignment=Qt.AlignmentFlag.AlignLeft)
        brand_layout.addSpacing(20)
        brand_layout.addWidget(brand_name)
        brand_layout.addWidget(subtitle)
        brand_layout.addSpacing(18)
        brand_layout.addWidget(welcome)
        brand_layout.addStretch()

        form_panel = QFrame()
        form_panel.setObjectName("formPanel")
        form_layout = QVBoxLayout(form_panel)
        form_layout.setContentsMargins(52, 48, 52, 48)
        form_layout.setSpacing(12)

        eyebrow = QLabel("ACCESO")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("Bienvenido")
        title.setObjectName("formTitle")
        description = QLabel("Ingresa tus credenciales para continuar.")
        description.setObjectName("formDescription")
        description.setWordWrap(True)

        user_label = QLabel("Usuario")
        self.usuario = QLineEdit()
        self.usuario.setObjectName("usuarioInput")
        self.usuario.setPlaceholderText("Escribe tu usuario")
        self.usuario.setClearButtonEnabled(True)

        password_label = QLabel("Contrasena")
        self.contrasena = QLineEdit()
        self.contrasena.setObjectName("contrasenaInput")
        self.contrasena.setPlaceholderText("Escribe tu contrasena")
        self.contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.setObjectName("primaryButton")
        self.boton_ingresar.setMinimumHeight(48)
        self.boton_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)

        form_layout.addWidget(eyebrow)
        form_layout.addWidget(title)
        form_layout.addWidget(description)
        form_layout.addSpacing(22)
        form_layout.addWidget(user_label)
        form_layout.addWidget(self.usuario)
        form_layout.addSpacing(8)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.contrasena)
        form_layout.addSpacing(18)
        form_layout.addWidget(self.boton_ingresar)
        form_layout.addStretch()

        card_layout.addWidget(brand_panel, 5)
        card_layout.addWidget(form_panel, 6)

        self.setStyleSheet(
            """
            QWidget#loginWindow {
                background-color: #F1F1ED;
                color: #202B3A;
                font-family: "Segoe UI";
            }
            QFrame#loginCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E5DF;
                border-radius: 14px;
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
            QLabel#emblem {
                background-color: #E5E8EB;
                border-radius: 33px;
                color: #14243A;
                font-family: Georgia;
                font-size: 34px;
                font-weight: 700;
            }
            QLabel#brandName {
                color: #FFFFFF;
                font-size: 25px;
                font-weight: 700;
                letter-spacing: 4px;
            }
            QLabel#brandSubtitle {
                color: #C5CED8;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 2px;
            }
            QLabel#brandMessage {
                color: #F3F4F2;
                font-family: Georgia;
                font-size: 22px;
                line-height: 1.4;
            }
            QLabel#eyebrow {
                color: #8A7135;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }
            QLabel#formTitle {
                color: #18283E;
                font-size: 30px;
                font-weight: 700;
            }
            QLabel#formDescription {
                color: #737B84;
                font-size: 13px;
                padding-bottom: 4px;
            }
            QLabel {
                color: #263447;
                font-size: 12px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #FAFAF8;
                border: 1px solid #DCDDD8;
                border-radius: 7px;
                color: #202B3A;
                font-size: 14px;
                min-height: 22px;
                padding: 11px 12px;
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
                border-radius: 7px;
                color: #17263A;
                font-size: 14px;
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaLogin()
    window.show()
    sys.exit(app.exec())