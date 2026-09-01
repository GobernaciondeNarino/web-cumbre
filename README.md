# Cumbre IA Nariño — Landing

Landing interactiva de scroll total para la **Cumbre IA Nariño** (Gobernación de Nariño).
Dos escenarios `sticky` de vídeo cuyo tiempo de reproducción está atado al cursor y al
scroll, cinco capítulos superpuestos, widgets flotantes persistentes y sección final de
inscripción.

## Stack

React 19 · TypeScript · Vite 6 · Tailwind CSS v4 (`@tailwindcss/vite`) · `motion`
(Framer Motion v12, importado desde `motion/react`) · `lucide-react`. Sin librerías de
smooth-scroll: todo el scrub se resuelve con `useScroll`, `useSpring`, `useTransform`
y `useMotionValueEvent`.

## Desarrollo

```bash
npm install
npm run dev       # servidor de desarrollo
npm run build     # typecheck + build de producción
npm run preview   # sirve dist/
```

## Despliegue en Plesk

Este es un proyecto Vite: **nunca sirvas la raíz del repositorio**. El `index.html` de la
raíz referencia `/src/main.tsx`, que solo existe en el servidor de desarrollo — servirlo
directo produce los 404 de `main.tsx`. Lo que se publica es la carpeta **`dist/`**, que
está compilada y versionada en este repositorio con rutas relativas (funciona en
`httpdocs` o en cualquier subcarpeta).

Opción A — Desplegar el repo completo (la más simple):

1. Despliega el repositorio entero (Git de Plesk, FTP o File Manager) a `httpdocs`
   **o a cualquier subcarpeta** (p. ej. `httpdocs/cumbre`).
2. Nada más: el `.htaccess` de la raíz reescribe todas las peticiones hacia `dist/`,
   así que `https://tudominio/` o `https://tudominio/cumbre/` sirven el build
   directamente. No se necesita Node.js en el servidor ni cambiar el document root.

Opción B — Document root a `dist`:

1. Despliega el repo y en **Hosting Settings → Document root** apunta a la carpeta
   `dist` del despliegue (p. ej. `httpdocs/dist`).

Opción C — Subida manual solo del build:

1. En tu máquina: `npm install && npm run build`.
2. Sube **el contenido de `dist/`** a `httpdocs` (o a la subcarpeta que quieras) con el
   File Manager o FTP.

Notas:

- No hay rutas de SPA: es una sola página, no se necesitan reglas de rewrite en
  `.htaccess` ni en nginx.
- Los MP4 ya llevan `faststart`; Apache/nginx de Plesk sirven `Range` por defecto,
  que es lo único que el scrub de vídeo necesita.
- Si cambias código, vuelve a ejecutar `npm run build` y confirma el nuevo `dist/`
  antes de desplegar.

## Dónde cambiar los assets

Todo vive en `src/config/assets.ts`:

- `VIDEO_PRINCIPAL_URL` — vídeo del hero (scrub por ratón). Hoy: `/videos/cumbre-principal.mp4`.
- `VIDEO_SECUENCIA_URL` — vídeo de la secuencia de capítulos (scrub por scroll). Hoy: `/videos/cumbre-secuencia.mp4`.
- `FORM_URL` — URL del formulario externo de inscripción. **Está vacía**: el CTA se
  muestra deshabilitado hasta que pegues aquí la URL real (Google Forms, etc.).

Ambos vídeos fueron generados con [Higgsfield](https://higgsfield.ai) y están servidos
desde `public/videos/` como MP4 H.264 con `faststart`, sin audio. El texto de los
capítulos se edita en `src/config/chapters.ts`.

## Integraciones incluidas

- `.claude/skills/` — skill [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
  y sus sub-skills de diseño para Claude Code.
- `.github/workflows/claude.yml` — [claude-code-action](https://github.com/anthropics/claude-code-action):
  responde a menciones `@claude` en issues y PRs. Requiere el secret `ANTHROPIC_API_KEY`.
- `.github/workflows/security-review.yml` — [claude-code-security-review](https://github.com/anthropics/claude-code-security-review):
  revisión de seguridad automática en cada PR. Usa el mismo secret `ANTHROPIC_API_KEY`.
