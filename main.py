from database.conexion import inicializar_bd
from database.crud_pupilos import obtener_pupilos

# Crear la base de datos y la tabla si no existen
inicializar_bd()

# Probar la lectura
print("Pupilos registrados:", obtener_pupilos())