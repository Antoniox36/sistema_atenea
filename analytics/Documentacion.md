
# Sistema Atenea - Módulo Analytics

## Descripción
El módulo Analytics permite analizar los datos de los
pupilos registrados en la base de datos SQLite y
generar gráficos estadísticos.

## Objetivo
Visualizar la distribución de pupilos por carrera
o ciclo mediante gráficos de barras.

## Librerías utilizadas
- **Pandas:** Organiza y procesa los datos.
- **Matplotlib:** Genera los gráficos estadísticos.
- **Argparse:** Permite utilizar argumentos en la terminal.
- **Sys:** Gestiona las rutas de importación.
- **Pathlib:** Administra las rutas de archivos.

## Funciones principales

### generar_grafico()
- Obtiene los pupilos desde SQLite.
- Convierte los registros en un DataFrame.
- Agrupa y cuenta los pupilos por carrera o ciclo.
- Genera un gráfico de barras.
- Guarda el gráfico como imagen PNG.

### main()
- Configura los argumentos del programa.
- Permite seleccionar carrera o ciclo.
- Ejecuta la función generar_grafico().

## Colores del proyecto
- Azul profundo: `#14243A`
- Dorado: `#D7B45A`
- Blanco: `#F5F7FA`

## Ejecución

Instalar dependencias:

```bash
pip install pandas matplotlib
```

Generar gráfico por carrera:

```bash
python -m analytics.graficos_progreso
```

Generar gráfico por ciclo:

```bash
python -m analytics.graficos_progreso --campo ciclo
```

Mostrar el gráfico:

```bash
python -m analytics.graficos_progreso --mostrar
```

## Resultado
El sistema genera el archivo `reporte_pupilos.png`
dentro de la carpeta `analytics`.

## Conclusión
Este módulo facilita la visualización y el análisis
estadístico de los pupilos registrados en el
Sistema Atenea.
