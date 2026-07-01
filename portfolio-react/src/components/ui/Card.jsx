import { motion } from 'framer-motion';
import { clsx } from 'clsx';
export default function Card({ children, className='', delay=0 }) {
  return (
    <motion.div initial={{ opacity:0, y:20 }} whileInView={{ opacity:1, y:0 }} viewport={{ once:true }} transition={{ duration:0.5, delay }} whileHover={{ y:-4, scale:1.01 }}
      className={clsx('glass-card rounded-lg border border-white/10 bg-surface-container/50 transition-shadow hover:shadow-card', className)}>
      {children}
    </motion.div>
  );
}
