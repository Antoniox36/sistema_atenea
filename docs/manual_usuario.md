# Manual de Usuario — Sistema Atenea

**Versión:** 1.0 (Prototipo Funcional)  
**Fecha:** Noviembre de 2026  
**Sistema Operativo Compatible:** Windows, Linux, macOS  

---

## 1. Introducción
**Sistema Atenea** es una aplicación de escritorio diseñada para facilitar la administración, registro y control de pupilos dentro del entorno académico. Este manual detalla los pasos para poner en marcha el sistema y utilizar sus funciones principales.

---

## 2. Requisitos Previos y Entorno
Asegúrate de tener instalado **Python 3.10** o superior en tu equipo. Las librerías y dependencias necesarias están especificadas en el archivo `requirements.txt` de la raíz del proyecto.

---

## 3. Instalación y Configuración Inicial

1. **Clonar o descargar** el repositorio del proyecto en tu equipo local.
2. **Crear y activar un entorno virtual** en la carpeta raíz del proyecto:
   ```bash
   python -m venv venv
   
   # En Windows (CMD / PowerShell):
   venv\Scripts\activate
   
   # En Linux / macOS:
   source venv/bin/activate
   ```
3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Guía de Uso del Sistema

### A. Inicio de Sesión (Login Seguro)
* Ejecuta el orquestador principal desde la terminal:
  ```bash
  python main.py
  ```
* Se abrirá la ventana flotante de acceso de Atenea (sin bordes nativos).
* Ingresa con las credenciales institucionales autorizadas (protegidas por cifrado SHA-256):
  * **Usuario:** `admin`
  * **Contraseña:** `1234`
* Haz clic en el botón **Ingresar** para validar el acceso y abrir el panel principal.

### B. Panel Principal ("El Partenón") y Gestión de Pupilos
Una vez superada la autenticación, se desplegará el panel de control principal:
1. Localiza el formulario de **Datos del pupilo** en el costado izquierdo.
2. Completa los campos correspondientes:
   * **Carnet:** (Ej. `20240001`)
   * **Nombre:** (Nombre completo del estudiante)
   * **Carrera:** (Ej. `Ingeniería en Sistemas`)
   * **Ciclo:** (Número entero, Ej. `3`)
3. Haz clic en el botón **Registrar Pupilo**. La información se almacenará al instante en la base de datos local SQLite y se reflejará en tiempo real en la tabla de control general.

### C. Generación de Estadísticas y Analítica
Para ejecutar el módulo estadístico desarrollado para procesar la información de los pupilos:
* **Ver gráfico interactivo agrupado por carrera:**
  ```bash
  python analytics/graficos_progreso.py --campo carrera --mostrar
  ```
* **Ver gráfico interactivo agrupado por ciclo:**
  ```bash
  python analytics/graficos_progreso.py --campo ciclo --mostrar
  ```
* *Nota:* Si ejecutas el script sin la bandera `--mostrar`, este compilará y guardará automáticamente un reporte gráfico optimizado (`reporte_pupilos.png`) en la carpeta `analytics/`.