import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (  # pyright: ignore[reportMissingImports]
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)


class VentanaPartenon(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Atenea | El Partenón")
        self.setMinimumSize(980, 650)
        self.resize(1280, 800)
        
        # Ventana flotante sin bordes nativos de Windows, con esquinas redondeadas
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.centrar_en_pantalla()
        self.drag_position = QPoint()

        central = QWidget()
        central.setObjectName("mainWindow")
        self.setCentralWidget(central)
        
        root = QHBoxLayout(central)
        root.setContentsMargins(10, 10, 10, 10)  # Margen para la sombra de la ventana flotante
        root.setSpacing(0)

        app_container = QFrame()
        app_container.setObjectName("appContainer")
        app_layout = QHBoxLayout(app_container)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)

        # ---------------------------------------------------------
        # BARRA LATERAL (SIDEBAR) OCULTABLE
        # ---------------------------------------------------------
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(230)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(18, 24, 18, 22)
        sidebar_layout.setSpacing(12)

        emblem = QLabel("A")
        emblem.setObjectName("sidebarEmblem")
        emblem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        emblem.setFixedSize(44, 44)
        
        brand = QLabel("ATENEA")
        brand.setObjectName("sidebarBrand")
        
        brand_caption = QLabel("SISTEMA ACADÉMICO")
        brand_caption.setObjectName("sidebarCaption")

        nav_heading = QLabel("GESTIÓN")
        nav_heading.setObjectName("navHeading")
        
        nav_item = QLabel("  Pupilos")
        nav_item.setObjectName("selectedNavItem")

        sidebar_layout.addWidget(emblem, alignment=Qt.AlignmentFlag.AlignLeft)
        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(brand_caption)
        sidebar_layout.addSpacing(28)
        sidebar_layout.addWidget(nav_heading)
        sidebar_layout.addWidget(nav_item)
        sidebar_layout.addStretch()
        
        footer_label = QLabel("Módulo Principal")
        footer_label.setObjectName("sidebarFooter")
        sidebar_layout.addWidget(footer_label)

        # ---------------------------------------------------------
        # ÁREA DE CONTENIDO PRINCIPAL
        # ---------------------------------------------------------
        content = QWidget()
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 24)
        content_layout.setSpacing(18)

        # Barra superior (Topbar) con el botón de menú siempre visible y controles de ventana
        self.topbar = QFrame()
        self.topbar.setObjectName("topbar")
        topbar_layout = QHBoxLayout(self.topbar)
        topbar_layout.setContentsMargins(16, 12, 16, 12)
        topbar_layout.setSpacing(12)

        self.btn_toggle = QPushButton("≡  Menú")
        self.btn_toggle.setObjectName("toggleButton")
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setFixedSize(80, 34)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(1)
        page_title = QLabel("El Partenón")
        page_title.setObjectName("pageTitle")
        page_subtitle = QLabel("Panel de administración y control de pupilos")
        page_subtitle.setObjectName("pageSubtitle")
        title_layout.addWidget(page_title)
        title_layout.addWidget(page_subtitle)

        # Botones de control de ventana (Minimizar, Maximizar/Restaurar, Cerrar)
        self.btn_min = QPushButton("─")
        self.btn_min.setObjectName("windowButton")
        self.btn_min.setFixedSize(30, 30)
        self.btn_min.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_min.clicked.connect(self.showMinimized)

        self.btn_max = QPushButton("□")
        self.btn_max.setObjectName("windowButton")
        self.btn_max.setFixedSize(30, 30)
        self.btn_max.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_max.clicked.connect(self.toggle_maximize)

        self.btn_cerrar = QPushButton("×")
        self.btn_cerrar.setObjectName("closeButton")
        self.btn_cerrar.setFixedSize(30, 30)
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.clicked.connect(self.close)

        topbar_layout.addWidget(self.btn_toggle)
        topbar_layout.addWidget(title_container, 1)
        topbar_layout.addWidget(self.btn_min)
        topbar_layout.addWidget(self.btn_max)
        topbar_layout.addWidget(self.btn_cerrar)

        content_layout.addWidget(self.topbar)

        section_heading = QLabel("Registro de Iniciados / Pupilos")
        section_heading.setObjectName("sectionHeading")
        content_layout.addWidget(section_heading)

        # Espacio de trabajo (Formulario + Tabla)
        workspace = QWidget()
        workspace_layout = QGridLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setHorizontalSpacing(18)
        workspace_layout.setVerticalSpacing(14)

        # Tarjeta del Formulario
        form_card = QFrame()
        form_card.setObjectName("surfaceCard")
        form_card.setMinimumWidth(280)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        form_title = QLabel("Datos del pupilo")
        form_title.setObjectName("cardTitle")
        form_hint = QLabel("Complete la información de registro.")
        form_hint.setObjectName("cardHint")
        form_hint.setWordWrap(True)
        form_layout.addWidget(form_title)
        form_layout.addWidget(form_hint)
        form_layout.addSpacing(6)

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
        self.ciclo.setPlaceholderText("Ej. 3")

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
        self.boton_registrar.setMinimumHeight(42)
        self.boton_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        form_layout.addSpacing(8)
        form_layout.addWidget(self.boton_registrar)
        form_layout.addStretch()

        # Tarjeta de la Tabla
        table_card = QFrame()
        table_card.setObjectName("surfaceCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(10)
        table_title = QLabel("Pupilos registrados")
        table_title.setObjectName("cardTitle")
        table_hint = QLabel("Listado general sincronizado con la base de datos.")
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
        header = self.tabla_pupilos.horizontalHeader()
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        header.setMinimumSectionSize(80)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_pupilos.setShowGrid(False)

        table_layout.addWidget(table_title)
        table_layout.addWidget(table_hint)
        table_layout.addSpacing(4)
        table_layout.addWidget(self.tabla_pupilos, 1)

        workspace_layout.addWidget(form_card, 0, 0)
        workspace_layout.addWidget(table_card, 0, 1)
        workspace_layout.setColumnStretch(0, 2)
        workspace_layout.setColumnStretch(1, 5)
        content_layout.addWidget(workspace, 1)

        app_layout.addWidget(self.sidebar)
        app_layout.addWidget(content, 1)

        root.addWidget(app_container)

        # Estilos visuales pulidos
        self.setStyleSheet(
            """
            QWidget#mainWindow {
                background-color: transparent;
            }
            QFrame#appContainer {
                background-color: #F4F4F0;
                border-radius: 12px;
                border: 1px solid #D5D6D0;
            }
            QWidget#contentArea {
                background-color: #F4F4F0;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
            QFrame#sidebar {
                background-color: #14243A;
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
                border: none;
            }
            QPushButton#toggleButton {
                background-color: #1D334D;
                border: none;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 11px;
                font-weight: 700;
                padding: 4px 8px;
            }
            QPushButton#toggleButton:hover {
                background-color: #243D5B;
            }
            QPushButton#windowButton {
                background-color: transparent;
                border: none;
                color: #AEC1D5;
                font-size: 14px;
                font-weight: 700;
                border-radius: 4px;
            }
            QPushButton#windowButton:hover {
                background-color: #1D334D;
                color: #FFFFFF;
            }
            QPushButton#closeButton {
                background-color: transparent;
                border: none;
                color: #AEC1D5;
                font-size: 18px;
                font-weight: 700;
                border-radius: 4px;
            }
            QPushButton#closeButton:hover {
                background-color: #1D334D;
                color: #FFFFFF;
            }
            QLabel#sidebarEmblem {
                background-color: #1D334D;
                border-radius: 22px;
                color: #FFFFFF;
                font-family: Georgia;
                font-size: 22px;
                font-weight: 700;
            }
            QLabel#sidebarBrand {
                color: #FFFFFF;
                font-size: 17px;
                font-weight: 700;
                letter-spacing: 2.5px;
            }
            QLabel#sidebarCaption {
                color: #9FB1C5;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 1.2px;
            }
            QLabel#navHeading {
                color: #8395A7;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 1.5px;
                padding-left: 6px;
            }
            QLabel#selectedNavItem {
                background-color: #1D334D;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 12px;
                padding: 10px 8px;
            }
            QLabel#sidebarFooter {
                color: #6C8197;
                font-size: 10px;
            }
            QFrame#topbar {
                background-color: #14243A;
                border-radius: 8px;
            }
            QLabel#pageTitle {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: 700;
            }
            QLabel#pageSubtitle {
                color: #AEC1D5;
                font-size: 11px;
            }
            QLabel#sectionHeading {
                color: #18283E;
                font-size: 18px;
                font-weight: 700;
            }
            QFrame#surfaceCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E2DC;
                border-radius: 8px;
            }
            QLabel#cardTitle {
                color: #1D2D42;
                font-size: 14px;
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
                border: 1px solid #D5D6D0;
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
            QTableWidget#tablaPupilos {
                background-color: #FFFFFF;
                alternate-background-color: #F8F8F5;
                border: 1px solid #E5E6E0;
                border-radius: 6px;
                color: #263447;
                font-size: 11px;
                selection-background-color: #E8EDF1;
                selection-color: #17263A;
            }
            QHeaderView::section {
                background-color: #EFEFED;
                border: none;
                border-bottom: 1px solid #DCDED7;
                color: #455365;
                font-size: 10px;
                font-weight: 700;
                padding: 9px 6px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #EFEFED;
                border: none;
            }
            """
        )

    def centrar_en_pantalla(self):
        screen_center = self.screen().availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(screen_center)
        self.move(geo.topLeft())

    def toggle_sidebar(self):
        # Muestra u oculta la barra lateral al instante de manera limpia
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # Métodos para permitir arrastrar la ventana sin bordes desde la barra superior (topbar)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPartenon()
    window.show()
    sys.exit(app.exec())