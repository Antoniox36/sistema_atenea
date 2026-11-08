"""
Módulo de Seguridad y Autenticación - Sistema Atenea
===================================================
Este módulo se encarga de la seguridad y criptografía del sistema:
- Generación de resúmenes criptográficos unidireccionales (hashing) con SHA-256.
- Verificación segura de credenciales sin almacenar contraseñas en texto plano.
"""

import hashlib
import hmac

# Diccionario de credenciales autorizadas del sistema.
# Las contraseñas se almacenan únicamente como hashes SHA-256 (nunca en texto plano).
# Ejemplo: el hash de '1234' es '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
USUARIOS_AUTORIZADOS: dict[str, str] = {
    "admin": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",
    "tutor": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # hash de 'admin'
}


def hashear_contrasena(contrasena: str) -> str:
    """
    Aplica un algoritmo criptográfico unidireccional SHA-256 a una contraseña
    en texto plano y retorna su representación hexadecimal (hash).

    Args:
        contrasena (str): La contraseña en texto plano.

    Returns:
        str: Cadena hexadecimal de 64 caracteres correspondiente al resumen SHA-256.
             Retorna cadena vacía si la contraseña es nula o inválida.
    """
    if not contrasena or not isinstance(contrasena, str):
        return ""

    # Codificar la cadena a bytes en UTF-8 y generar el hash SHA-256
    bytes_contrasena = contrasena.encode("utf-8")
    hash_obj = hashlib.sha256(bytes_contrasena)
    return hash_obj.hexdigest()


# Alias en inglés para compatibilidad
hash_password = hashear_contrasena


def verificar_credenciales(usuario: str, contrasena: str) -> bool:
    """
    Verifica si las credenciales ingresadas son válidas.
    
    Genera el hash de la contraseña recibida y la compara de forma segura
    con el hash de referencia registrado para el usuario.

    Args:
        usuario (str): Nombre de usuario ingresado.
        contrasena (str): Contraseña en texto plano ingresada en el login.

    Returns:
        bool: True si el usuario existe y el hash de la contraseña coincide; False en caso contrario.
    """
    if not usuario or not contrasena:
        return False

    usuario_limpio = usuario.strip()
    if usuario_limpio not in USUARIOS_AUTORIZADOS:
        return False

    hash_esperado = USUARIOS_AUTORIZADOS[usuario_limpio]
    hash_calculado = hashear_contrasena(contrasena.strip())

    # Comparación segura contra ataques de temporización (timing attacks)
    return hmac.compare_digest(hash_esperado, hash_calculado)


# Alias alternativos para facilitar la integración por parte de otros módulos
verificar_login = verificar_credenciales
check_credentials = verificar_credenciales


if __name__ == "__main__":
    # Pruebas unitarias directas del módulo
    print("=" * 60)
    print("Prueba del Módulo de Seguridad (security/auth_manager.py)")
    print("=" * 60)

    # 1. Prueba de hashing
    clave_prueba = "1234"
    hash_prueba = hashear_contrasena(clave_prueba)
    print(f"Contraseña original : '{clave_prueba}'")
    print(f"Hash SHA-256        : {hash_prueba}")
    assert len(hash_prueba) == 64, "El hash SHA-256 debe tener 64 caracteres"

    # 2. Prueba de verificación exitosa
    acceso_valido = verificar_credenciales("admin", "1234")
    print(f"\nIntento de login con credenciales correctas ('admin', '1234'): {acceso_valido}")
    assert acceso_valido is True, "Las credenciales correctas deberían retornar True"

    # 3. Prueba de contraseña errónea
    acceso_invalido = verificar_credenciales("admin", "clave_incorrecta")
    print(f"Intento de login con contraseña incorrecta ('admin', 'clave_incorrecta'): {acceso_invalido}")
    assert acceso_invalido is False, "Una contraseña incorrecta debe retornar False"

    # 4. Prueba de usuario inexistente
    acceso_no_usuario = verificar_credenciales("usuario_inexistente", "1234")
    print(f"Intento de login con usuario no registrado: {acceso_no_usuario}")
    assert acceso_no_usuario is False, "Un usuario inexistente debe retornar False"

    print("\n[OK] Todas las pruebas de seguridad pasaron correctamente.")
