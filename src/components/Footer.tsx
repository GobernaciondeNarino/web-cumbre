export default function Footer() {
  return (
    <footer className="border-t border-white/10 py-12">
      <div className="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 md:grid-cols-3 gap-8 font-mono text-xs text-white/40">
        <div>
          <p className="text-white/70 mb-2">Cumbre IA Nariño</p>
          <p>Gobernación de Nariño</p>
          <p>Pasto · Nariño · Colombia</p>
        </div>
        <div>
          <p className="text-white/70 mb-2">Contacto</p>
          <p>
            <a
              href="mailto:hosting@narino.gov.co"
              className="hover:text-sky transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky"
            >
              hosting@narino.gov.co
            </a>
          </p>
          <p>
            <a
              href="https://narino.gov.co"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-sky transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky"
            >
              narino.gov.co
            </a>
          </p>
        </div>
        <div className="md:text-right">
          <p className="text-white/70 mb-2">© 2026</p>
          <p>Secretaría TIC — Gobernación de Nariño</p>
          <p>Todos los derechos reservados</p>
        </div>
      </div>
    </footer>
  );
}
