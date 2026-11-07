from PySide6.QtWidgets import QTableWidgetItem
from database.crud_pupilos import registrar_pupilo, obtener_pupilos
from controllers.validaciones import validar_datos_pupilo

class ControladorMain:
    def __init__(self, ventana):
        self.ventana = ventana
        
        # Enlazar el botón a la acción de procesar
        self.ventana.boton_registrar.clicked.connect(self.procesar_registro)
        
        # Ejecutar el refresco apenas se abre la ventana
        self.refrescar_tabla()

    def procesar_registro(self):
        # Extraer y limpiar los textos de la interfaz
        carnet = self.ventana.carnet.text().strip()
        nombre = self.ventana.nombre.text().strip()
        carrera = self.ventana.carrera.text().strip()
        ciclo_texto = self.ventana.ciclo.text().strip()

        # Validar los datos e intentar convertir el ciclo
        es_valido, mensaje_error, ciclo_num = validar_datos_pupilo(carnet, nombre, carrera, ciclo_texto)

        if not es_valido:
            print(f"Error de validación: {mensaje_error}")
            return

        # Invocar la función de base de datos para el guardado
        guardado_exitoso = registrar_pupilo(carnet, nombre, carrera, ciclo_num)
        
        if guardado_exitoso:
            print("Pupilo registrado exitosamente en la base de datos.")
            
            # Limpiar las cajas de texto
            self.ventana.carnet.clear()
            self.ventana.nombre.clear()
            self.ventana.carrera.clear()
            self.ventana.ciclo.clear()
            
            # Actualizar la tabla visual para reflejar el nuevo registro
            self.refrescar_tabla()
        else:
            print("Error: Falló el registro en la base de datos.")

    def refrescar_tabla(self):
        # Obtener la lista de diccionarios desde la base de datos
        pupilos = obtener_pupilos()
        
        # Reiniciar la cantidad de filas en la tabla visual
        self.ventana.tabla_pupilos.setRowCount(0)
        
        # Recorrer los datos e insertarlos fila por fila
        for fila_idx, pupilo in enumerate(pupilos):
            self.ventana.tabla_pupilos.insertRow(fila_idx)
            
            self.ventana.tabla_pupilos.setItem(fila_idx, 0, QTableWidgetItem(str(pupilo.get("carnet", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 1, QTableWidgetItem(str(pupilo.get("nombre", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 2, QTableWidgetItem(str(pupilo.get("carrera", ""))))
            self.ventana.tabla_pupilos.setItem(fila_idx, 3, QTableWidgetItem(str(pupilo.get("ciclo", ""))))