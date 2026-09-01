import { motion } from "motion/react";

export default function LeftInfoBlock() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6, duration: 0.8, ease: "easeOut" }}
      className="lg:col-span-6 xl:col-span-7"
    >
      <p className="font-mono text-xs tracking-[0.3em] text-ember uppercase mb-3">
        Inteligencia Artificial · Nariño
      </p>
      <p className="text-white/60 text-base md:text-lg leading-relaxed max-w-md">
        El primer gran encuentro de inteligencia artificial del suroccidente
        colombiano. Mueve el cursor sobre esta escena y desplázate para
        recorrer la Cumbre.
      </p>
    </motion.div>
  );
}
