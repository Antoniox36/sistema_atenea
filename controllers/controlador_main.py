from PySide6.QtWidgets import QMessageBox, QTableWidgetItem

from database.crud_pupilos import registrar_pupilo, obtener_pupilos
from controllers.validaciones import validar_datos_pupilo


class ControladorMain:
    def __init__(self, ventana):
        self.ventana = ventana

        # Clic en "Registrar Pupilo"
        self.ventana.boton_registrar.clicked.connect(self.procesar_registro)

        # Enter en el último campo (ciclo) también registra
        self.ventana.ciclo.returnPressed.connect(self.procesar_registro)

        # Cargar la tabla apenas se abre la ventana
        self.refrescar_tabla()

    def procesar_registro(self):
        carnet = self.ventana.carnet.text().strip()
        nombre = self.ventana.nombre.text().strip()
        carrera = self.ventana.carrera.text().strip()
        ciclo_texto = self.ventana.ciclo.text().strip()

        # Validar datos y convertir el ciclo a entero
        es_valido, mensaje_error, ciclo_num = validar_datos_pupilo(
            carnet, nombre, carrera, ciclo_texto
        )

        if not es_valido:
            QMessageBox.warning(self.ventana, "Datos inválidos", mensaje_error)
            return

        guardado_exitoso = registrar_pupilo(carnet, nombre, carrera, ciclo_num)

        if guardado_exitoso:
            QMessageBox.information(
                self.ventana, "Registro exitoso", "Pupilo registrado correctamente."
            )

            self.ventana.carnet.clear()
            self.ventana.nombre.clear()
            self.ventana.carrera.clear()
            self.ventana.ciclo.clear()
            self.ventana.carnet.setFocus()

            self.refrescar_tabla()
        else:
            # Causa más probable: carnet duplicado (carnet es UNIQUE en la BD)
            QMessageBox.critical(
                self.ventana,
                "Error al registrar",
                "No se pudo guardar el pupilo. Verifica que el carnet no esté ya registrado.",
            )

    def refrescar_tabla(self):
        pupilos = obtener_pupilos()

        self.ventana.tabla_pupilos.setRowCount(0)

        for fila_idx, pupilo in enumerate(pupilos):
            self.ventana.tabla_pupilos.insertRow(fila_idx)

            self.ventana.tabla_pupilos.setItem(fila_idx, 0, QTableWidgetItem(str(pupilo.get("carnet", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 1, QTableWidgetItem(str(pupilo.get("nombre", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 2, QTableWidgetItem(str(pupilo.get("carrera", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 3, QTableWidgetItem(str(pupilo.get("ciclo", ""))))