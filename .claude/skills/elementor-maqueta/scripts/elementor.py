"""Constructor de plantillas importables de Elementor (WordPress).

Sin dependencias externas. La idea es describir la maqueta en Python y dejar
que la librería resuelva lo que Elementor exige y es fácil de equivocar: ids
únicos, la forma de los valores con unidad, las variantes responsive y —sobre
todo— la clave correcta de clases CSS, que difiere entre contenedores
(`css_classes`) y widgets (`_css_classes`).

Uso mínimo:

    from elementor import *

    p = Plantilla("Mi sección")
    p.agregar(seccion(titulo("Hola"), parrafo("<p>Qué tal.</p>")))
    p.guardar("seccion.json")
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass, field
from typing import Any, Iterable

__all__ = [
    "Tema", "Plantilla", "nuevo_id",
    "medida", "px", "pct", "vh", "vw", "em", "marco", "enlace",
    "contenedor", "seccion", "fila",
    "titulo", "parrafo", "boton", "imagen", "icono", "video",
    "html_personalizado", "espaciador", "separador", "widget",
]

# --------------------------------------------------------------------------
# Tema
# --------------------------------------------------------------------------

COLORES_BASE = {
    "fondo": "#0B1220",
    "texto": "#FFFFFF",
    "suave": "rgba(255,255,255,0.6)",
    "tenue": "rgba(255,255,255,0.4)",
    "acento": "#FF6300",
    "acento2": "#009EDB",
}


@dataclass
class Tema:
    """Paleta y tipografías compartidas por toda la maqueta.

    Fijarlas una sola vez evita que cada sección acabe con su propio azul o su
    propia fuente, que es como se degradan las maquetas largas.
    """

    colores: dict[str, str] = field(default_factory=lambda: dict(COLORES_BASE))
    fuente_titulos: str = "Outfit"
    fuente_texto: str = "Inter"
    fuente_mono: str = "JetBrains Mono"

    def __post_init__(self) -> None:
        # Crear un tema lo activa: así los helpers lo usan aunque construyas
        # elementos antes de instanciar la Plantilla.
        global TEMA_ACTUAL
        TEMA_ACTUAL = self

    def color(self, nombre_o_valor: str | None) -> str | None:
        """Acepta un nombre del tema ("acento") o un color literal ("#FF6300")."""
        if nombre_o_valor is None:
            return None
        return self.colores.get(nombre_o_valor, nombre_o_valor)


TEMA_ACTUAL = Tema()


# --------------------------------------------------------------------------
# Primitivas del formato
# --------------------------------------------------------------------------

def nuevo_id() -> str:
    """Elementor identifica cada elemento con 8 dígitos hexadecimales."""
    return secrets.token_hex(4)


def medida(valor: float | int, unidad: str = "px") -> dict[str, Any]:
    """Valor con unidad: {"unit": "px", "size": 24, "sizes": []}."""
    return {"unit": unidad, "size": valor, "sizes": []}


def px(valor): return medida(valor, "px")
def pct(valor): return medida(valor, "%")
def vh(valor): return medida(valor, "vh")
def vw(valor): return medida(valor, "vw")
def em(valor): return medida(valor, "em")


def marco(arriba=0, derecha=0, abajo=0, izquierda=0, unidad="px") -> dict[str, Any]:
    """Padding o margin. Elementor guarda los cuatro lados como cadenas."""
    ligado = arriba == derecha == abajo == izquierda
    return {
        "unit": unidad,
        "top": str(arriba), "right": str(derecha),
        "bottom": str(abajo), "left": str(izquierda),
        "isLinked": ligado,
    }


def enlace(url: str, externo: bool = False, nofollow: bool = False) -> dict[str, str]:
    """Estructura de enlace que esperan los widgets con URL."""
    return {
        "url": url,
        "is_external": "on" if externo else "",
        "nofollow": "on" if nofollow else "",
        "custom_attributes": "",
    }


def _limpiar(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


def _comunes(settings: dict[str, Any], es_widget: bool,
             clases: str | None, id_css: str | None) -> dict[str, Any]:
    """Enruta clases e id a las claves que Elementor lee de verdad.

    Los widgets leen `_css_classes` y los contenedores `css_classes`. Usar la
    del otro tipo no produce ningún error al importar: la clase simplemente no
    llega al HTML y el estilo no aparece nunca.
    """
    if clases:
        settings["_css_classes" if es_widget else "css_classes"] = clases
    if id_css:
        settings["_element_id"] = id_css
    return settings


def _responsive(settings: dict[str, Any], clave: str,
                tablet: Any = None, movil: Any = None) -> None:
    if tablet is not None:
        settings[f"{clave}_tablet"] = tablet
    if movil is not None:
        settings[f"{clave}_mobile"] = movil


def _tipografia(settings: dict[str, Any], fuente: str | None = None,
                tam: float | None = None, tam_tablet: float | None = None,
                tam_movil: float | None = None, peso: str | None = None,
                interlineado: float | None = None, espaciado: float | None = None,
                mayusculas: bool = False, unidad_tam: str = "px") -> None:
    """Activa tipografía personalizada. Sin `typography_typography: custom`
    Elementor ignora el resto de ajustes tipográficos."""
    if not any([fuente, tam, peso, interlineado, espaciado, mayusculas,
                tam_tablet, tam_movil]):
        return
    settings["typography_typography"] = "custom"
    if fuente:
        settings["typography_font_family"] = fuente
    if tam is not None:
        settings["typography_font_size"] = medida(tam, unidad_tam)
    _responsive(settings, "typography_font_size",
                medida(tam_tablet, unidad_tam) if tam_tablet is not None else None,
                medida(tam_movil, unidad_tam) if tam_movil is not None else None)
    if peso:
        settings["typography_font_weight"] = str(peso)
    if interlineado is not None:
        settings["typography_line_height"] = medida(interlineado, "em")
    if espaciado is not None:
        settings["typography_letter_spacing"] = medida(espaciado, "px")
    if mayusculas:
        settings["typography_text_transform"] = "uppercase"


def _fondo(settings: dict[str, Any], color: str | None,
           imagen_url: str | None = None) -> None:
    if color or imagen_url:
        settings["background_background"] = "classic"
    if color:
        settings["background_color"] = color
    if imagen_url:
        settings["background_image"] = {"url": imagen_url, "id": "", "size": ""}
        settings.setdefault("background_size", "cover")
        settings.setdefault("background_position", "center center")


# --------------------------------------------------------------------------
# Elementos
# --------------------------------------------------------------------------

def widget(tipo: str, settings: dict[str, Any] | None = None, *,
           clases: str | None = None, id_css: str | None = None) -> dict[str, Any]:
    """Widget genérico. Úsalo para cualquier widget sin helper propio —
    incluidos los de terceros, cuyo `widgetType` verás en un export real."""
    s = _comunes(_limpiar(settings or {}), True, clases, id_css)
    return {"id": nuevo_id(), "elType": "widget", "isInner": False,
            "settings": s, "elements": [], "widgetType": tipo}


def contenedor(*hijos: dict[str, Any], direccion: str = "column",
               justificar: str | None = None, alinear: str | None = None,
               ancho: str = "full", ancho_px: float | None = None,
               alto_min: float | None = None, alto_min_movil: float | None = None,
               unidad_alto: str = "vh", separacion: float | None = None,
               fondo: str | None = None, imagen_fondo: str | None = None,
               padding: dict | None = None, margen: dict | None = None,
               clases: str | None = None, id_css: str | None = None,
               interior: bool = False, extra: dict | None = None,
               tema: Tema | None = None) -> dict[str, Any]:
    """Contenedor flexbox: la unidad estructural de Elementor moderno.

    `direccion="row"` crea una fila; anida contenedores para columnas.
    """
    t = tema or TEMA_ACTUAL
    s: dict[str, Any] = {"content_width": ancho, "flex_direction": direccion}
    if justificar:
        s["flex_justify_content"] = justificar
    if alinear:
        s["flex_align_items"] = alinear
    if ancho_px is not None:
        s["width"] = px(ancho_px)
    if alto_min is not None:
        s["min_height"] = medida(alto_min, unidad_alto)
    if alto_min_movil is not None:
        s["min_height_mobile"] = medida(alto_min_movil, unidad_alto)
    if separacion is not None:
        s["flex_gap"] = {"unit": "px", "size": separacion, "column": str(separacion),
                         "row": str(separacion), "isLinked": True}
    _fondo(s, t.color(fondo), imagen_fondo)
    if padding:
        s["padding"] = padding
    if margen:
        s["margin"] = margen
    if extra:
        s.update(extra)
    s = _comunes(s, False, clases, id_css)
    return {"id": nuevo_id(), "elType": "container", "isInner": interior,
            "settings": s, "elements": list(hijos)}


def seccion(*hijos: dict[str, Any], alto_min: float | None = 100,
            padding: dict | None = None, **opts) -> dict[str, Any]:
    """Contenedor de primer nivel con los valores habituales de una sección:
    ancho completo, alto de pantalla y aire alrededor."""
    opts.setdefault("justificar", "center")
    return contenedor(*hijos, alto_min=alto_min,
                      padding=padding or marco(96, 24, 96, 24), **opts)


def fila(*hijos: dict[str, Any], separacion: float = 24, **opts) -> dict[str, Any]:
    """Fila de elementos (tarjetas, columnas) que se apila en móvil."""
    opts.setdefault("alinear", "stretch")
    return contenedor(*hijos, direccion="row", separacion=separacion,
                      interior=True, extra={"flex_wrap": "wrap"}, **opts)


def titulo(texto: str, nivel: str = "h2", *, color: str | None = "texto",
           tam: float | None = None, tam_tablet: float | None = None,
           tam_movil: float | None = None, unidad_tam: str = "px",
           alineacion: str | None = None, fuente: str | None = None,
           peso: str = "700", interlineado: float | None = None,
           espaciado: float | None = None, mayusculas: bool = False,
           clases: str | None = None, id_css: str | None = None,
           tema: Tema | None = None) -> dict[str, Any]:
    """Widget `heading`: el sitio natural de cualquier titular."""
    t = tema or TEMA_ACTUAL
    s: dict[str, Any] = {"title": texto, "header_size": nivel}
    if color:
        s["title_color"] = t.color(color)
    if alineacion:
        s["align"] = alineacion
    _tipografia(s, fuente or t.fuente_titulos, tam, tam_tablet, tam_movil,
                peso, interlineado, espaciado, mayusculas, unidad_tam)
    return widget("heading", s, clases=clases, id_css=id_css)


def parrafo(html: str, *, color: str | None = "suave", tam: float | None = 16,
            tam_movil: float | None = None, alineacion: str | None = None,
            fuente: str | None = None, interlineado: float | None = 1.6,
            ancho_max: float | None = None, clases: str | None = None,
            id_css: str | None = None, tema: Tema | None = None) -> dict[str, Any]:
    """Widget `text-editor`. Recibe HTML: envuelve el texto en `<p>`.

    Es el widget correcto para todo cuerpo de texto, porque el cliente lo edita
    con el editor enriquecido de Elementor.
    """
    t = tema or TEMA_ACTUAL
    if "<" not in html:
        html = f"<p>{html}</p>"
    s: dict[str, Any] = {"editor": html}
    if color:
        s["text_color"] = t.color(color)
    if alineacion:
        s["align"] = alineacion
    _tipografia(s, fuente or t.fuente_texto, tam, None, tam_movil,
                None, interlineado, None)
    if ancho_max is not None:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = px(ancho_max)
    return widget("text-editor", s, clases=clases, id_css=id_css)


def boton(texto: str, url: str = "#", *, externo: bool = True,
          color_fondo: str | None = "acento", color_texto: str | None = "#0B1220",
          color_fondo_hover: str | None = None, color_texto_hover: str | None = None,
          alineacion: str | None = "center", radio: float | None = 999,
          icono_fa: str | None = None, tam: float | None = 16,
          padding: dict | None = None, clases: str | None = None,
          id_css: str | None = None, tema: Tema | None = None) -> dict[str, Any]:
    """Widget `button`. El enlace queda editable desde el editor visual."""
    t = tema or TEMA_ACTUAL
    s: dict[str, Any] = {"text": texto, "link": enlace(url, externo)}
    if alineacion:
        s["align"] = alineacion
    if color_fondo:
        s["background_color"] = t.color(color_fondo)
    if color_texto:
        s["button_text_color"] = t.color(color_texto)
    if color_fondo_hover:
        s["button_background_hover_color"] = t.color(color_fondo_hover)
    if color_texto_hover:
        s["hover_color"] = t.color(color_texto_hover)
    if radio is not None:
        s["border_radius"] = marco(radio, radio, radio, radio)
    if icono_fa:
        s["selected_icon"] = {"value": icono_fa, "library": "fa-solid"}
        s["icon_align"] = "right"
    s["button_padding"] = padding or marco(16, 32, 16, 32)
    _tipografia(s, t.fuente_titulos, tam, None, None, "700")
    return widget("button", s, clases=clases, id_css=id_css)


def imagen(url: str, *, alt: str = "", ancho: float | None = None,
           radio: float | None = None, alineacion: str | None = None,
           url_enlace: str | None = None, clases: str | None = None,
           id_css: str | None = None) -> dict[str, Any]:
    """Widget `image`. La URL debe apuntar a la Biblioteca de medios del sitio
    destino; una ruta local no existe para WordPress."""
    s: dict[str, Any] = {"image": {"url": url, "id": "", "alt": alt, "source": "library"}}
    if ancho is not None:
        s["width"] = px(ancho)
    if radio is not None:
        s["image_border_radius"] = marco(radio, radio, radio, radio)
    if alineacion:
        s["align"] = alineacion
    if url_enlace:
        s["link_to"] = "custom"
        s["link"] = enlace(url_enlace, True)
    return widget("image", s, clases=clases, id_css=id_css)


def icono(icono_fa: str, *, titulo_texto: str = "", descripcion: str = "",
          color: str | None = "acento", tam: float | None = 32,
          clases: str | None = None, tema: Tema | None = None) -> dict[str, Any]:
    """Widget `icon-box` (icono + título + texto). Con `titulo_texto` vacío
    funciona como icono suelto."""
    t = tema or TEMA_ACTUAL
    s: dict[str, Any] = {
        "selected_icon": {"value": icono_fa, "library": "fa-solid"},
        "title_text": titulo_texto,
        "description_text": descripcion,
        "primary_color": t.color(color),
    }
    if tam is not None:
        s["icon_size"] = px(tam)
    return widget("icon-box", s, clases=clases)


def video(url: str, *, autoplay: bool = False, silenciado: bool = True,
          bucle: bool = False, controles: bool = True,
          clases: str | None = None) -> dict[str, Any]:
    """Widget `video` para reproducción normal. Para vídeo atado al cursor o al
    scroll usa los efectos de `assets/efectos/` dentro de un widget `html`."""
    s: dict[str, Any] = {
        "video_type": "hosted",
        "hosted_url": {"url": url, "id": "", "source": "library"},
        "autoplay": "yes" if autoplay else "",
        "mute": "yes" if silenciado else "",
        "loop": "yes" if bucle else "",
        "controls": "yes" if controles else "",
    }
    return widget("video", s, clases=clases)


def html_personalizado(codigo: str, *, clases: str | None = None,
                       id_css: str | None = None) -> dict[str, Any]:
    """Widget `html` para CSS/JS a medida.

    Resérvalo para comportamiento que Elementor no cubre. Si lo estás usando
    para maquetar texto, ese texto debería ser un `heading` o un `parrafo`:
    dentro de un `html` el cliente no puede editarlo desde el editor visual.
    """
    return widget("html", {"html": codigo}, clases=clases, id_css=id_css)


def espaciador(alto: float = 50, *, alto_movil: float | None = None) -> dict[str, Any]:
    s: dict[str, Any] = {"space": px(alto)}
    if alto_movil is not None:
        s["space_mobile"] = px(alto_movil)
    return widget("spacer", s)


def separador(*, color: str | None = "tenue", grosor: float = 1,
              tema: Tema | None = None) -> dict[str, Any]:
    t = tema or TEMA_ACTUAL
    return widget("divider", {"color": t.color(color), "weight": px(grosor)})


# --------------------------------------------------------------------------
# Plantilla
# --------------------------------------------------------------------------

class Plantilla:
    """Documento importable de Elementor.

    Elementor acepta `type: "page"` tanto para páginas completas como para
    secciones sueltas; al importarlas quedan en Plantillas guardadas y se
    insertan donde el cliente quiera.
    """

    def __init__(self, titulo_plantilla: str, tema: Tema | None = None,
                 fondo: str | None = None, ajustes_pagina: dict | None = None):
        global TEMA_ACTUAL
        self.titulo = titulo_plantilla
        self.tema = tema or TEMA_ACTUAL
        TEMA_ACTUAL = self.tema
        self.elementos: list[dict[str, Any]] = []
        self.ajustes_pagina: dict[str, Any] = dict(ajustes_pagina or {})
        color_fondo = self.tema.color(fondo or "fondo")
        if color_fondo:
            _fondo(self.ajustes_pagina, color_fondo)

    def agregar(self, *elementos: dict[str, Any]) -> "Plantilla":
        for e in elementos:
            self.elementos.append(e)
        return self

    def como_dict(self) -> dict[str, Any]:
        return {
            "content": self.elementos,
            "page_settings": self.ajustes_pagina,
            "version": "0.4",
            "title": self.titulo,
            "type": "page",
        }

    def guardar(self, ruta: str) -> str:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.como_dict(), f, ensure_ascii=False, indent=1)
        return ruta


def leer_efecto(ruta: str, **sustituciones: str) -> str:
    """Carga un efecto de `assets/efectos/` y sustituye marcadores `{{clave}}`."""
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    for clave, valor in sustituciones.items():
        codigo = codigo.replace("{{" + clave + "}}", valor)
    return codigo
