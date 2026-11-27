"""
Gestión de Materias, Tutores y Ágoras (círculos de tutoría) en MySQL.
"""

from datetime import date
from mysql.connector import Error
from database.conexion import conectar_bd


def obtener_materias() -> list[dict]:
    """Lista todas las materias disponibles para tutoría."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_materia, codigo, nombre, area FROM materias ORDER BY nombre")
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener materias: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_tutores() -> list[dict]:
    """Lista todos los tutores registrados."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_tutor, id_usuario, codigo_tutor, nombre, especialidad, correo FROM tutores ORDER BY nombre"
        )
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener tutores: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_tutor_por_usuario(id_usuario: int) -> dict | None:
    """Obtiene el perfil del tutor vinculado al id_usuario que inició sesión."""
    conexion = conectar_bd()
    if not conexion:
        return None

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_tutor, id_usuario, codigo_tutor, nombre, especialidad, correo FROM tutores WHERE id_usuario = %s",
            (id_usuario,),
        )
        return cursor.fetchone()
    except Error as e:
        print(f"[DB ERROR] Error al obtener tutor por usuario: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def crear_agora(nombre_agora: str, id_tutor: int, id_materia: int, horario: str, cupo_maximo: int = 30) -> bool:
    """Crea un nuevo círculo de tutoría (Ágora)."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO agoras (nombre_agora, id_tutor, id_materia, horario, cupo_maximo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (nombre_agora, id_tutor, id_materia, horario, cupo_maximo))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al crear Ágora: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_agoras() -> list[dict]:
    """Retorna todas las Ágoras activas con el nombre del tutor, materia y total de inscritos."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT
                a.id_agora,
                a.nombre_agora,
                t.nombre AS tutor,
                m.codigo AS codigo_materia,
                m.nombre AS materia,
                a.horario,
                a.cupo_maximo,
                COUNT(ia.id_pupilo) AS total_pupilos
            FROM agoras a
            INNER JOIN tutores t ON a.id_tutor = t.id_tutor
            INNER JOIN materias m ON a.id_materia = m.id_materia
            LEFT JOIN inscripciones_agora ia ON a.id_agora = ia.id_agora
            WHERE a.activa = 1
            GROUP BY a.id_agora, a.nombre_agora, t.nombre, m.codigo, m.nombre, a.horario, a.cupo_maximo
            ORDER BY a.id_agora ASC
        """
        cursor.execute(consulta)
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener Ágoras: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def inscribir_pupilo_en_agora(id_agora: int, id_pupilo: int) -> bool:
    """Asigna un pupilo a un Ágora específica."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO inscripciones_agora (id_agora, id_pupilo, fecha_inscripcion)
            VALUES (%s, %s, %s)
        """
        cursor.execute(consulta, (id_agora, id_pupilo, date.today()))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al inscribir pupilo en Ágora: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_pupilos_de_agora(id_agora: int) -> list[dict]:
    """Lista los pupilos inscritos en un Ágora determinada."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT p.id_pupilo, p.carnet, p.nombre, p.carrera, p.ciclo
            FROM inscripciones_agora ia
            INNER JOIN pupilos p ON ia.id_pupilo = p.id_pupilo
            WHERE ia.id_agora = %s
            ORDER BY p.nombre ASC
        """
        cursor.execute(consulta, (id_agora,))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener pupilos del Ágora: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()