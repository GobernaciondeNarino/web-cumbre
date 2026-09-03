# Anatomía del JSON de Elementor

Lo verificado aquí sale de exportaciones reales de Elementor 3.x y del código
fuente del plugin, no de suposiciones. Si algo no aparece en este documento, la
forma más fiable de averiguarlo es exportar desde Elementor una sección que ya
tenga ese ajuste puesto y mirar el JSON (`validar.py archivo.json --arbol`).

## Documento

```json
{
  "content": [ ...elementos de primer nivel... ],
  "page_settings": { "background_background": "classic", "background_color": "#00133D" },
  "version": "0.4",
  "title": "Nombre en la biblioteca de plantillas",
  "type": "page"
}
```

Las cinco claves son obligatorias: si falta una, Elementor responde "el archivo
no es válido" sin más detalle. `version` es la del formato de exportación
(`0.4` en Elementor 3.x), no la del plugin.

`type: "page"` sirve igual para una página completa que para una sección
suelta: al importar, ambas quedan en *Plantillas guardadas* y se insertan donde
haga falta. Solo usa `header`/`footer` si la plantilla es para el Theme Builder.

## Elemento

```json
{
  "id": "242f4b3d",
  "elType": "container",
  "isInner": false,
  "settings": { },
  "elements": [ ]
}
```

- `id`: 8 dígitos hexadecimales en minúscula, **único en todo el documento**.
  Ids repetidos hacen que Elementor pierda elementos silenciosamente.
- `elType`: `container` para estructura, `widget` para contenido. Los
  `section`/`column` son el modelo antiguo: no lo uses en plantillas nuevas.
- `isInner`: `true` en contenedores anidados dentro de otro contenedor.
- `settings` y `elements` deben existir siempre, aunque vayan vacíos (`{}`/`[]`).
- Los widgets añaden `widgetType` y su `elements` va vacío (salvo los widgets
  anidados: `nested-tabs`, `nested-accordion`, `nested-carousel`, que sí llevan
  contenedores dentro).

## Contenedores flexbox

Elementor moderno maqueta con contenedores flex anidados. Los ajustes que más
se usan:

| Ajuste                | Valores                                          |
|-----------------------|--------------------------------------------------|
| `content_width`       | `"full"` (ancho completo) o `"boxed"`            |
| `flex_direction`      | `"column"` (por defecto) o `"row"`               |
| `flex_justify_content`| `flex-start`, `center`, `space-between`, `flex-end` |
| `flex_align_items`    | `flex-start`, `center`, `flex-end`, `stretch`    |
| `flex_wrap`           | `"wrap"` para que las filas se apilen en móvil   |
| `flex_gap`            | `{"unit":"px","size":24,"column":"24","row":"24","isLinked":true}` |
| `min_height`          | valor con unidad, típicamente `vh`               |

Una sección estándar es un contenedor `column` a `100vh` con `padding`; una
fila de tarjetas es un contenedor `row` con un contenedor interior por tarjeta.

## Valores con unidad

```json
{"unit": "px", "size": 24, "sizes": []}
```

`sizes` va siempre, aunque vacío. Unidades válidas: `px`, `%`, `em`, `rem`,
`vh`, `vw`. La excepción es el control de separación (`flex_gap`), que en vez
de `sizes` guarda `column` y `row` como cadenas.

## Valores de cuatro lados (padding, margin, radio)

```json
{"unit": "px", "top": "96", "right": "48", "bottom": "48", "left": "48", "isLinked": false}
```

Los cuatro lados son **cadenas**, no números. `isLinked` indica si el editor
muestra el candado cerrado; ponlo en `true` solo si los cuatro son iguales.

## Enlaces

```json
{"url": "https://…", "is_external": "on", "nofollow": "", "custom_attributes": ""}
```

`is_external: "on"` abre en pestaña nueva; `""` es el valor apagado. Elementor
usa esta convención de `"on"`/`""` en todos los interruptores (`autoplay`,
`mute`, etc. usan `"yes"`/`""` según el widget: compruébalo exportando).

## Clases CSS e ID — la diferencia que rompe maquetas

| Elemento    | Clases CSS      | ID CSS         |
|-------------|-----------------|----------------|
| Contenedor  | `css_classes`   | `_element_id`  |
| Widget      | `_css_classes`  | `_element_id`  |

Verificado en el código de Elementor: los widgets registran `_css_classes` en
`Widget_Common_Base::register_layout_section()`, y el contenedor registra
`css_classes` en `Container::register_advanced_controls()`.

Usar la clave del otro tipo **no produce ningún error**: la plantilla importa,
la clase no llega al HTML y el estilo asociado no aparece nunca. Cuando un
efecto que depende de una clase "no funciona", empieza por aquí.

`_element_id` es el ancla: un contenedor con `_element_id: "inscripcion"`
recibe los enlaces `#inscripcion`.

## Responsive

Cualquier ajuste dimensional admite sufijos por dispositivo:

```json
"typography_font_size":        {"unit": "px", "size": 84, "sizes": []},
"typography_font_size_tablet": {"unit": "px", "size": 64, "sizes": []},
"typography_font_size_mobile": {"unit": "px", "size": 40, "sizes": []}
```

Sufijos: `_tablet` (≤1024px) y `_mobile` (≤767px). Sin sufijo se aplica a
escritorio y hereda hacia abajo. Los tamaños grandes en `vw` suelen
autoajustarse; los grandes en `px` casi siempre necesitan `_mobile`.

## Tipografía

Los ajustes tipográficos se ignoran si no se activa antes el interruptor:

```json
"typography_typography": "custom",
"typography_font_family": "Outfit",
"typography_font_weight": "900",
"typography_font_size": {"unit": "px", "size": 84, "sizes": []},
"typography_line_height": {"unit": "em", "size": 0.9, "sizes": []},
"typography_letter_spacing": {"unit": "px", "size": 4, "sizes": []},
"typography_text_transform": "uppercase"
```

La fuente debe estar disponible en el sitio (Google Fonts las carga Elementor
solo; una fuente propia hay que subirla en *Elementor → Fuentes personalizadas*).

## Fondos

```json
"background_background": "classic",
"background_color": "#00133D",
"background_image": {"url": "https://…/imagen.jpg", "id": "", "size": ""},
"background_size": "cover",
"background_position": "center center"
```

`background_background: "classic"` es el interruptor: sin él, el color se
ignora. Para degradado, `"gradient"` con `background_color_b` y
`background_gradient_angle`.

## Medios

Las URLs de imágenes y vídeos deben ser accesibles desde el sitio destino:
súbelas a la Biblioteca de medios de WordPress y usa la URL resultante. Una
ruta local (`/home/…`) o de otro dominio sin CORS deja el hueco vacío. El campo
`id` puede ir vacío en una plantilla importada; WordPress no lo necesita para
mostrar el medio por URL.
