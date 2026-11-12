# Documentación de las ventanas de Atenea

Este documento describe las ventanas de interfaz gráfica de **Atenea**:
**Ingreso (Login)** y **El Partenón**. La interfaz está implementada con
PySide6 y separa la presentación de las operaciones mediante controladores.

## 1. Flujo entre ventanas

1. `main.py` crea y muestra `VentanaLogin`.
2. `ControladorLogin` conecta el botón **Ingresar** y la tecla Enter de los
   campos de usuario y contraseña con el proceso de autenticación.
3. Si las credenciales son válidas, se crea `VentanaPartenon`, se conecta su
   `ControladorMain`, se muestra la ventana principal y se cierra el login.
4. Si la autenticación falla o falta algún campo, se muestra un aviso. El campo
   de contraseña se limpia y recibe el foco.

## 2. Ventana de ingreso (Login)

**Implementación:** `ui/ventana_login.py` (`VentanaLogin`); **controlador:**
`controllers/controlador_login.py` (`ControladorLogin`).

### Propósito

Solicitar las credenciales antes de permitir el acceso al panel principal.

### Presentación y componentes

- Título de ventana: **Atenea | Ingreso**.
- Tamaño fijo: **760 × 440 píxeles**; se centra en la pantalla.
- Ventana sin bordes nativos, con un botón de cierre propio.
- Panel de marca con el nombre Atenea y el mensaje institucional.
- Formulario con:
  - **Usuario** (`usuario`), con botón para borrar el texto.
  - **Contraseña** (`contrasena`), con los caracteres ocultos.
  - Botón **Ingresar** (`boton_ingresar`).

### Interacciones

- El botón **Ingresar** inicia la validación.
- Enter desde cualquiera de los dos campos también intenta iniciar sesión.
- Los campos vacíos generan un aviso y no continúan con la autenticación.
- Las credenciales se verifican mediante `verificar_credenciales`, definido
  en `security/auth_manager.py`.
- Si la verificación falla, se informa que las credenciales son incorrectas.
- En los errores de acceso, se limpia la contraseña y se devuelve el foco a ese
  campo.
- El botón **×** cierra la ventana.

## 3. Ventana principal (El Partenón)

**Implementación:** `ui/ventana_partenon.py` (`VentanaPartenon`); **controlador:**
`controllers/controlador_main.py` (`ControladorMain`).

### Propósito

Mostrar el registro de pupilos y permitir agregar registros a la base de datos.

### Presentación y componentes

- Título de ventana: **Atenea | El Partenón**.
- Tamaño inicial: **1280 × 800 píxeles**; tamaño mínimo: **980 × 650**.
- Se centra en la pantalla y utiliza una ventana personalizada sin marco nativo.
- La barra superior incluye el botón **Menú**, el título de la sección y los
  controles para minimizar, maximizar/restaurar y cerrar.
- El área de trabajo se divide en:
  - **Datos del pupilo**, con los campos Carnet, Nombre, Carrera y Ciclo y el
    botón **Registrar Pupilo**.
  - **Pupilos registrados**, una tabla de solo lectura con las columnas Carnet,
    Nombre, Carrera y Ciclo. Se puede seleccionar una fila a la vez.
- La barra lateral contiene la marca Atenea y la navegación del módulo.
  Empieza **oculta** y el botón **Menú** permite mostrarla u ocultarla.

### Registro y actualización de la tabla

Al crearse el controlador principal, se carga la lista existente con
`obtener_pupilos`. El botón **Registrar Pupilo** y Enter en el campo Ciclo
ejecutan el mismo proceso:

1. Se leen y recortan los valores del formulario.
2. `validar_datos_pupilo` comprueba los datos y convierte Ciclo a entero.
3. Si los datos no son válidos, se muestra un aviso con el motivo.
4. Si son válidos, `registrar_pupilo` intenta guardar el registro.
5. Si el guardado tiene éxito, se confirma la operación, se limpian los campos,
   se devuelve el foco a Carnet y se actualiza la tabla.
6. Si el guardado falla, se muestra un error que indica revisar si el carnet ya
   está registrado.

### Controles de ventana

- **─** minimiza la ventana.
- **□** alterna entre maximizada y tamaño normal.
- **×** cierra la ventana.
- Al no tener marco nativo, el usuario puede arrastrar la ventana desde su
  superficie.

## 4. Archivos relacionados

- `main.py`: crea y muestra la ventana de ingreso.
- `ui/ventana_login.py`: estructura y apariencia del login.
- `controllers/controlador_login.py`: autenticación y transición al Partenón.
- `ui/ventana_partenon.py`: estructura y apariencia del panel principal.
- `controllers/controlador_main.py`: carga, validación y registro de pupilos.
- `controllers/validaciones.py`: validación de los datos del pupilo.
- `database/crud_pupilos.py`: lectura y registro de pupilos.
- `security/auth_manager.py`: verificación de credenciales.
