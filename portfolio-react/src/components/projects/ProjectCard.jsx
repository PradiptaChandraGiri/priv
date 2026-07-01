import { useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Info } from 'lucide-react';
import { Github } from '../icons/BrandIcons';
import Badge from '../ui/Badge';
import Modal from '../ui/Modal';

const catColor = { web:'primary', ml:'secondary', systems:'tertiary', mobile:'accent' };
const statusColor = { completed:'success', ongoing:'warning', archived:'neutral' };

export default function ProjectCard({ project: p, delay=0 }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}} whileHover={{y:-6,scale:1.01}}
        className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300 cursor-pointer group" onClick={() => setOpen(true)}>
        <div className="relative h-44 overflow-hidden">
          {(p.thumbnail_url || p.thumbnail) ? <img src={p.thumbnail_url || p.thumbnail} alt={p.title} loading="lazy" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
            : <div className="h-full bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center"><span className="font-display font-bold text-6xl text-primary/30">{p.title[0]}</span></div>}
          <div className="absolute inset-0 bg-gradient-to-t from-surface-container/90 to-transparent"/>
          <div className="absolute top-3 left-3"><Badge variant={catColor[p.category]||'primary'}>{p.category}</Badge></div>
          {p.featured && <div className="absolute top-3 right-3"><Badge variant="warning">⭐ Featured</Badge></div>}
        </div>
        <div className="p-5 flex flex-col flex-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-display font-semibold text-on-surface">{p.title}</h3>
            <Badge variant={statusColor[p.status]||'neutral'} size="sm">{p.status}</Badge>
          </div>
          <p className="font-body text-sm text-on-surface-variant mb-4 flex-1 line-clamp-2">{p.description}</p>
          <div className="flex flex-wrap gap-1.5 mb-4">{p.tech_stack?.slice(0,4).map(t => <span key={t} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full">{t}</span>)}</div>
          <div className="flex items-center gap-3 border-t border-white/10 pt-3 mt-auto" onClick={e => e.stopPropagation()}>
            {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><Github size={16}/></a>}
            {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><ExternalLink size={16}/></a>}
            <button className="ml-auto font-mono text-[10px] uppercase tracking-wider text-primary flex items-center gap-1 hover:text-primary-light transition-colors"><Info size={14}/> Details</button>
          </div>
        </div>
      </motion.div>
 
      <Modal open={open} onClose={() => setOpen(false)} title={p.title}>
        <div className="space-y-4">
          {(p.thumbnail_url || p.thumbnail) && <img src={p.thumbnail_url || p.thumbnail} alt={p.title} className="w-full h-48 object-cover rounded-lg mb-4"/>}
          <div className="flex gap-2 flex-wrap"><Badge variant={catColor[p.category]||'primary'}>{p.category}</Badge><Badge variant={statusColor[p.status]||'neutral'}>{p.status}</Badge></div>
          <p className="font-body text-on-surface-variant">{p.description}</p>
          <div><p className="font-mono text-[10px] uppercase tracking-wider text-primary mb-2">Tech Stack</p><div className="flex flex-wrap gap-2">{p.tech_stack?.map(t => <span key={t} className="font-mono text-xs px-3 py-1 bg-primary/10 text-primary border border-primary/20 rounded-full">{t}</span>)}</div></div>
          <div className="flex gap-3 pt-2">
            {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="btn-outline flex items-center gap-2 text-sm"><Github size={16}/> View Source</a>}
            {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="btn-primary flex items-center gap-2 text-sm"><ExternalLink size={16}/> Live Demo</a>}
          </div>
        </div>
      </Modal>
    </>
  );
}
