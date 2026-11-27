"""
Gestión de Desafíos (Tareas), Buzones de Entrega y Entregas de Pupilos en MySQL.
"""

from mysql.connector import Error
from database.conexion import conectar_bd


def crear_desafio(id_agora: int, titulo: str, descripcion: str, fecha_limite: str, buzon_abierto: bool = True) -> bool:
    """Permite al tutor asignar una nueva tarea/desafío y habilitar su buzón."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO desafios (id_agora, titulo, descripcion, fecha_limite, buzon_abierto)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (id_agora, titulo, descripcion, fecha_limite, 1 if buzon_abierto else 0))
        conexion.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Error al crear desafío: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def cambiar_estado_buzon(id_desafio: int, abierto: bool) -> bool:
    """Habilita (True) o cierra (False) el buzón de entregas de un desafío."""
    conexion = conectar_bd()
    if not conexion:
        return False

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE desafios SET buzon_abierto = %s WHERE id_desafio = %s",
            (1 if abierto else 0, id_desafio),
        )
        conexion.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"[DB ERROR] Error al cambiar estado del buzón: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_desafios_por_agora(id_agora: int | None = None) -> list[dict]:
    """Lista los desafíos; si id_agora es None, lista todos los desafíos registrados."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        if id_agora is not None:
            consulta = """
                SELECT d.id_desafio, d.id_agora, a.nombre_agora, d.titulo, d.descripcion,
                       d.fecha_limite, d.buzon_abierto
                FROM desafios d
                INNER JOIN agoras a ON d.id_agora = a.id_agora
                WHERE d.id_agora = %s
                ORDER BY d.fecha_limite DESC
            """
            cursor.execute(consulta, (id_agora,))
        else:
            consulta = """
                SELECT d.id_desafio, d.id_agora, a.nombre_agora, d.titulo, d.descripcion,
                       d.fecha_limite, d.buzon_abierto
                FROM desafios d
                INNER JOIN agoras a ON d.id_agora = a.id_agora
                ORDER BY d.fecha_limite DESC
            """
            cursor.execute(consulta)
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener desafíos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_desafios_pupilo(id_pupilo: int) -> list[dict]:
    """Lista los desafíos asignados a las Ágoras donde el pupilo está inscrito, junto con el estado de su entrega."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT
                d.id_desafio,
                a.nombre_agora,
                m.nombre AS materia,
                d.titulo,
                d.descripcion,
                d.fecha_limite,
                d.buzon_abierto,
                ed.id_entrega,
                ed.fecha_entrega,
                ed.calificacion,
                ed.retroalimentacion
            FROM inscripciones_agora ia
            INNER JOIN agoras a ON ia.id_agora = a.id_agora
            INNER JOIN materias m ON a.id_materia = m.id_materia
            INNER JOIN desafios d ON d.id_agora = a.id_agora
            LEFT JOIN entregas_desafios ed
                ON ed.id_desafio = d.id_desafio AND ed.id_pupilo = %s
            WHERE ia.id_pupilo = %s
            ORDER BY d.fecha_limite DESC
        """
        cursor.execute(consulta, (id_pupilo, id_pupilo))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener desafíos del pupilo: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def enviar_entrega_buzon(id_desafio: int, id_pupilo: int, contenido: str, enlace_recurso: str = "") -> tuple[bool, str]:
    """
    Permite al pupilo subir o actualizar su entrega si el buzón del desafío está abierto.
    """
    conexion = conectar_bd()
    if not conexion:
        return False, "Sin conexión con la base de datos MySQL."

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT buzon_abierto FROM desafios WHERE id_desafio = %s", (id_desafio,))
        desafio = cursor.fetchone()
        if not desafio:
            return False, "El desafío seleccionado no existe."
        if not desafio["buzon_abierto"]:
            return False, "El buzón para este desafío se encuentra cerrado por el tutor."

        consulta = """
            INSERT INTO entregas_desafios (id_desafio, id_pupilo, contenido_entrega, enlace_recurso)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                contenido_entrega = VALUES(contenido_entrega),
                enlace_recurso = VALUES(enlace_recurso),
                fecha_entrega = CURRENT_TIMESTAMP
        """
        cursor.execute(consulta, (id_desafio, id_pupilo, contenido, enlace_recurso or None))
        conexion.commit()
        return True, "Entrega enviada correctamente al buzón."
    except Error as e:
        print(f"[DB ERROR] Error al enviar entrega al buzón: {e}")
        return False, f"Error de base de datos: {e}"
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def obtener_entregas_de_desafio(id_desafio: int) -> list[dict]:
    """Permite al tutor revisar todas las entregas recibidas en el buzón de un desafío."""
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT
                ed.id_entrega,
                p.carnet,
                p.nombre AS pupilo,
                p.carrera,
                ed.contenido_entrega,
                ed.enlace_recurso,
                ed.fecha_entrega,
                ed.calificacion,
                ed.retroalimentacion
            FROM entregas_desafios ed
            INNER JOIN pupilos p ON ed.id_pupilo = p.id_pupilo
            WHERE ed.id_desafio = %s
            ORDER BY ed.fecha_entrega ASC
        """
        cursor.execute(consulta, (id_desafio,))
        return cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] Error al obtener entregas del desafío: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conexion.close()