"""
Gestión de Asistencias por sesión de tutoría y Edictos (Comunicados) en MySQL.
"""

from mysql.connector import Error
from database.conexion import conectar_bd


def registrar_asistencia(id_agora: int, id_pupilo: int, fecha_sesion: str, estado: str, observacion: str = "") -> bool:
    """
    Registra o actualiza la asistencia de un pupilo en una fecha de sesión específica.
    Estados válidos: 'Presente', 'Ausente', 'Tardanza'.
    """
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO asistencias (id_agora, id_pupilo, fecha_sesion, estado, observacion)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                estado = VALUES(estado),
                observacion = VALUES(observacion)
        """
        cursor.execute(consulta, (id_agora, id_pupilo, fecha_sesion, estado, observacion or None))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al registrar asistencia: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_asistencias_agora(id_agora: int) -> list[dict]:
    """Obtiene el historial de asistencias de un Ágora."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT
                ast.id_asistencia,
                ast.fecha_sesion,
                p.carnet,
                p.nombre AS pupilo,
                p.carrera,
                ast.estado,
                ast.observacion
            FROM asistencias ast
            INNER JOIN pupilos p ON ast.id_pupilo = p.id_pupilo
            WHERE ast.id_agora = %s
            ORDER BY ast.fecha_sesion DESC, p.nombre ASC
        """
        cursor.execute(consulta, (id_agora,))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener asistencias: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def publicar_edicto(id_agora: int, id_tutor: int, titulo: str, mensaje: str) -> bool:
    """Permite al tutor publicar un comunicado (Edicto) para su Ágora."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO edictos (id_agora, id_tutor, titulo, mensaje)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(consulta, (id_agora, id_tutor, titulo, mensaje))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al publicar edicto: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_edictos_por_agora(id_agora: int | None = None) -> list[dict]:
    """Lista los comunicados publicados; si id_agora es None, lista todos."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        if id_agora is not None:
            consulta = """
                SELECT e.id_edicto, a.nombre_agora, t.nombre AS tutor,
                       e.titulo, e.mensaje, e.fecha_publicacion
                FROM edictos e
                INNER JOIN agoras a ON e.id_agora = a.id_agora
                INNER JOIN tutores t ON e.id_tutor = t.id_tutor
                WHERE e.id_agora = %s
                ORDER BY e.fecha_publicacion DESC
            """
            cursor.execute(consulta, (id_agora,))
        else:
            consulta = """
                SELECT e.id_edicto, a.nombre_agora, t.nombre AS tutor,
                       e.titulo, e.mensaje, e.fecha_publicacion
                FROM edictos e
                INNER JOIN agoras a ON e.id_agora = a.id_agora
                INNER JOIN tutores t ON e.id_tutor = t.id_tutor
                ORDER BY e.fecha_publicacion DESC
            """
            cursor.execute(consulta)
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener edictos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_edictos_pupilo(id_pupilo: int) -> list[dict]:
    """Obtiene los comunicados de todas las Ágoras donde el pupilo está inscrito."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT
                e.id_edicto,
                a.nombre_agora,
                t.nombre AS tutor,
                e.titulo,
                e.mensaje,
                e.fecha_publicacion
            FROM inscripciones_agora ia
            INNER JOIN edictos e ON ia.id_agora = e.id_agora
            INNER JOIN agoras a ON e.id_agora = a.id_agora
            INNER JOIN tutores t ON e.id_tutor = t.id_tutor
            WHERE ia.id_pupilo = %s
            ORDER BY e.fecha_publicacion DESC
        """
        cursor.execute(consulta, (id_pupilo,))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener edictos del pupilo: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()