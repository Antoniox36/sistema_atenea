# Sistema Atenea 🏛️

<div align="center">

**Sistema Académico y de Gestión de Tutorías**  
*«El conocimiento construye el futuro»*

[![Estado del Prototipo](https://img.shields.io/badge/Estado-Prototipo%201%20(Activo)-blue?style=for-the-badge&logo=git&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

</div>

---

## 📌 Descripción General del Proyecto

**Sistema Atenea** es una solución de software de escritorio modular diseñada para optimizar y automatizar el registro, la administración y el control de pupilos (estudiantes) en entornos académicos y de tutoría. 

Desarrollado bajo una arquitectura limpia y desacoplada en **Python**, este **Prototipo 1** integra de manera armónica bases de datos locales relacionales, interfaces gráficas modernas y flotantes sin marcos nativos, validaciones estrictas de datos, un robusto sistema de autenticación cifrada mediante *SHA-256*, y un módulo analítico integrado con *Pandas* y *Matplotlib* para la generación de estadísticas institucionales.

> ⚠️ **Nota del Prototipo:** Este repositorio corresponde a la **Fase de Prototipo 1** (entrega programada para el 15 de noviembre de 2026). Las funcionalidades principales de persistencia local, seguridad en accesos, interfaces visuales y reportes estadísticos ya se encuentran totalmente operativas y probadas.

---

## 👥 Estructura del Equipo y División de Módulos

Para garantizar un control de versiones fluido y evitar conflictos de integración en Git, el desarrollo se ha estructurado estrictamente por responsabilidades modulares:

| Integrante | Módulo / Capas | Responsabilidad Principal |
| :--- | :--- | :--- |
| **Antonio** *(Coordinador)* | `database/`, `docs/`, `main.py` | Configuración y esquema relacional en SQLite, orquestación del flujo principal y documentación técnica. |
| **Gabriel** | `ui/` | Maquetación Frontend, diseño de ventanas flotantes modernas (`FramelessWindowHint`) y barras de navegación en PySide6. |
| **Pablo** | `controllers/` | Controladores de eventos, lógica de navegación entre pantallas, integración de datos y validadores estrictos. |
| **Samuel** | `security/` | Módulo de criptografía, hashing unidireccional con SHA-256 y protección contra ataques de temporización (`hmac`). |
| **Fredy** | `analytics/` | Procesamiento de datos estadísticos con Pandas y renderizado de gráficos vectoriales mediante Matplotlib. |

---

## 📂 Arquitectura del Repositorio

La disposición de los directorios sigue un estándar riguroso de separación de incumbencias:

```text
sistema_atenea/
├── main.py                     # Punto de entrada y orquestador global del sistema
├── requirements.txt            # Dependencias externas del entorno virtual
├── README.md                   # Documentación oficial y carta de presentación
├── sistema_atenea.db           # Base de datos local SQLite (generada automáticamente)
│
├── database/                   # CAPA DE DATOS (Antonio)
│   ├── __init__.py
│   ├── conexion.py             # Conexión y creación de tablas relacionales
│   └── crud_pupilos.py         # Sentencias SQL para inserción y consultas
│
├── ui/                         # CAPA DE INTERFAZ GRÁFICA (Gabriel)
│   ├── __init__.py
│   ├── ventana_login.py        # Pantalla de acceso institucional corporativa
│   └── ventana_partenon.py     # Panel de administración principal (El Partenón)
│
├── controllers/                # CAPA DE CONTROLADORES Y LÓGICA (Pablo)
│   ├── __init__.py
│   ├── controlador_login.py    # Gestión de eventos y autenticación del acceso
│   ├── controlador_main.py     # Puente de datos entre la tabla visual y SQLite
│   └── validaciones.py         # Filtrado de errores y tipos de datos (bloque try/except)
│
├── security/                   # CAPA DE SEGURIDAD (Samuel)
│   ├── __init__.py
│   └── auth_manager.py         # Cifrado SHA-256, HMAC y verificación de credenciales
│
├── analytics/                  # CAPA ANALÍTICA Y REPORTES (Fredy)
│   ├── __init__.py
│   └── graficos_progreso.py    # Procesamiento con Pandas y gráficos de Matplotlib
│
└── docs/                       # RECURSOS Y DOCUMENTACIÓN (Antonio)
    ├── informe_laboratorio1.md # Reporte técnico del prototipo
    └── manual_usuario.md       # Guía de uso rápido para el usuario final
```

---

## ⚙️ Guía de Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/sistema_atenea.git
cd sistema_atenea
```

### 2. Crear y activar un entorno virtual
* **En Windows (CMD / PowerShell):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **En macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias del proyecto
```bash
pip install -r requirements.txt
```

---

## 🚀 Guía de Ejecución

### A. Iniciar la aplicación completa (Sistema de Login + Panel de Administración)
Ejecuta el orquestador principal desde la raíz del proyecto:
```bash
python main.py
```

* **Credenciales de Acceso Autorizadas (Protegidas con SHA-256):**
  * **Usuario 1:** `admin` | **Contraseña:** `1234`
  * **Usuario 2:** `tutor` | **Contraseña:** `admin`

Una vez autenticado con éxito, se abrirá de forma automática la interfaz principal de administración (**El Partenón**), donde podrás registrar pupilos en tiempo real y ver su sincronización directa con la base de datos local SQLite.

### B. Ejecutar el módulo analítico independiente
Para generar estadísticas visuales de los estudiantes registrados (por carrera o ciclo académico) utilizando Pandas y Matplotlib, ejecuta el script de analítica desde la terminal:

* **Ver gráfico interactivo en ventana flotante (agrupado por carrera):**
  ```bash
  python analytics/graficos_progreso.py --campo carrera --mostrar
  ```
* **Ver gráfico interactivo agrupado por ciclo:**
  ```bash
  python analytics/graficos_progreso.py --campo ciclo --mostrar
  ```
* *Nota:* Si ejecutas el script sin la bandera `--mostrar`, este compilará y guardará automáticamente un reporte gráfico optimizado (`reporte_pupilos.png`) dentro de la carpeta `analytics/`.

---
<div align="center">
  <small>Desarrollado con dedicación por el equipo de ingeniería para la entrega del Prototipo 1 — Noviembre 2026.</small>
</div>