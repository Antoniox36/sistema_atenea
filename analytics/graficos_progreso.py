
"""Genera estadísticas de pupilos registrados en SQLite."""

import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Ruta principal del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

# Importar función de la base de datos
from database.crud_pupilos import obtener_pupilos

# Colores del proyecto
AZUL_PROFUNDO = "#14243A"
DORADO = "#D7B45A"
BLANCO = "#F5F7FA"

# Ruta donde se guardará el gráfico
RUTA_REPORTE = (
    Path(__file__).resolve().parent / "reporte_pupilos.png"
)


def generar_grafico(campo="carrera", mostrar=False):

    # Validar campo seleccionado
    if campo not in ["carrera", "ciclo"]:
        raise ValueError(
            "El campo debe ser 'carrera' o 'ciclo'."
        )

    # Obtener pupilos desde SQLite
    datos = obtener_pupilos()

    # Convertir datos a DataFrame
    df = pd.DataFrame(datos)

    # Verificar si existen registros
    if df.empty:
        print("No hay pupilos registrados.")
        return None

    # Verificar columna
    if campo not in df.columns:
        print(f"No existe la columna: {campo}")
        print("Columnas disponibles:", list(df.columns))
        return None

    # Agrupar y contar pupilos
    conteo = (
        df[campo]
        .fillna("Sin especificar")
        .astype(str)
        .str.strip()
        .replace("", "Sin especificar")
        .value_counts()
    )

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Aplicar colores
    fig.patch.set_facecolor(AZUL_PROFUNDO)
    ax.set_facecolor(AZUL_PROFUNDO)

    # Crear gráfico de barras
    barras = ax.bar(
        conteo.index,
        conteo.values,
        color=DORADO,
        width=0.65
    )

    # Título
    ax.set_title(
        f"Distribución de pupilos por {campo}",
        fontsize=17,
        fontweight="bold",
        color=DORADO,
        pad=20
    )

    # Etiquetas
    ax.set_xlabel(
        campo.capitalize(),
        fontsize=12,
        color=BLANCO
    )

    ax.set_ylabel(
        "Cantidad de pupilos",
        fontsize=12,
        color=BLANCO
    )

    # Configurar ejes
    ax.tick_params(
        axis="x",
        colors=BLANCO,
        labelrotation=30
    )

    ax.tick_params(
        axis="y",
        colors=BLANCO
    )

    # Cuadrícula
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.2,
        color=BLANCO
    )

    ax.set_axisbelow(True)

    # Ocultar bordes
    for borde in ax.spines.values():
        borde.set_visible(False)

    # Mostrar cantidades sobre cada barra
    for barra in barras:
        altura = barra.get_height()

        ax.annotate(
            str(int(altura)),
            xy=(
                barra.get_x() + barra.get_width() / 2,
                altura
            ),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            color=BLANCO,
            fontweight="bold"
        )

    # Ajustar espacio superior
    ax.set_ylim(0, max(conteo.values) * 1.2 + 0.5)

    plt.tight_layout()

    # Guardar imagen
    plt.savefig(
        RUTA_REPORTE,
        dpi=200,
        bbox_inches="tight",
        facecolor=AZUL_PROFUNDO
    )

    print("Gráfico generado correctamente.")
    print(f"Guardado en: {RUTA_REPORTE}")

    # Mostrar gráfico opcionalmente
    if mostrar:
        plt.show()

    plt.close(fig)

    return RUTA_REPORTE


def main():

    parser = argparse.ArgumentParser(
        description="Estadísticas de pupilos"
    )

    parser.add_argument(
        "--campo",
        choices=["carrera", "ciclo"],
        default="carrera"
    )

    parser.add_argument(
        "--mostrar",
        action="store_true"
    )

    args = parser.parse_args()

    generar_grafico(
        campo=args.campo,
        mostrar=args.mostrar
    )


if __name__ == "__main__":
    main()
