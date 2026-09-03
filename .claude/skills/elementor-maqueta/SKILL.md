---
name: elementor-maqueta
description: Construye maquetación y diseño web como plantillas JSON importables en Elementor (WordPress) en lugar de HTML suelto. Úsala SIEMPRE que se pida diseñar, maquetar o construir una página, landing, banner, hero, sección, bloque, formulario, tarjeta de precios, footer o cualquier pieza visual que vaya a vivir en WordPress/Elementor — y también cuando se pida "pásame esto a Elementor", "un JSON para importar", "una plantilla de Elementor", "hazlo editable en el editor", o cuando el sitio destino sea WordPress aunque no se nombre Elementor. Genera un .json por sección (importable y reordenable), con textos en widgets nativos editables y efectos personalizados encapsulados en widgets HTML autónomos.
---

# Maquetación como plantillas de Elementor

Elementor no consume HTML: consume un JSON con su propio árbol de elementos. Una
maqueta entregada como HTML suelto obliga al cliente a editar código; entregada
como plantilla JSON, cada título, párrafo y botón queda editable con el editor
visual. Esa es la diferencia que justifica esta skill.

## El principio que ordena todo lo demás

**Todo lo que el cliente vaya a querer cambiar debe ser un widget nativo.**
Textos, botones, imágenes e iconos van en `heading`, `text-editor`, `button`,
`image`, `icon-box`. El widget `html` se reserva para lo que Elementor no sabe
hacer (un vídeo atado al scroll, un canvas, una animación a medida).

Volcar la sección entera dentro de un `html` es la tentación fácil y el peor
resultado posible: se ve bien y es inmantenible — el cliente abre Elementor y no
puede tocar nada. Si te sorprendes escribiendo `<h1>` dentro de un widget `html`,
para y conviértelo en un `heading`.

## Flujo de trabajo

1. **Descompón la maqueta en secciones** (banner, contenido, precios, contacto,
   pie…). Una plantilla `.json` por sección: se importan por separado, se
   reordenan y se reutilizan sin tocarse entre sí. Solo entrega una plantilla de
   página completa si te la piden explícitamente.
2. **Fija el tema una vez**: paleta y tipografías en un objeto `Tema` y
   propágalo. Evita que la sección 4 tenga un azul distinto al de la 1.
3. **Construye con `scripts/elementor.py`.** No escribas el JSON a mano: los
   `id`, las claves de ajustes y las variantes responsive son un campo minado
   (ver `references/formato.md`) y la librería ya los resuelve.
4. **Valida con `scripts/validar.py`** antes de entregar. Detecta ids
   duplicados, widgets mal formados y el error de clases CSS que describe la
   sección siguiente. Un JSON que Elementor rechaza al importar no admite
   depuración: solo dice "archivo no válido".
5. **Entrega** el o los `.json` más dos líneas de cómo importarlos
   (*Plantillas → Plantillas guardadas → Importar plantillas*) y qué queda por
   rellenar (URLs de formularios, imágenes de la Biblioteca de medios).

## La trampa de las clases CSS

Este detalle rompe maquetas de forma silenciosa y no está en la documentación
pública de Elementor; verificado en su código fuente:

| Elemento    | Clases CSS      | ID CSS         |
|-------------|-----------------|----------------|
| Contenedor  | `css_classes`   | `_element_id`  |
| Widget      | `_css_classes`  | `_element_id`  |

Poner `css_classes` en un widget no da error: la plantilla importa, la clase
nunca llega al HTML y el estilo simplemente no aparece. Si un efecto depende de
una clase y "no funciona", este es el primer sospechoso. La librería enruta la
clave correcta según el tipo de elemento, y el validador marca el caso.

## Cómo usar la librería

`scripts/elementor.py` no tiene dependencias. Impórtala y describe la página:

```python
import sys; sys.path.insert(0, "<ruta-skill>/scripts")
from elementor import *

tema = Tema(colores={"fondo": "#00133D", "acento": "#FF6300", "texto": "#FFFFFF"},
            fuente_titulos="Outfit", fuente_texto="Inter")

p = Plantilla("Mi landing — Hero", tema)
p.agregar(seccion(
    titulo("Bienvenido", nivel="h1", tam=72, tam_movil=40),
    parrafo("<p>Texto de apoyo que el cliente podrá editar.</p>"),
    boton("Inscríbete", "https://ejemplo.com/form", clases="mi-boton"),
    alto_min=100, fondo="#00133D", alinear="center",
))
p.guardar("hero.json")
```

`scripts/ejemplo_pagina.py` construye una página de tres secciones y sirve como
plantilla de arranque: léelo antes de escribir el tuyo, ahorra tanteo.

La API completa (parámetros de cada helper) está en `references/api.md`. El
catálogo de widgets nativos con sus ajustes reales está en
`references/widgets.md`; consúltalo cuando necesites un widget que no tenga
helper propio, en lugar de inventar nombres de ajustes.

## Estructura visual: contenedores flexbox

Elementor moderno maqueta con contenedores flex anidados, no con filas y
columnas. Una sección típica es un contenedor vertical a `100vh` que contiene
contenedores interiores. Para una fila de tarjetas, un contenedor con
`direccion="row"` y dentro un contenedor por tarjeta. `references/formato.md`
detalla el modelo y las unidades; `references/estilos.md`, la tipografía, el
color, el espaciado y los tres breakpoints.

## Efectos que Elementor no sabe hacer

Cuando la pieza necesita comportamiento real (vídeo atado al cursor o al scroll,
lienzo animado), va en un widget `html` **autónomo**: su CSS y su JS viajan
dentro del mismo bloque, y el script se ancla solo al contenedor de Elementor
que lo aloja para que los demás widgets queden por encima.

En `assets/efectos/` hay dos efectos ya probados y reutilizables:

- `video-scrub-mouse.html` — el vídeo avanza y retrocede siguiendo el cursor.
- `video-scroll-secuencia.html` — vídeo fijo a pantalla completa que avanza con
  el scroll mientras el visitante recorre las secciones que tú marques.

`references/efectos.md` explica el patrón de anclaje, la guarda contra doble
inicialización y por qué el JS no corre dentro del lienzo del editor (solo en
vista previa y en la página publicada) — dato que conviene advertirle al cliente
antes de que reporte un falso fallo.

## Antes de entregar

Ejecuta el validador sobre cada archivo:

```bash
python3 <ruta-skill>/scripts/validar.py hero.json --arbol
```

`--arbol` imprime la jerarquía resultante: léela y compárala con la maqueta que
te pidieron. Es la forma más rápida de detectar que una sección quedó anidada
donde no debía, algo que el JSON en crudo no deja ver.

El mismo validador lee exportaciones reales de Elementor. Si el cliente comparte
un JSON de su sitio, `--arbol` te muestra cómo está construido y qué widgets de
terceros usa, útil para imitar su estilo o reutilizar sus patrones.
