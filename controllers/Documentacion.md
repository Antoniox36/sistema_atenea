# 🏛️ Documentación del Sistema Partenón

Este documento describe la estructura y el funcionamiento de los controladores y validaciones principales de la aplicación de escritorio "Partenón", desarrollada con **PySide6** y **SQLite3**.

---

## 📂 1. Módulo: `controlador.login.py`
Este archivo gestiona la ventana de inicio de sesión de la aplicación. Se encarga de capturar las credenciales, validarlas de forma segura y dar paso al menú principal si los datos son correctos.

### 🔹 Clase: `ControladorLogin`
Clase principal que enlaza la interfaz gráfica del Login con la lógica de autenticación.

**Métodos principales:**
* `__init__(self, ventana_login)`: Inicializa el controlador, enlaza el botón "Ingresar" y configura la tecla `Enter` para que envíe los datos desde los campos de texto.
* `procesar_login(self)`: Extrae el texto de los campos `usuario` y `contrasena`. Verifica que no estén vacíos y llama a `verificar_credenciales()`. Si falla, muestra un mensaje de error visual (`QMessageBox`) y limpia el campo de contraseña.
* `iniciar_sesion(self)`: Si la autenticación es exitosa, este método instancia y muestra la `VentanaPartenon` (menú principal), inicializa su respectivo controlador y cierra la ventana de login actual.

> **💡 Nota de seguridad:** La validación se realiza a través de `verificar_credenciales`, que procesa la contraseña con SHA-256 y HMAC para evitar exponer texto plano.

---

## 📂 2. Módulo: `controlador_main.py`
Este archivo controla la ventana principal de la aplicación, donde se registran los pupilos (estudiantes) y se visualizan en una tabla de datos.

### 🔹 Clase: `ControladorMain`
Maneja los eventos de la interfaz principal tras un inicio de sesión exitoso.

**Métodos principales:**
* `__init__(self, ventana)`: Configura los eventos de los botones (como "Registrar Pupilo"), permite usar la tecla `Enter` en el último campo (ciclo) para registrar, y carga automáticamente la tabla de alumnos al abrir la ventana.
* `procesar_registro(self)`: 
  1. Captura los datos ingresados: `carnet`, `nombre`, `carrera` y `ciclo`.
  2. Llama a `validar_datos_pupilo()` para verificar formatos.
  3. Si es válido, invoca `registrar_pupilo()` para insertarlo en la base de datos (SQLite3).
  4. Muestra alertas de éxito o error (ej. si el carnet ya existe, por ser `UNIQUE`).
  5. Limpia los campos y actualiza la tabla.
* `refrescar_tabla(self)`: Consulta la base de datos usando `obtener_pupilos()` y repuebla el widget `tabla_pupilos` de PySide6, insertando fila por fila los datos actualizados.

---

## 📂 3. Módulo: `validaciones.py`
Un módulo independiente de la interfaz gráfica que contiene la lógica de negocio pura para validar la entrada de datos.

### 🔹 Funciones:
* `validar_datos_pupilo(carnet, nombre, carrera, ciclo_texto)`:
  * **Propósito:** Evitar que datos corruptos, incompletos o mal formateados lleguen a la base de datos.
  * **Validaciones que realiza:**
    1. **Campos vacíos:** Lanza un error si algún string está vacío.
    2. **Tipo de dato:** Intenta convertir `ciclo_texto` a un número entero (`int`).
  * **Retornos:** Devuelve una tupla de 3 valores: `(Booleano de éxito, Mensaje de estado, Valor numérico del ciclo)`.
  * **Manejo de errores:** Captura excepciones de tipo `ValueError`. Si el usuario escribió letras en el campo ciclo (lo que causa un `invalid literal for int()`), devuelve un mensaje amigable indicando que solo se permiten números.