"""
Operaciones CRUD para los pupilos (estudiantes) y consulta de compañeros en MySQL.
"""

from mysql.connector import Error
from database.conexion import conectar_bd


def registrar_pupilo(carnet: str, nombre: str, carrera: str, ciclo: int, correo: str = "") -> bool:
    """Inserta un nuevo pupilo en la base de datos MySQL."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO pupilos (carnet, nombre, carrera, ciclo, correo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (carnet, nombre, carrera, ciclo, correo or None))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al registrar pupilo: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_pupilos() -> list[dict]:
    """Retorna todos los pupilos registrados como lista de diccionarios."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id_pupilo, id_usuario, carnet, nombre, carrera, ciclo, correo
            FROM pupilos
            ORDER BY id_pupilo ASC
        """
        cursor.execute(consulta)
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener pupilos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_pupilo_por_usuario(id_usuario: int) -> dict | None:
    """Obtiene el perfil del pupilo asociado a un id_usuario logueado."""
    conexion = conectar_bd()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id_pupilo, id_usuario, carnet, nombre, carrera, ciclo, correo
            FROM pupilos
            WHERE id_usuario = %s
        """
        cursor.execute(consulta, (id_usuario,))
        return cursor.fetchone()
    except Error as e:
        print(f"[DB ERROR] Error al buscar pupilo por usuario: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_companeros_pupilo(id_pupilo: int) -> list[dict]:
    """
    Retorna los compañeros inscritos en las mismas Ágoras que el pupilo indicado.
    """
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT DISTINCT
                p.carnet,
                p.nombre,
                p.carrera,
                p.ciclo,
                a.nombre_agora
            FROM inscripciones_agora ia_companero
            INNER JOIN pupilos p ON ia_companero.id_pupilo = p.id_pupilo
            INNER JOIN agoras a ON ia_companero.id_agora = a.id_agora
            WHERE ia_companero.id_agora IN (
                SELECT id_agora FROM inscripciones_agora WHERE id_pupilo = %s
            )
            AND p.id_pupilo <> %s
            ORDER BY a.nombre_agora, p.nombre
        """
        cursor.execute(consulta, (id_pupilo, id_pupilo))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener compañeros: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()