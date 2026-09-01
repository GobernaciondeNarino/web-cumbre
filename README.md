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
