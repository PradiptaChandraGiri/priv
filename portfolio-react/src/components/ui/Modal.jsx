import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
export default function Modal({ open, onClose, children, title }) {
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => { window.removeEventListener('keydown', onKey); document.body.style.overflow = ''; };
  }, [open, onClose]);
  return (
    <AnimatePresence>
      {open && (
        <motion.div initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-background/80 backdrop-blur-md" onClick={onClose} />
          <motion.div initial={{scale:0.95,opacity:0}} animate={{scale:1,opacity:1}} exit={{scale:0.95,opacity:0}}
            className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto glass-card rounded-xl border border-white/10 shadow-card">
            <div className="flex items-center justify-between p-4 border-b border-white/10">
              {title && <h3 className="font-display font-semibold text-on-surface">{title}</h3>}
              <button onClick={onClose} className="ml-auto p-1.5 rounded-lg text-on-surface-variant hover:text-primary hover:bg-primary/10 transition-all"><X size={18}/></button>
            </div>
            <div className="p-6">{children}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
