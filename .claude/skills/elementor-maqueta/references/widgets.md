# Catálogo de widgets nativos

Widgets que existen en cualquier instalación de Elementor (los gratuitos, sin
Pro ni plugins de terceros). Para los que no tienen helper en la librería, usa
`widget("tipo", {ajustes})`.

La regla de oro al elegir: si el cliente va a querer cambiar ese contenido,
tiene que ser un widget nativo. Un bloque `html` es cómodo de escribir y
horrible de mantener.

## Los que más se usan

| `widgetType`  | Para qué                    | Ajustes clave |
|---------------|-----------------------------|---------------|
| `heading`     | Titulares y etiquetas       | `title`, `header_size` (h1–h6, div, span), `align`, `title_color` |
| `text-editor` | Cuerpo de texto (HTML)      | `editor`, `text_color`, `align` |
| `button`      | Llamadas a la acción        | `text`, `link`, `align`, `background_color`, `button_text_color`, `selected_icon`, `icon_align` |
| `image`       | Imágenes                    | `image` (`{url, id, alt}`), `image_size`, `align`, `link_to` + `link` |
| `video`       | Vídeo con controles         | `video_type` (`hosted`/`youtube`/`vimeo`), `hosted_url` o `youtube_url`, `autoplay`, `mute`, `loop`, `controls` |
| `html`        | CSS/JS a medida             | `html` |
| `spacer`      | Espacio vertical            | `space` |
| `divider`     | Línea separadora            | `color`, `weight`, `style` |
| `icon`        | Icono suelto                | `selected_icon`, `primary_color`, `size` |
| `icon-box`    | Icono + título + texto      | `selected_icon`, `title_text`, `description_text`, `primary_color` |
| `icon-list`   | Lista con viñetas de icono  | `icon_list` (lista de `{text, selected_icon, link}`) |
| `image-box`   | Imagen + título + texto     | `image`, `title_text`, `description_text` |
| `menu-anchor` | Ancla de destino            | `anchor` |
| `shortcode`   | Shortcode de WordPress      | `shortcode` |

## Estructurales y de composición

| `widgetType`       | Para qué |
|--------------------|----------|
| `tabs`             | Pestañas clásicas (`tabs` = lista de `{tab_title, tab_content}`) |
| `accordion`        | Acordeón (`tabs` = lista de `{tab_title, tab_content}`) |
| `toggle`           | Desplegables independientes |
| `nested-tabs`      | Pestañas cuyo contenido son contenedores completos |
| `nested-accordion` | Acordeón con contenedores dentro |
| `nested-carousel`  | Carrusel con contenedores dentro |

Los tres `nested-*` son la vía para meter maquetación rica dentro de una
pestaña o un slide: su `elements` contiene contenedores, a diferencia del resto
de widgets.

## Otros disponibles

`image-gallery`, `image-carousel`, `counter`, `progress`, `testimonial`,
`star-rating`, `alert`, `social-icons`, `google_maps`, `sidebar`, `text-path`.

## Formularios

`form` es un widget de **Elementor Pro**. En un sitio sin Pro, las alternativas
que sí funcionan:

1. Un `button` que enlaza a un formulario externo (Google Forms, Typeform). Es
   lo más robusto y no depende de plugins.
2. Un `shortcode` con el shortcode de Contact Form 7, WPForms o similar, si el
   sitio ya tiene ese plugin. Pregunta cuál usan antes de asumirlo.

Antes de dar por supuesto que un widget existe en el sitio destino, confírmalo:
una plantilla con un widget ausente importa, pero el hueco aparece vacío.

## Widgets de terceros

Un export del sitio del cliente revela qué plugins usa. En el ejemplo real que
motivó esta skill aparecían `ha-slider`, `ha-icon-box` y `nested-carousel`: los
dos primeros son de HappyAddons. Se pueden reutilizar copiando su bloque de
`settings` de ese export, pero solo funcionarán en sitios con ese plugin
instalado — por eso conviene preferir nativos salvo que el cliente pida lo
contrario.

`validar.py` avisa de cada widget no nativo que encuentre, para que la decisión
sea consciente.

## Cómo averiguar los ajustes de un widget que no está aquí

1. En el sitio destino, monta ese widget con Elementor y configúralo.
2. Exporta la plantilla.
3. `python3 validar.py export.json --arbol` para localizarlo, y abre el JSON
   para copiar las claves exactas de `settings`.

Es más rápido y fiable que deducir los nombres: Elementor no mantiene una
referencia pública completa de claves de ajustes.
