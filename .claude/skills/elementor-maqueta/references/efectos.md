# Efectos personalizados en widgets HTML

Elementor cubre lo habitual (aparecer al hacer scroll, parallax, sticky). Para
lo que no cubre —un vídeo cuyo fotograma depende del cursor o del scroll, un
lienzo animado, una interacción a medida— la vía es un widget `html` con su CSS
y su JS dentro.

Un efecto así convive con el editor visual si cumple tres condiciones. Las tres
salen de haber roto maquetas por no cumplirlas.

## 1. Anclarse al contenedor que lo aloja

Un widget HTML no sabe dónde lo van a colocar. Si posiciona algo en absoluto
sin más, se ancla al primer ancestro posicionado, que puede ser cualquier cosa.
La solución es que el propio script busque su contenedor de Elementor y lo
marque:

```js
var raiz = document.querySelector(".mi-efecto:not([data-listo])");
raiz.setAttribute("data-listo", "1");

var anfitrion = raiz.closest(".elementor-widget");        // el widget html
if (anfitrion) anfitrion.classList.add("mi-efecto-anfitrion");

var marco = raiz.closest(".e-con, .elementor-section, .elementor-column")
         || raiz.parentElement;                           // el contenedor
marco.classList.add("mi-efecto-marco");
```

Con eso, el CSS puede convertir ese contenedor en el marco del efecto y dejar
los demás widgets por encima:

```css
.mi-efecto-marco { position: relative !important; overflow: hidden; }
.mi-efecto-marco .elementor-widget:not(.mi-efecto-anfitrion) {
  position: relative; z-index: 2;
}
```

Así el cliente añade títulos y botones en el mismo contenedor y aparecen sobre
el efecto sin tocar código.

Clases útiles del frontend de Elementor: `.e-con` (contenedor moderno),
`.elementor-section` y `.elementor-column` (modelo antiguo),
`.elementor-widget` (cualquier widget).

## 2. Guardarse contra la doble inicialización

El mismo bloque puede acabar dos veces en una página (el cliente duplica la
sección) y Elementor reinyecta el HTML al editar. El selector
`:not([data-listo])` más el marcado inmediato resuelven ambos casos: cada
instancia se inicializa una vez y solo la suya.

Evita `document.currentScript` como forma de localizar el bloque: dentro del
editor no es fiable. Busca por clase.

## 3. Degradar bien

- Respeta `prefers-reduced-motion`: si está activo, muestra un estado estático
  en lugar de animar.
- Contempla el puntero grueso: `matchMedia("(pointer: fine)")` distingue ratón
  de táctil. Un efecto que solo responde al mouse necesita una alternativa
  (normalmente el scroll) o quedarse quieto.
- Escucha `scroll` con `{ passive: true }` para no bloquear el desplazamiento.

## El JS no corre dentro del editor

En el lienzo del editor de Elementor los widgets HTML no ejecutan JavaScript.
El efecto se ve en **Vista previa** y en la página publicada. Adviértelo al
entregar: de lo contrario el cliente reporta como fallo algo que funciona.

## Vídeo atado al cursor o al scroll

`assets/efectos/` trae dos efectos probados; sustituye `{{VIDEO_URL}}` (con
`leer_efecto(ruta, VIDEO_URL="…")`) por la URL del MP4 en la Biblioteca de
medios:

- **`video-scrub-mouse.html`** — el vídeo avanza y retrocede siguiendo el
  cursor. Se coloca dentro del contenedor del banner.
- **`video-scroll-secuencia.html`** — vídeo fijo a pantalla completa que avanza
  con el scroll mientras el visitante recorre las secciones marcadas con la
  clase `cumbre-capitulo`. Se coloca antes de esas secciones; funciona con
  cualquier número de ellas, repartiendo el vídeo en partes iguales.

Al reutilizarlos, **renombra el prefijo de sus clases** (`cumbre-banner` →
`festival-banner`, etc.). Dos secciones distintas generadas con esta skill
pueden acabar en la misma página, y si comparten prefijo el CSS de una pisa a
la otra. Es un renombrado mecánico de todo el bloque; hazlo también en el `<style>`
y en el `<script>`, que se buscan por esas mismas clases.

Ambos comparten la disciplina que hace que el scrub se vea fluido:

**Cola de un solo seek.** Un `<video>` no puede atender un salto por cada
`mousemove`: se satura y da tirones. Se guarda como mucho un salto pendiente y
se drena en el evento `seeked`, de modo que nunca se pide más de lo que el
decodificador puede dar.

**Suavizado con `requestAnimationFrame`.** El cursor o el scroll fijan un
*objetivo*; un bucle interpola hacia él (`actual += (objetivo - actual) * 0.09`).
Es lo que convierte un salto brusco en un movimiento amortiguado.

**Margen en el fotograma final.** Buscar exactamente `duration` bloquea el
vídeo en algunos navegadores; el destino se limita a `duration - 0.05`.

**El vídeo nunca se reproduce.** `muted playsinline preload="auto"`, pausado en
`loadedmetadata`, y el fotograma se controla solo por `currentTime`.

## Requisitos del archivo de vídeo

MP4 H.264, sin pista de audio, con `faststart` (el átomo `moov` al principio del
archivo, no al final). Sin `faststart` el navegador debe descargar casi todo
antes de poder saltar a un fotograma, y el efecto arranca tarde o no arranca.

Para comprobarlo y corregirlo:

```bash
ffmpeg -i entrada.mp4 -c copy -movflags +faststart -an salida.mp4
```

La duración debe ser finita: si `video.duration` devuelve `Infinity`, el
navegador no puede mapear el progreso y el efecto se queda en el primer
fotograma. Suele pasar con vídeos exportados como flujo continuo.
