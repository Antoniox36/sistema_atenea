def validar_datos_pupilo(carnet, nombre, carrera, ciclo_texto):
    try:
        # Verificar que no existan campos vacíos
        if not carnet or not nombre or not carrera or not ciclo_texto:
            raise ValueError("Todos los campos son obligatorios y no pueden quedar vacíos.")
        
        # Intentar convertir el ciclo a número entero para la base de datos
        ciclo_num = int(ciclo_texto)
        
        return True, "Validación exitosa", ciclo_num
        
    except ValueError as e:
        # Atrapa tanto el error lanzado manualmente como el error de conversión de int()
        if "invalid literal for int()" in str(e):
            return False, "El campo 'ciclo' debe contener únicamente números.", None
        return False, str(e), None