# Informe de Laboratorio 1: Prototipo Funcional — Sistema Atenea

**Asignación:** Desarrollo de Arquitectura Modular y Persistencia de Datos  
**Fecha de Entrega:** 15 de Noviembre de 2026  
**Proyecto:** Sistema Atenea (Gestión Académica y de Tutorías)  

---

## 1. Resumen Ejecutivo
El presente informe detalla la implementación y estructuración del Prototipo 1 del **Sistema Atenea**, una plataforma de gestión académica enfocada en automatizar el control de pupilos, la persistencia de datos relacionales y la seguridad de acceso mediante interfaces gráficas modernas en Python (PySide6). El desarrollo se ejecutó bajo una arquitectura estrictamente modular para garantizar la colaboración simultánea del equipo sin conflictos de integración.

---

## 2. Distribución y Roles del Equipo de Trabajo
Para garantizar la escalabilidad y el desacoplamiento del software, el desarrollo se dividió en los siguientes módulos especializados:

* **Antonio (Coordinador / Base de Datos):** Diseño y despliegue del esquema relacional en SQLite (`database/`), gestión del punto de entrada principal (`main.py`) y redacción de la documentación técnica (`docs/`).
* **Gabriel (Frontend / UI):** Maquetación y diseño de interfaces gráficas modernas y flotantes con PySide6 sin marcos nativos del sistema operativo (`ui/ventana_login.py` y `ui/ventana_partenon.py`).
* **Pablo (Controladores y Lógica):** Desarrollo de los controladores de eventos, gestión de rutas de navegación, validaciones de formularios y control de errores con bloques estructurados (`controllers/`).
* **Samuel (Seguridad):** Implementación del módulo criptográfico unidireccional con SHA-256 y HMAC para la autenticación segura de credenciales de acceso (`security/auth_manager.py`).
* **Fredy (Analítica y Procesamiento):** Programación del script de analítica con Pandas y Matplotlib para la generación de gráficos estadísticos conectados a la base de datos (`analytics/graficos_progreso.py`).

---

## 3. Arquitectura del Sistema
El proyecto se organiza en directorios independientes orientados a responsabilidades únicas:

```text
sistema_atenea/
├── main.py                     # Orquestador del flujo de la aplicación
├── requirements.txt            # Dependencias externas del entorno
├── README.md                   # Documentación principal del repositorio
├── sistema_atenea.db           # Base de datos local SQLite (creada en ejecución)
│
├── database/                   # Persistencia relacional (SQLite)
├── ui/                         # Interfaces gráficas con PySide6
├── controllers/                # Lógica de negocio, validaciones y navegación
├── security/                   # Criptografía, hashes y autenticación SHA-256
├── analytics/                  # Procesamiento de datos y gráficos estadísticos
└── docs/                       # Manuales y reportes técnicos
```

---

## 4. Pruebas y Resultados del Prototipo 1
1. **Autenticación:** El sistema valida de manera cifrada las credenciales del usuario comparando hashes SHA-256, previniendo ataques de temporización (*timing attacks*).
2. **Persistencia:** Se registró satisfactoriamente información de prueba (carnet, nombre, carrera y ciclo), la cual se almacena de forma local en `sistema_atenea.db` y se actualiza dinámicamente en la tabla de la interfaz gráfica de *El Partenón*.
3. **Analítica:** El módulo de Fredy procesa con éxito los registros mediante Pandas y exporta los gráficos estadísticos correspondientes.