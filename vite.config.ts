import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // Rutas relativas: el build funciona en httpdocs o en cualquier subcarpeta de Plesk.
  base: "./",
  plugins: [react(), tailwindcss()],
});
