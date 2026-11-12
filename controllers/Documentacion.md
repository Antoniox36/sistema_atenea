Documentación del Sistema

Esta documentación describe la lógica de los controladores principales y el módulo de validación para la aplicación de gestión de pupilos. La interfaz de usuario está construida utilizando PySide6.

1. Módulo: controlador.login.py

Este módulo gestiona la ventana de inicio de sesión de la aplicación. Se encarga de capturar las credenciales del usuario, validarlas y conceder o denegar el acceso al sistema principal.

Clase: ControladorLogin

Clase encargada de controlar la lógica de la vista de login.

Métodos:

__init__(self, ventana_login)

Descripción: Constructor de la clase. Inicializa la ventana de login y conecta las señales de la interfaz de usuario (clic en el botón de ingresar o presionar "Enter" en los campos de texto) con el método procesar_login.

Parámetros:

ventana_login: Instancia de la interfaz gráfica de la ventana de login.

procesar_login(self)

Descripción: Captura los textos de los campos usuario y contrasena. Realiza una validación básica para asegurar que no estén vacíos. Luego, llama a la función verificar_credenciales (utilizando SHA-256 + HMAC) para autenticar al usuario. Si las credenciales son correctas, llama a iniciar_sesion(); de lo contrario, muestra una ventana de advertencia (QMessageBox.warning) y limpia el campo de contraseña.

iniciar_sesion(self)

Descripción: Maneja la transición de la ventana de login a la ventana principal. Instancia VentanaPartenon y su controlador respectivo (ControladorMain). Finalmente, muestra la ventana principal y cierra la ventana de login.

2. Módulo: controlador_main.py

Este módulo contiene la lógica de la ventana principal de la aplicación, desde donde se registran y visualizan los "pupilos".

Clase: ControladorMain

Clase encargada de coordinar las interacciones de la ventana principal (Partenón), manejando el registro en la base de datos y la actualización de la tabla de visualización.

Métodos:

__init__(self, ventana)

Descripción: Constructor de la clase. Vincula los eventos de la interfaz (clic en "Registrar Pupilo" o presionar "Enter" en el campo de ciclo) con el método procesar_registro. También ejecuta refrescar_tabla() al inicio para cargar los datos existentes.

Parámetros:

ventana: Instancia de la interfaz gráfica principal.

procesar_registro(self)

Descripción: Recopila los datos de los campos de entrada (carnet, nombre, carrera, ciclo). Utiliza la función validar_datos_pupilo para verificar la integridad de la información.

Flujo:

Si los datos son inválidos, muestra un mensaje de advertencia y detiene la ejecución.

Si son válidos, intenta guardarlos en la base de datos mediante registrar_pupilo.

Si el registro es exitoso, muestra un mensaje de éxito, limpia los campos del formulario y actualiza la tabla.

Si falla (generalmente por un carnet duplicado), muestra un mensaje de error crítico.

refrescar_tabla(self)

Descripción: Consulta todos los registros de la base de datos mediante obtener_pupilos(). Limpia la tabla actual (setRowCount(0)) y la vuelve a poblar iterando sobre los resultados obtenidos, insertando el carnet, nombre, carrera y ciclo en sus respectivas columnas.

3. Módulo: validaciones.py

Este módulo centraliza las reglas de validación de datos antes de que interactúen con la base de datos o la lógica de negocio.

Función: validar_datos_pupilo

Firma: def validar_datos_pupilo(carnet, nombre, carrera, ciclo_texto):

Descripción: Valida los datos ingresados en el formulario de registro de un nuevo pupilo.

Reglas de validación:

Ningún campo puede estar vacío o ser nulo.

El campo ciclo_texto debe poder convertirse a un número entero (int).

Retorno: Devuelve una tupla de tres valores: (es_valido, mensaje, ciclo_num)

es_valido (bool): True si pasó todas las validaciones, False en caso contrario.

mensaje (str): Mensaje descriptivo del resultado (ej. "Validación exitosa" o el mensaje de error específico).

ciclo_num (int | None): El valor numérico del ciclo si la conversión fue exitosa; de lo contrario, None.