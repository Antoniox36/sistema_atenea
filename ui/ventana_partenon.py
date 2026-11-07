import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (  # pyright: ignore[reportMissingImports]
    QApplication,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class VentanaPartenon(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Atenea | El Partenon")
        self.setMinimumSize(980, 650)
        self.resize(1280, 800)

        central = QWidget()
        central.setObjectName("mainWindow")
        self.setCentralWidget(central)
        root = QGridLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(228)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(24, 28, 24, 26)
        sidebar_layout.setSpacing(12)

        emblem = QLabel("A")
        emblem.setObjectName("sidebarEmblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setFixedSize(46, 46)
        brand = QLabel("ATENEA")
        brand.setObjectName("sidebarBrand")
        brand_caption = QLabel("SISTEMA ACADEMICO")
        brand_caption.setObjectName("sidebarCaption")

        nav_heading = QLabel("GESTION")
        nav_heading.setObjectName("navHeading")
        nav_item = QLabel("  Pupilos")
        nav_item.setObjectName("selectedNavItem")

        sidebar_layout.addWidget(emblem, alignment=Qt.AlignmentFlag.AlignLeft)
        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(brand_caption)
        sidebar_layout.addSpacing(42)
        sidebar_layout.addWidget(nav_heading)
        sidebar_layout.addWidget(nav_item)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(QLabel("Prototipo de interfaz"))

        content = QWidget()
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(34, 28, 34, 30)
        content_layout.setSpacing(22)

        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar_layout = QVBoxLayout(topbar)
        topbar_layout.setContentsMargins(26, 18, 26, 18)
        topbar_layout.setSpacing(4)
        page_title = QLabel("El Partenon")
        page_title.setObjectName("pageTitle")
        page_subtitle = QLabel("Administracion de pupilos")
        page_subtitle.setObjectName("pageSubtitle")
        topbar_layout.addWidget(page_title)
        topbar_layout.addWidget(page_subtitle)
        content_layout.addWidget(topbar)

        section_heading = QLabel("Registro de Iniciados/Pupilos")
        section_heading.setObjectName("sectionHeading")
        content_layout.addWidget(section_heading)

        workspace = QWidget()
        workspace_layout = QGridLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setHorizontalSpacing(20)
        workspace_layout.setVerticalSpacing(14)

        form_card = QFrame()
        form_card.setObjectName("surfaceCard")
        form_card.setMinimumWidth(280)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(22, 22, 22, 22)
        form_layout.setSpacing(11)

        form_title = QLabel("Datos del pupilo")
        form_title.setObjectName("cardTitle")
        form_hint = QLabel("Completa la informacion de registro.")
        form_hint.setObjectName("cardHint")
        form_hint.setWordWrap(True)
        form_layout.addWidget(form_title)
        form_layout.addWidget(form_hint)
        form_layout.addSpacing(8)

        self.carnet = QLineEdit()
        self.carnet.setObjectName("carnetInput")
        self.carnet.setPlaceholderText("Ej. 20240001")
        self.nombre = QLineEdit()
        self.nombre.setObjectName("nombreInput")
        self.nombre.setPlaceholderText("Nombre completo")
        self.carrera = QLineEdit()
        self.carrera.setObjectName("carreraInput")
        self.carrera.setPlaceholderText("Carrera")
        self.ciclo = QLineEdit()
        self.ciclo.setObjectName("cicloInput")
        self.ciclo.setPlaceholderText("Ej. Primer ciclo")

        for field_label, field in (
            ("Carnet", self.carnet),
            ("Nombre", self.nombre),
            ("Carrera", self.carrera),
            ("Ciclo", self.ciclo),
        ):
            form_layout.addWidget(QLabel(field_label))
            form_layout.addWidget(field)

        self.boton_registrar = QPushButton("Registrar Pupilo")
        self.boton_registrar.setObjectName("primaryButton")
        self.boton_registrar.setMinimumHeight(46)
        self.boton_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        form_layout.addSpacing(9)
        form_layout.addWidget(self.boton_registrar)
        form_layout.addStretch()

        table_card = QFrame()
        table_card.setObjectName("surfaceCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(12)
        table_title = QLabel("Pupilos registrados")
        table_title.setObjectName("cardTitle")
        table_hint = QLabel("Los registros apareceran en esta tabla.")
        table_hint.setObjectName("cardHint")

        self.tabla_pupilos = QTableWidget(0, 4)
        self.tabla_pupilos.setObjectName("tablaPupilos")
        self.tabla_pupilos.setHorizontalHeaderLabels(
            ["Carnet", "Nombre", "Carrera", "Ciclo"]
        )
        self.tabla_pupilos.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.tabla_pupilos.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla_pupilos.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.tabla_pupilos.setAlternatingRowColors(True)
        self.tabla_pupilos.verticalHeader().setVisible(False)
        self.tabla_pupilos.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla_pupilos.setShowGrid(False)

        table_layout.addWidget(table_title)
        table_layout.addWidget(table_hint)
        table_layout.addSpacing(6)
        table_layout.addWidget(self.tabla_pupilos, 1)

        workspace_layout.addWidget(form_card, 0, 0)
        workspace_layout.addWidget(table_card, 0, 1)
        workspace_layout.setColumnStretch(0, 2)
        workspace_layout.setColumnStretch(1, 5)
        content_layout.addWidget(workspace, 1)

        root.addWidget(sidebar, 0, 0)
        root.addWidget(content, 0, 1)
        root.setColumnStretch(1, 1)

        self.setStyleSheet(
            """
            QWidget#mainWindow {
                background-color: #F1F1ED;
                color: #202B3A;
                font-family: "Segoe UI";
            }
            QWidget#contentArea {
                background-color: #F1F1ED;
            }
            QFrame#sidebar {
                background-color: #14243A;
                border: none;
            }
            QLabel#sidebarEmblem {
                background-color: #E5E8EB;
                border-radius: 23px;
                color: #14243A;
                font-family: Georgia;
                font-size: 25px;
                font-weight: 700;
            }
            QLabel#sidebarBrand {
                color: #FFFFFF;
                font-size: 19px;
                font-weight: 700;
                letter-spacing: 3px;
            }
            QLabel#sidebarCaption {
                color: #AEBAC8;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 1.2px;
            }
            QLabel#navHeading {
                color: #95A3B4;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1.6px;
                padding-left: 8px;
            }
            QLabel#selectedNavItem {
                background-color: #243951;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 13px;
                padding: 11px 8px;
            }
            QFrame#topbar {
                background-color: #14243A;
                border-radius: 9px;
            }
            QLabel#pageTitle {
                color: #FFFFFF;
                font-size: 21px;
                font-weight: 700;
            }
            QLabel#pageSubtitle {
                color: #C1CBD5;
                font-size: 12px;
            }
            QLabel#sectionHeading {
                color: #18283E;
                font-size: 20px;
                font-weight: 700;
            }
            QFrame#surfaceCard {
                background-color: #FFFFFF;
                border: 1px solid #E4E4DE;
                border-radius: 9px;
            }
            QLabel#cardTitle {
                color: #1D2D42;
                font-size: 15px;
                font-weight: 700;
            }
            QLabel#cardHint {
                color: #7A828B;
                font-size: 11px;
            }
            QLabel {
                color: #354255;
                font-size: 11px;
                font-weight: 600;
            }
            QLineEdit {
                background-color: #FAFAF8;
                border: 1px solid #DCDDD8;
                border-radius: 6px;
                color: #202B3A;
                font-size: 12px;
                min-height: 20px;
                padding: 9px 10px;
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
            QTableWidget#tablaPupilos {
                background-color: #FFFFFF;
                alternate-background-color: #F7F7F4;
                border: 1px solid #E7E8E3;
                border-radius: 6px;
                color: #263447;
                font-size: 11px;
                selection-background-color: #E8EDF1;
                selection-color: #17263A;
            }
            QHeaderView::section {
                background-color: #F1F2EF;
                border: none;
                border-bottom: 1px solid #E2E3DE;
                color: #455365;
                font-size: 10px;
                font-weight: 700;
                padding: 10px 7px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #F1F2EF;
                border: none;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPartenon()
    window.show()
    sys.exit(app.exec())