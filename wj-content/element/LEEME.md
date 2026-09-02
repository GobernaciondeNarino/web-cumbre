# Elementos para Elementor (WordPress)

Versiones autónomas de los dos efectos de la landing, listas para copiar y pegar
en widgets **HTML** de Elementor. No dependen de React ni de ninguna librería:
todo el CSS y JS viaja dentro de cada archivo, así que funcionan en cualquier
página de WordPress, en el orden que quieras y sin afectarse entre sí.

## Archivos

| Archivo                 | Qué hace |
|-------------------------|----------|
| `banner.html`           | Efecto del banner: el vídeo avanza/retrocede siguiendo el mouse (con suavizado), fondo azul con rejilla y fundido a oscuro al hacer scroll. |
| `contenido.html`        | Motor del recorrido: vídeo fijo a pantalla completa que se scrubbea con el scroll mientras el visitante pasa por tus secciones de capítulos. |
| `cumbre-banner.json`    | Plantilla importable de Elementor: banner completo (vídeo + títulos + párrafo) ya armado con widgets nativos. |
| `cumbre-contenido.json` | Plantilla importable de Elementor: motor + 5 capítulos con los textos de la Cumbre en widgets `heading`/`text-editor`. |
| `cumbre-inscripcion.json` | Plantilla importable de Elementor: sección "Inscripciones abiertas / Sé parte de la Cumbre" completa (etiqueta con punto pulsante, título, párrafo, fila de datos, botón píldora y nota), con ID de anclaje `inscripcion`. |

## Opción rápida — importar los JSON

1. En WordPress: **Plantillas → Plantillas guardadas → Importar plantillas**
   (o desde el editor de Elementor: carpeta → *Importar plantilla*).
2. Sube `cumbre-banner.json` y/o `cumbre-contenido.json`.
3. Inserta la plantilla en tu página y edita títulos, textos y botones como
   cualquier widget de Elementor.

## Opción manual — pegar los HTML

### Banner (`banner.html`)

1. Crea un contenedor con **Altura mínima = 100vh**.
2. Dentro, agrega un widget **HTML** y pega todo el contenido de `banner.html`.
3. En el mismo contenedor agrega tus widgets de título/texto: quedan
   automáticamente **encima** del vídeo, en el orden que quieras.
4. Para el degradado ámbar→naranja de un título, asigna al widget de título la
   clase CSS `cumbre-texto-degradado` (Avanzado → Clases CSS).

### Contenido (`contenido.html`)

1. Agrega un widget **HTML** con todo el contenido de `contenido.html`, ANTES
   de tus secciones de capítulos.
2. Crea cada capítulo como un contenedor normal de Elementor (título, texto,
   botones…) y asígnale la clase CSS **`cumbre-capitulo`** (Avanzado → Clases
   CSS). Fondo transparente para que el vídeo se vea detrás.
3. Crea los capítulos que quieras y en el orden que quieras: el vídeo se
   reparte en partes iguales entre ellos, y antes/después del recorrido
   desaparece solo.
4. Si no agregas ningún capítulo, el widget genera un recorrido de
   demostración de `data-secciones` × 100vh.

### Inscripción (`cumbre-inscripcion.json`)

1. Importa la plantilla e insértala donde quieras (normalmente al final).
2. El contenedor ya trae el ID CSS `inscripcion`, así que el botón "Quiero
   inscribirme" de los capítulos (enlace `#inscripcion`) salta hasta aquí.
3. **Pega la URL real de tu formulario** en el enlace del botón "Ir al
   formulario de inscripción" (por defecto apunta a `#`).
4. El punto pulsante de la etiqueta y el botón píldora vienen de las clases
   CSS `cumbre-etiqueta-viva` y `cumbre-boton` que define el pequeño widget
   HTML de decoración incluido en la plantilla (rejilla + glow naranja);
   puedes reutilizarlas en otros widgets de la misma página.

## Cambiar el vídeo

En la primera línea del `<div>` de cada archivo está `data-video="…"`:

- Por defecto apunta a `/cumbre/videos/…` (los vídeos de la landing en este
  mismo servidor).
- Puedes subir un MP4 a la **Biblioteca de medios** de WordPress y pegar aquí
  su URL. Requisitos: MP4 directo H.264, sin audio, idealmente con `faststart`.

## Notas

- Los scripts corren en la página publicada y en **Vista previa**; dentro del
  lienzo del editor de Elementor los widgets HTML no ejecutan JavaScript, así
  que el efecto se ve al previsualizar.
- Con `prefers-reduced-motion` activo, cada efecto muestra un frame fijo en
  lugar de animar.
- Ambos widgets pueden convivir en la misma página junto a cualquier otra
  sección de Elementor.
