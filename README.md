# elementor-maqueta

Skill de Claude Code para **construir maquetación web como plantillas JSON
importables en Elementor (WordPress)** en lugar de HTML suelto.

Cuando pides una landing, un banner, una sección de precios o cualquier pieza
visual para un sitio WordPress, la skill produce uno o varios `.json` que se
importan en *Plantillas → Plantillas guardadas → Importar plantillas*. Los
textos, botones e imágenes quedan en widgets nativos —editables desde el editor
visual, sin tocar código— y los efectos que Elementor no sabe hacer (vídeo
atado al cursor o al scroll) viajan encapsulados en widgets HTML autónomos.

## Qué incluye

```
.claude/skills/elementor-maqueta/
├── SKILL.md                      Criterio de trabajo y flujo
├── scripts/
│   ├── elementor.py              Librería constructora (sin dependencias)
│   ├── validar.py                Validador e inspector de plantillas
│   └── ejemplo_pagina.py         Ejemplo ejecutable de tres secciones
├── references/
│   ├── formato.md                Anatomía del JSON de Elementor
│   ├── api.md                    API de la librería
│   ├── widgets.md                Catálogo de widgets nativos
│   ├── estilos.md                Color, tipografía, ritmo y responsive
│   └── efectos.md                Efectos a medida en widgets HTML
└── assets/
    ├── efectos/                  Vídeo con scrub por cursor y por scroll
    └── ejemplos/                 Plantillas reales ya validadas
```

## Instalación

Para usarla en cualquier proyecto, copia la carpeta de la skill a tu perfil:

```bash
git clone https://github.com/GobernaciondeNarino/landing.git
cp -r landing/.claude/skills/elementor-maqueta ~/.claude/skills/
```

Dentro de este repositorio la skill se carga sola: Claude Code lee
`.claude/skills/` del proyecto en el que trabaja.

## Uso

Basta con pedir la maqueta en lenguaje natural — la skill se activa por sí
sola cuando el destino es WordPress o Elementor:

> «Hazme una sección de precios con tres planes para mi sitio en WordPress.»

Para validar o inspeccionar una plantilla (propia o exportada del sitio de un
cliente):

```bash
python3 .claude/skills/elementor-maqueta/scripts/validar.py plantilla.json --arbol
```

## Historial

Este repositorio alojó antes la landing de la Cumbre IA Nariño (React + Vite,
vídeos y las primeras plantillas de Elementor), de donde salió todo lo que la
skill sabe sobre el formato. Ese código sigue íntegro en el historial, en el
commit `861dc74`:

```bash
git show --stat 861dc74          # ver qué contenía
git checkout 861dc74             # explorarlo
git checkout 861dc74 -- .        # recuperarlo al directorio de trabajo
```

La landing publicada en `tic.narino.gov.co/cumbre/` se sirve desde la carpeta
`dist/` de ese commit: si necesitas volver a desplegarla, recupérala así antes
de hacer *pull* en Plesk.
