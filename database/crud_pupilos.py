from database.conexion import conectar_bd

def registrar_pupilo(carnet, nombre, carrera, ciclo):
    # Inserta un nuevo estudiante en la base de datos
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """INSERT INTO pupilos (carnet, nombre, carrera, ciclo) 
                          VALUES (?, ?, ?, ?)"""
            valores = (carnet, nombre, carrera, ciclo)
            cursor.execute(consulta, valores)
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar pupilo: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_pupilos():
    # Extrae todos los estudiantes registrados y los retorna como lista de diccionarios
    conexion = conectar_bd()
    pupilos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT carnet, nombre, carrera, ciclo FROM pupilos")
            filas = cursor.fetchall()
            pupilos = [dict(fila) for fila in filas]
        except Exception as e:
            print(f"Error al obtener pupilos: {e}")
        finally:
            cursor.close()
            conexion.close()
    return pupilos