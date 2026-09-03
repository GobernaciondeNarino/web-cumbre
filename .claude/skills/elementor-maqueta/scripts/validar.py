#!/usr/bin/env python3
"""Valida (e inspecciona) plantillas JSON de Elementor.

Elementor no explica por qué rechaza un archivo: dice "el archivo no es válido"
y ahí se acaba la depuración. Este validador revisa antes las condiciones que
provocan ese rechazo, y además marca errores que importan sin romper la
importación —el caso típico son las clases CSS puestas en la clave del otro
tipo de elemento, que se pierden en silencio.

    python3 validar.py plantilla.json           # validar
    python3 validar.py plantilla.json --arbol   # validar y ver la jerarquía

También sirve para leer un export real del cliente y entender cómo está
construido su sitio antes de imitar su estilo.
"""

from __future__ import annotations

import json
import re
import sys

ID_VALIDO = re.compile(r"^[0-9a-f]{6,10}$")
TIPOS_CONTENEDOR = {"container", "section", "column", "e-flexbox", "e-div-block"}

# Widgets que existen en cualquier instalación de Elementor. Los de terceros no
# se marcan como error: solo se avisa, porque dependen de plugins del sitio.
WIDGETS_NATIVOS = {
    "heading", "text-editor", "button", "image", "video", "html", "spacer",
    "divider", "icon", "icon-box", "icon-list", "image-box", "image-gallery",
    "image-carousel", "google_maps", "tabs", "accordion", "toggle", "alert",
    "counter", "progress", "testimonial", "social-icons", "shortcode",
    "menu-anchor", "sidebar", "text-path", "star-rating", "form", "nested-tabs",
    "nested-accordion", "nested-carousel", "container",
}


class Informe:
    def __init__(self) -> None:
        self.errores: list[str] = []
        self.avisos: list[str] = []

    def error(self, ruta: str, mensaje: str) -> None:
        self.errores.append(f"{ruta}: {mensaje}")

    def aviso(self, ruta: str, mensaje: str) -> None:
        self.avisos.append(f"{ruta}: {mensaje}")


def _revisar_elemento(el, ruta: str, inf: Informe, ids: dict[str, str]) -> None:
    if not isinstance(el, dict):
        inf.error(ruta, f"se esperaba un objeto y hay {type(el).__name__}")
        return

    tipo = el.get("elType")
    if not tipo:
        inf.error(ruta, "falta 'elType' (Elementor no sabe qué construir)")
    ident = el.get("id")
    if not ident:
        inf.error(ruta, "falta 'id'")
    elif not isinstance(ident, str) or not ID_VALIDO.match(ident):
        inf.error(ruta, f"id inválido {ident!r}: deben ser dígitos hexadecimales "
                        "en minúscula (8 es lo habitual)")
    elif ident in ids:
        inf.error(ruta, f"id duplicado {ident!r}, ya usado en {ids[ident]}; "
                        "Elementor pierde elementos con ids repetidos")
    else:
        ids[ident] = ruta

    ajustes = el.get("settings")
    if not isinstance(ajustes, dict):
        inf.error(ruta, "'settings' debe existir y ser un objeto (usa {} si no hay ajustes)")
        ajustes = {}

    hijos = el.get("elements")
    if not isinstance(hijos, list):
        inf.error(ruta, "'elements' debe existir y ser una lista (usa [] si no tiene hijos)")
        hijos = []

    es_widget = tipo == "widget"

    if es_widget:
        wt = el.get("widgetType")
        if not wt:
            inf.error(ruta, "un elemento 'widget' necesita 'widgetType'")
        elif wt not in WIDGETS_NATIVOS:
            inf.aviso(ruta, f"widget '{wt}' no es nativo: solo funcionará si el "
                            "sitio destino tiene instalado el plugin que lo aporta")
        if "css_classes" in ajustes:
            inf.error(ruta, "un widget guarda sus clases en '_css_classes'; con "
                            "'css_classes' la plantilla importa pero la clase "
                            "nunca llega al HTML y el estilo no se aplica")
    else:
        if el.get("widgetType"):
            inf.error(ruta, f"'{tipo}' no debe llevar 'widgetType'")
        if "_css_classes" in ajustes:
            inf.error(ruta, "un contenedor guarda sus clases en 'css_classes' "
                            "(sin guion bajo); con '_css_classes' se pierden")
        if tipo not in TIPOS_CONTENEDOR:
            inf.aviso(ruta, f"elType '{tipo}' poco habitual")

    if es_widget and hijos:
        inf.aviso(ruta, "un widget con hijos: salvo los widgets anidados "
                        "(nested-tabs, nested-carousel) esto suele ser un error")

    # Un widget html que maqueta texto es la señal de que la sección no será
    # editable desde el editor visual, que es el motivo de usar Elementor.
    if es_widget and el.get("widgetType") == "html":
        codigo = ajustes.get("html", "")
        if isinstance(codigo, str):
            titulares = len(re.findall(r"<h[1-6][\s>]", codigo, re.I))
            if titulares >= 2:
                inf.aviso(ruta, f"el widget html contiene {titulares} titulares: "
                                "conviértelos en widgets 'heading' para que el "
                                "cliente pueda editarlos desde Elementor")
            if "<script" in codigo.lower() and "data-listo" not in codigo:
                inf.aviso(ruta, "el widget html ejecuta JS sin guarda de doble "
                                "inicialización: si el bloque se duplica en la "
                                "página, el efecto se inicializa dos veces")

    _revisar_ajustes(ajustes, ruta, inf)

    for i, hijo in enumerate(hijos):
        _revisar_elemento(hijo, f"{ruta} > [{i}]", inf, ids)


def _revisar_ajustes(ajustes: dict, ruta: str, inf: Informe) -> None:
    for clave, valor in ajustes.items():
        if not isinstance(valor, dict):
            continue
        # El control de separación (gap) guarda 'column'/'row' en vez de 'sizes'.
        es_gap = "column" in valor or "row" in valor
        if "unit" in valor and "size" in valor and "sizes" not in valor and not es_gap:
            inf.aviso(ruta, f"'{clave}': falta la clave 'sizes' (Elementor la "
                            "escribe siempre, aunque sea una lista vacía)")
        if "top" in valor and "unit" in valor and "isLinked" not in valor:
            inf.aviso(ruta, f"'{clave}': falta 'isLinked' en el valor de cuatro lados")
        if clave == "link" or clave.endswith("_link"):
            if "url" in valor and "is_external" not in valor:
                inf.aviso(ruta, f"'{clave}': sin 'is_external' el enlace no puede "
                                "abrir en pestaña nueva")


def validar(datos, inf: Informe) -> None:
    if not isinstance(datos, dict):
        inf.error("raíz", "el archivo debe contener un objeto JSON")
        return

    for clave in ("content", "page_settings", "version", "title", "type"):
        if clave not in datos:
            inf.error("raíz", f"falta la clave '{clave}' que Elementor exige al importar")

    if not isinstance(datos.get("content"), list):
        inf.error("raíz", "'content' debe ser la lista de elementos de primer nivel")
    elif not datos["content"]:
        inf.aviso("raíz", "'content' está vacío: la plantilla se importará en blanco")

    tipo = datos.get("type")
    if tipo and tipo not in {"page", "section", "container", "header", "footer",
                             "single-page", "popup", "wp-page"}:
        inf.aviso("raíz", f"type '{tipo}' poco habitual; 'page' funciona tanto "
                          "para páginas completas como para secciones sueltas")

    if not isinstance(datos.get("page_settings"), dict):
        inf.error("raíz", "'page_settings' debe ser un objeto (usa {} si no hay ajustes)")

    if not isinstance(datos.get("title"), str) or not datos.get("title"):
        inf.aviso("raíz", "sin 'title' la plantilla aparece sin nombre en la biblioteca")

    ids: dict[str, str] = {}
    for i, el in enumerate(datos.get("content") or []):
        _revisar_elemento(el, f"content[{i}]", inf, ids)


def imprimir_arbol(elementos, nivel: int = 0) -> None:
    for el in elementos:
        if not isinstance(el, dict):
            continue
        sangria = "  " * nivel
        tipo = el.get("elType", "?")
        ajustes = el.get("settings", {}) if isinstance(el.get("settings"), dict) else {}
        if tipo == "widget":
            etiqueta = el.get("widgetType", "?")
            detalle = (ajustes.get("title") or ajustes.get("text")
                       or ajustes.get("title_text") or "")
            if not detalle and ajustes.get("editor"):
                detalle = re.sub(r"<[^>]+>", "", ajustes["editor"]).strip()
            if not detalle and etiqueta == "html":
                detalle = f"({len(ajustes.get('html', ''))} caracteres de código)"
            detalle = re.sub(r"\s+", " ", str(detalle))[:60]
            print(f"{sangria}• {etiqueta}{': ' + detalle if detalle else ''}")
        else:
            partes = [tipo]
            if ajustes.get("css_classes"):
                partes.append(f".{ajustes['css_classes']}")
            if ajustes.get("_element_id"):
                partes.append(f"#{ajustes['_element_id']}")
            if ajustes.get("flex_direction") == "row":
                partes.append("(fila)")
            alto = ajustes.get("min_height")
            if isinstance(alto, dict) and alto.get("size"):
                partes.append(f"{alto['size']}{alto.get('unit', '')}")
            print(f"{sangria}┌ {' '.join(partes)}")
        imprimir_arbol(el.get("elements") or [], nivel + 1)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ver_arbol = "--arbol" in sys.argv
    if not args:
        print(__doc__)
        return 2

    salida = 0
    for ruta in args:
        try:
            with open(ruta, encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            print(f"✗ {ruta}: JSON mal formado (línea {e.lineno}, columna {e.colno}): {e.msg}")
            salida = 1
            continue
        except OSError as e:
            print(f"✗ {ruta}: no se pudo leer ({e})")
            salida = 1
            continue

        inf = Informe()
        validar(datos, inf)

        print(f"\n=== {ruta} ===")
        if isinstance(datos, dict):
            print(f"Título: {datos.get('title')!r} · versión {datos.get('version')} "
                  f"· type {datos.get('type')} · {len(datos.get('content') or [])} "
                  "elemento(s) de primer nivel")

        if ver_arbol and isinstance(datos, dict):
            print("\nJerarquía:")
            imprimir_arbol(datos.get("content") or [])
            print()

        for e in inf.errores:
            print(f"  ✗ {e}")
        for a in inf.avisos:
            print(f"  ! {a}")

        if inf.errores:
            print(f"  → {len(inf.errores)} error(es): corrígelos antes de entregar.")
            salida = 1
        elif inf.avisos:
            print(f"  ✓ Importable. {len(inf.avisos)} aviso(s) que conviene revisar.")
        else:
            print("  ✓ Sin problemas.")
    return salida


if __name__ == "__main__":
    sys.exit(main())
