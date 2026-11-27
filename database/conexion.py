"""
Módulo de conexión centralizada a MySQL para el Sistema Atenea.
Lee las credenciales desde el archivo local .env para evitar exponer datos sensibles.
"""

import os
from pathlib import Path
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ_PROYECTO / ".env")


def conectar_bd():
    """
    Establece y retorna una conexión activa hacia el servidor MySQL.
    Retorna None si ocurre un error de red o credenciales.
    """
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME", "sistema_atenea"),
            user=os.getenv("DB_USER", "antonio"),
            password=os.getenv("DB_PASSWORD", "antonio1234"),
            charset="utf8mb4",
            connection_timeout=8,
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"[DB ERROR] No se pudo conectar a MySQL: {e}")
    return None


def verificar_conexion() -> tuple[bool, str]:
    """
    Comprueba la conectividad con MySQL y devuelve (exito, mensaje).
    Útil para diagnósticos al arrancar el sistema.
    """
    conexion = conectar_bd()
    if conexion:
        info = conexion.server_info
        conexion.close()
        return True, f"Conectado exitosamente a MySQL Server {info}"
    return False, "No se pudo establecer conexión con el servidor MySQL. Verifica Radmin VPN y tu archivo .env."


if __name__ == "__main__":
    ok, msg = verificar_conexion()
    print(msg)