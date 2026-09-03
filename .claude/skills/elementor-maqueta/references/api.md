# API de `scripts/elementor.py`

Todos los helpers devuelven diccionarios listos para anidar. Los parámetros de
color aceptan un nombre del tema (`"acento"`) o un valor literal (`"#FF6300"`).

## Tema y plantilla

```python
Tema(colores={...}, fuente_titulos="Outfit", fuente_texto="Inter",
     fuente_mono="JetBrains Mono")
```

`colores` es un diccionario libre; las claves que usan los helpers por defecto
son `fondo`, `texto`, `suave`, `tenue`, `acento`, `acento2`. Añade las que
quieras (`profundo`, `exito`…) y refiérete a ellas por nombre.

```python
p = Plantilla("Título en la biblioteca", tema, fondo="fondo")
p.agregar(seccion1, seccion2)     # encadenable
p.guardar("01-banner.json")       # devuelve la ruta
p.como_dict()                     # por si necesitas post-procesar
```

Crear una `Plantilla` fija su tema como el activo, así que los helpers
posteriores lo usan sin pasarlo. Con varias plantillas y un solo tema no hay
sorpresas; si usas dos temas distintos en el mismo guion, pasa `tema=` a los
helpers de la segunda.

## Estructura

```python
contenedor(*hijos, direccion="column", justificar=None, alinear=None,
           ancho="full", ancho_px=None, alto_min=None, alto_min_movil=None,
           unidad_alto="vh", separacion=None, fondo=None, imagen_fondo=None,
           padding=None, margen=None, clases=None, id_css=None,
           interior=False, extra=None)
```

`extra` inyecta ajustes crudos de Elementor que no tengan parámetro propio
(p. ej. `extra={"flex_wrap": "wrap", "border_radius": marco(16,16,16,16)}`).
Es la vía de escape para todo lo que la librería no cubre.

```python
seccion(*hijos, alto_min=100, padding=None, **opts)
```
Contenedor de primer nivel con los valores habituales (ancho completo, `100vh`,
`justificar="center"`, padding `96/24/96/24`). Cualquiera se puede sobrescribir.

```python
fila(*hijos, separacion=24, **opts)
```
Contenedor `row` interior con `flex_wrap: wrap`, para tarjetas o columnas que
deben apilarse en móvil.

## Contenido

```python
titulo(texto, nivel="h2", color="texto", tam=None, tam_tablet=None,
       tam_movil=None, unidad_tam="px", alineacion=None, fuente=None,
       peso="700", interlineado=None, espaciado=None, mayusculas=False,
       clases=None, id_css=None)
```
Widget `heading`. Con `tam` pequeño, `espaciado` y `mayusculas=True` sirve
también para las etiquetas tipo *kicker* en monoespaciada.

```python
parrafo(html, color="suave", tam=16, tam_movil=None, alineacion=None,
        fuente=None, interlineado=1.6, ancho_max=None, clases=None)
```
Widget `text-editor`. Si el texto no trae etiquetas, lo envuelve en `<p>`.
`ancho_max` limita el ancho del widget en píxeles (útil para columnas de
lectura centradas).

```python
boton(texto, url="#", externo=True, color_fondo="acento",
      color_texto="#0B1220", color_fondo_hover=None, color_texto_hover=None,
      alineacion="center", radio=999, icono_fa=None, tam=16, padding=None,
      clases=None)
```
Widget `button`. `icono_fa` acepta un identificador de Font Awesome
(`"fas fa-arrow-right"`).

```python
imagen(url, alt="", ancho=None, radio=None, alineacion=None, url_enlace=None)
icono(icono_fa, titulo_texto="", descripcion="", color="acento", tam=32)
video(url, autoplay=False, silenciado=True, bucle=False, controles=True)
espaciador(alto=50, alto_movil=None)
separador(color="tenue", grosor=1)
```

```python
html_personalizado(codigo, clases=None, id_css=None)
```
Widget `html`, solo para comportamiento que Elementor no cubre. Si contiene
titulares, conviértelos en `titulo()`: dentro de un `html` el cliente no puede
editarlos.

```python
widget(tipo, settings, clases=None, id_css=None)
```
Escotilla para cualquier widget sin helper, incluidos los de terceros. El
`widgetType` exacto y sus ajustes se averiguan exportando desde el sitio del
cliente una sección que ya use ese widget.

## Utilidades

```python
px(24)  pct(50)  vh(100)  vw(9.5)  em(1.6)   # valores con unidad
medida(24, "rem")                             # unidad libre
marco(96, 48, 48, 48)                         # padding/margin/radio
enlace("https://…", externo=True)             # estructura de enlace
nuevo_id()                                    # id hexadecimal único
leer_efecto(ruta, VIDEO_URL="…")              # carga de assets/efectos con sustitución
```

## Patrón completo

```python
import sys; sys.path.insert(0, "<ruta-skill>/scripts")
from elementor import *

tema = Tema(colores={"fondo": "#0F172A", "acento": "#22D3EE", "texto": "#FFFFFF"})
p = Plantilla("Precios", tema)

def plan(nombre, precio, rasgos):
    return contenedor(
        titulo(nombre, nivel="h3", tam=28),
        titulo(precio, nivel="h2", tam=48, color="acento"),
        *[parrafo(r, tam=15) for r in rasgos],
        boton("Elegir", "https://ejemplo.com/checkout"),
        fondo="rgba(255,255,255,0.04)", padding=marco(32, 28, 32, 28),
        ancho_px=320, interior=True,
    )

p.agregar(seccion(
    titulo("Planes", nivel="h2", tam=56, alineacion="center"),
    fila(plan("Básico", "$0", ["1 sitio", "Soporte por correo"]),
         plan("Pro", "$29", ["10 sitios", "Soporte prioritario"]),
         justificar="center"),
    alinear="center",
))
p.guardar("precios.json")
```

Después: `python3 <ruta-skill>/scripts/validar.py precios.json --arbol`.
