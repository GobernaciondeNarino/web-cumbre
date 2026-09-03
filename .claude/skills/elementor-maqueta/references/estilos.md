# Estilos: color, tipografía, ritmo y responsive

Criterios de maquetación que hacen que una plantilla se vea intencionada en vez
de genérica. No son reglas rígidas: son los puntos donde una maqueta suele
fallar y merece la pena decidir a conciencia.

## Color

Define la paleta una vez en el `Tema` y no introduzcas colores fuera de ella.
Un reparto que funciona casi siempre:

- **Un fondo** que domine la composición. Si es oscuro, el texto es blanco con
  opacidades (`1`, `0.6`, `0.4`) en lugar de grises distintos: mantiene la
  unidad y evita que aparezcan seis grises casi iguales.
- **Un acento principal** para lo accionable (botones, enlaces, indicadores).
- **Uno o dos acentos secundarios** para datos, cifras y estados.

Los acentos son puntuales: si ocupan más del 10 % de la pantalla dejan de
señalar y pasan a decorar. Un acento como fondo de una sección entera es la
forma más rápida de que una maqueta parezca de plantilla.

Contraste: comprueba el par crítico (texto sobre fondo y texto sobre botón).
Sobre fondo oscuro, blanco al 60 % suele ser el mínimo cómodo para párrafos;
por debajo de 0.4 solo para texto accesorio.

Foco visible: usa un color **distinto** al de relleno del botón. Si el botón es
naranja y el anillo de foco también, el foco no se distingue.

## Tipografía

Dos familias bastan: una de display para titulares y una de texto para lectura.
Una tercera monoespaciada funciona bien para etiquetas, cifras y metadatos.

Escala: los saltos deben ser evidentes. Un titular de sección a 56–84 px frente
a un cuerpo de 16–17 px crea jerarquía; 24 px frente a 18 px no crea ninguna.

- Titulares grandes: `peso="900"`, `interlineado=0.85–0.95`. El interlineado por
  defecto (~1.5) deja los titulares grandes desarmados.
- Cuerpo: `interlineado=1.6`, ancho máximo de 60–75 caracteres (`ancho_max` de
  520–620 px). Una línea de texto que cruza toda la pantalla no se lee.
- Etiquetas: monoespaciada, 11–12 px, `mayusculas=True`, `espaciado=3–4`.

Fuentes: Elementor carga las de Google automáticamente. Una fuente propia debe
subirse en *Elementor → Fuentes personalizadas* antes de nombrarla, o el
navegador cae al respaldo del sistema.

## Ritmo vertical

El aire es lo que separa una maqueta profesional de una amontonada. Padding de
sección de 96 px arriba y abajo en escritorio, 48–64 px en móvil, es un punto de
partida sano. Mantén el mismo valor entre secciones hermanas: un ritmo irregular
se percibe como descuido aunque nadie sepa nombrarlo.

Dentro de una sección, agrupa por proximidad: etiqueta y título casi pegados
(8 px), título y párrafo cerca (16–24 px), párrafo y botón separados (32–40 px).
La distancia comunica qué pertenece a qué.

## Responsive

Tres breakpoints: escritorio, `_tablet` (≤1024 px) y `_mobile` (≤767 px). Lo que
casi siempre hay que ajustar:

- **Titulares en `px`**: necesitan `tam_movil`. Un `84px` sin ajuste se sale de
  la pantalla. Los tamaños en `vw` escalan solos, pero conviene un mínimo.
- **Filas**: `fila()` ya trae `flex_wrap: wrap`, así que las tarjetas se apilan.
  Comprueba que el `ancho_px` de cada tarjeta no impida el apilado.
- **Padding lateral**: 48 px en escritorio suele ser 24 px en móvil.
- **Alturas fijas**: `100vh` en móvil compite con la barra del navegador;
  `alto_min_movil=None` (altura automática) evita cortes en secciones con mucho
  texto.

## Cuándo el efecto ayuda y cuándo estorba

Una animación tiene sentido cuando refuerza la lectura: algo que aparece al
entrar en pantalla, un vídeo que avanza con el scroll y acompaña al texto. Deja
de ayudar cuando compite con el contenido o retrasa la lectura.

Dos condiciones que conviene respetar siempre: que el contenido sea legible sin
esperar a la animación, y que `prefers-reduced-motion` desactive el movimiento
(los efectos de `assets/efectos/` ya lo hacen).
