# SISTEMA ATENEA - MÓDULO DE SEGURIDAD Y CRIPTOGRAFÍA

* **Entrega:** Laboratorio 1 / Entrega 1
* **Capa:** Seguridad (`security/`)
* **Autor:** Responsable de Seguridad
* **Tecnología:** Python 3 (Librerías nativas: `hashlib`, `hmac`)

## 1. Objetivo del Módulo

El módulo `security` se encarga de proteger las credenciales del sistema, garantizando que ninguna clave o contraseña sea procesada o almacenada en texto plano. Implementa algoritmos de resumen criptográfico (hash) unidireccionales bajo estándares seguros de la industria.

## 2. Estructura de Archivos

```text
sistema_atenea/
  └── security/
      ├── __init__.py           -> Convierte la carpeta en paquete Python y expone las funciones principales.
      ├── auth_manager.py       -> Archivo principal con la lógica de cifrado y verificación de credenciales.
      └── documentacion.md      -> Este archivo descriptivo y manual técnico.
```

## 3. Funciones Implementadas (`auth_manager.py`)

### A) `hashear_contrasena(contrasena: str) -> str`
- **Descripción:** Toma una contraseña en texto plano y aplica el algoritmo criptográfico SHA-256 para transformarla en un resumen (hash) hexadecimal de 64 caracteres.
- **Proceso interno:**
  1. Codifica la cadena a bytes mediante UTF-8 (`.encode('utf-8')`).
  2. Pasa los bytes al algoritmo `hashlib.sha256()`.
  3. Obtiene y retorna la cadena hexadecimal resultante (`.hexdigest()`).
- **Alias incluido:** `hash_password(contrasena)`

### B) `verificar_credenciales(usuario: str, contrasena: str) -> bool`
- **Descripción:** Verifica las credenciales ingresadas por un usuario contra la base de usuarios autorizados del sistema.
- **Proceso interno:**
  1. Valida que el usuario y la contraseña no sean nulos o vacíos.
  2. Verifica si el usuario existe en el diccionario `USUARIOS_AUTORIZADOS`.
  3. Hashea la contraseña recibida con SHA-256.
  4. Utiliza `hmac.compare_digest` para comparar el hash calculado con el hash esperado. Esto evita ataques basados en tiempo (*timing attacks*).
  5. Retorna `True` si coinciden las credenciales, o `False` si fallan.
- **Alias incluidos:**
  - `verificar_login(usuario, contrasena)`
  - `check_credentials(usuario, contrasena)`

## 4. Usuarios Autorizados de Prueba

Las claves nunca se almacenan en texto plano. En su lugar, se guardan sus hashes:

- **Usuario:** `"admin"`
  - **Clave real:** `"1234"`
  - **Hash SHA-256 almacenado:**
    `03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4`

- **Usuario:** `"tutor"`
  - **Clave real:** `"admin"`
  - **Hash SHA-256 almacenado:**
    `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918`

## 5. Ejemplo de Integración (Para `controlador_login.py`)

Desde el controlador de Login (`controllers/controlador_login.py`), el responsable (Pablo) puede consumir este módulo de la siguiente manera:

```python
from security.auth_manager import verificar_credenciales

def procesar_login(self):
    usuario = self.ventana_login.usuario.text().strip()
    contrasena = self.ventana_login.contrasena.text().strip()

    if verificar_credenciales(usuario, contrasena):
        print("Acceso concedido.")
        self.iniciar_sesion()
    else:
        raise ValueError("Credenciales inválidas.")
```

## 6. Pruebas Unitarias

Para ejecutar las pruebas integradas y validar el correcto funcionamiento:

- **Comando en consola:**
  ```bash
  python security/auth_manager.py
  ```

- **Casos probados en el bloque:**
  - [OK] Hash de contraseña `'1234'` genera 64 caracteres SHA-256.
  - [OK] Intento con credenciales válidas (`'admin', '1234'`) -> Retorna `True`.
  - [OK] Intento con contraseña incorrecta -> Retorna `False`.
  - [OK] Intento con usuario no registrado -> Retorna `False`.