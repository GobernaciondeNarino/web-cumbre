import { motion, type Variants } from "motion/react";

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15, delayChildren: 0.1 },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 40, filter: "blur(10px)" },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: { type: "spring", damping: 18, stiffness: 100 },
  },
};

export default function CumbreTitle() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="relative w-full max-w-7xl mx-auto px-6 md:px-12 pt-4 md:pt-6 pb-2 select-none"
    >
      <div className="flex flex-col md:flex-row items-stretch justify-between relative">
        <div
          aria-hidden="true"
          className="hidden md:block absolute left-1/2 top-0 bottom-0 w-[1px] bg-gradient-to-b from-transparent via-white/10 to-transparent"
        />
        <motion.div variants={itemVariants}>
          <p className="text-xs font-mono tracking-[0.25em] text-amber mb-1 ml-2 uppercase">
            2026 · Pasto
          </p>
          <h1 className="font-display font-black leading-[0.8] tracking-tighter text-[22vw] md:text-[16vw]">
            CUM
          </h1>
        </motion.div>
        <motion.div variants={itemVariants} className="md:text-right">
          <p className="text-xs font-mono tracking-[0.2em] uppercase mb-1 mr-2">
            <span className="text-amber">500+</span>
            <span className="text-white/40"> asistentes esperados</span>
          </p>
          <h1 className="font-display font-black leading-[0.8] tracking-tighter text-[22vw] md:text-[16vw]">
            BRE
          </h1>
        </motion.div>
      </div>
    </motion.div>
  );
}
