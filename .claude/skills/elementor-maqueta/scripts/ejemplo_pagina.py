#!/usr/bin/env python3
"""Ejemplo ejecutable: una landing de tres secciones, una plantilla por sección.

Léelo antes de escribir tu propio guion — muestra el patrón completo (tema,
secciones, filas de tarjetas, efecto en widget html y validación) y evita
tanteo. Ejecútalo con:

    python3 ejemplo_pagina.py [carpeta_de_salida]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from elementor import (  # noqa: E402
    Plantilla, Tema, boton, contenedor, fila, html_personalizado, imagen,
    leer_efecto, marco, parrafo, px, seccion, titulo,
)

SALIDA = sys.argv[1] if len(sys.argv) > 1 else "."
AQUI = os.path.dirname(os.path.abspath(__file__))
EFECTOS = os.path.join(os.path.dirname(AQUI), "assets", "efectos")

# Un solo tema para todas las secciones: así la paleta no se dispersa.
tema = Tema(
    colores={
        "fondo": "#00133D",
        "texto": "#FFFFFF",
        "suave": "rgba(255,255,255,0.65)",
        "tenue": "rgba(255,255,255,0.4)",
        "acento": "#FF6300",
        "acento2": "#009EDB",
        "profundo": "#8C0001",
    },
    fuente_titulos="Outfit",
    fuente_texto="Inter",
)

# --------------------------------------------------------------- 1. Banner --
# El efecto de vídeo va en un widget html; el texto, en widgets nativos para
# que el cliente lo edite desde el editor visual.
efecto = leer_efecto(
    os.path.join(EFECTOS, "video-scrub-mouse.html"),
    VIDEO_URL="/wp-content/uploads/2026/01/hero.mp4",
)

banner = Plantilla("Landing — Banner", tema)
banner.agregar(seccion(
    html_personalizado(efecto),
    titulo("CUMBRE DE", nivel="h1", tam=9.5, unidad_tam="vw", peso="900",
           interlineado=0.85, tam_movil=13),
    titulo("TECNOLOGÍA", nivel="h1", tam=9.5, unidad_tam="vw", peso="900",
           interlineado=0.85, tam_movil=13),
    parrafo("<p>Dos días para decidir cómo la tecnología trabaja para el "
            "territorio.</p>", ancho_max=520, tam=17),
    justificar="space-between",
    padding=marco(96, 48, 48, 48),
))
banner.guardar(os.path.join(SALIDA, "01-banner.json"))

# ------------------------------------------------------------ 2. Tarjetas --
def tarjeta(indice: str, nombre: str, texto: str):
    """Una tarjeta es un contenedor interior; la fila las reparte y las apila
    sola en móvil."""
    return contenedor(
        titulo(indice, nivel="h6", tam=12, color="acento", espaciado=4,
               mayusculas=True),
        titulo(nombre, nivel="h3", tam=32, peso="800"),
        parrafo(texto, tam=15),
        fondo="rgba(255,255,255,0.03)",
        padding=marco(32, 32, 32, 32),
        ancho_px=320,
        interior=True,
    )

tarjetas = Plantilla("Landing — Ejes", tema)
tarjetas.agregar(seccion(
    titulo("Cuatro ejes", nivel="h2", tam=64, tam_movil=40, peso="900",
           alineacion="center"),
    fila(
        tarjeta("01", "Educación", "Formación docente y aulas conectadas."),
        tarjeta("02", "Campo", "Datos y sensores para el agro."),
        tarjeta("03", "Salud", "Telemedicina en zonas dispersas."),
        separacion=24,
        justificar="center",
    ),
    alinear="center",
))
tarjetas.guardar(os.path.join(SALIDA, "02-ejes.json"))

# --------------------------------------------------------- 3. Inscripción --
inscripcion = Plantilla("Landing — Inscripción", tema)
inscripcion.agregar(seccion(
    titulo("Inscripciones abiertas", nivel="h6", tam=12, color="acento",
           espaciado=4, mayusculas=True, alineacion="center"),
    titulo("Sé parte de la Cumbre", nivel="h2", tam=84, tam_movil=48,
           peso="900", interlineado=0.9, alineacion="center"),
    parrafo("<p>La inscripción toma menos de dos minutos.</p>",
            alineacion="center", ancho_max=620),
    boton("Ir al formulario", "https://ejemplo.com/inscripcion",
          color_fondo="acento", color_texto="#00133D",
          color_fondo_hover="profundo", color_texto_hover="texto",
          icono_fa="fas fa-arrow-right"),
    alinear="center",
    id_css="inscripcion",  # ancla para enlaces #inscripcion
))
inscripcion.guardar(os.path.join(SALIDA, "03-inscripcion.json"))

print("Generadas 3 plantillas en", os.path.abspath(SALIDA))
print("Valida con:  python3 validar.py", os.path.join(SALIDA, "*.json"), "--arbol")
