import sqlite3

def conectar_bd():
    # Establece conexion a la base de datos local SQLite
    try:
        conexion = sqlite3.connect('sistema_atenea.db')
        conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a SQLite: {e}")
        return None

def inicializar_bd():
    # Crea la tabla pupilos si no existe al arrancar
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pupilos (
                    id_pupilo INTEGER PRIMARY KEY AUTOINCREMENT,
                    carnet TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    carrera TEXT NOT NULL,
                    ciclo INTEGER NOT NULL
                )
            """)
            conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conexion.close()

# Ejecuta la inicialización de la tabla automáticamente al importar el módulo
inicializar_bd()