import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { FolderCode, Award, BookOpen, Layers } from 'lucide-react';

const stats = [
  { label: 'Projects Built', value: 12, suffix: '+', icon: FolderCode, color: 'text-primary', bg: 'bg-primary/10', border: 'border-primary/20' },
  { label: 'Certificates Earned', value: 8, suffix: '+', icon: Award, color: 'text-tertiary', bg: 'bg-tertiary/10', border: 'border-tertiary/20' },
  { label: 'Research Papers', value: 2, suffix: '', icon: BookOpen, color: 'text-secondary', bg: 'bg-secondary/10', border: 'border-secondary/20' },
  { label: 'Tech Skills', value: 20, suffix: '+', icon: Layers, color: 'text-primary', bg: 'bg-primary/10', border: 'border-primary/20' },
];

function AnimatedNumber({ target, suffix }) {
  const [val, setVal] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        let start = 0;
        const step = () => { start += Math.ceil(target / 40); if (start >= target) { setVal(target); } else { setVal(start); requestAnimationFrame(step); } };
        requestAnimationFrame(step);
        obs.disconnect();
      }
    }, { threshold: 0.5 });
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, [target]);
  return <span ref={ref}>{val}{suffix}</span>;
}

export default function StatsSection() {
  return (
    <section className="py-20 px-5 md:px-16 border-y border-outline-variant/10 bg-background">
      <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity:0, y:20 }} whileInView={{ opacity:1, y:0 }} viewport={{ once:true }} transition={{ delay: i * 0.1 }} whileHover={{ y: -4 }}
            className="glass-card rounded-xl p-6 flex flex-col items-center text-center gap-3">
            <div className={`w-12 h-12 rounded-full ${s.bg} flex items-center justify-center border ${s.border}`}>
              <s.icon size={22} className={s.color}/>
            </div>
            <div className={`font-display font-bold text-3xl ${s.color}`}>
              <AnimatedNumber target={s.value} suffix={s.suffix} />
            </div>
            <div className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">{s.label}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
