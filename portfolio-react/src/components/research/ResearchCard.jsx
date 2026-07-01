import { useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import Badge from '../ui/Badge';

const statusColor = { published:'success', under_review:'warning', preprint:'primary' };
const statusLabel = { published:'Published', under_review:'Under Review', preprint:'Preprint' };

export default function ResearchCard({ paper: p, delay=0 }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}}
      className="glass-card rounded-xl overflow-hidden flex hover:shadow-card transition-all duration-300">
      <div className="w-1.5 flex-shrink-0 bg-gradient-to-b from-primary to-secondary rounded-l-xl"/>
      <div className="p-6 flex-1">
        <div className="flex flex-wrap items-center gap-3 mb-3">
          <Badge variant={statusColor[p.status]||'neutral'}>{statusLabel[p.status]||p.status}</Badge>
          {p.citations > 0 && <span className="font-mono text-[10px] text-on-surface-variant">{p.citations} citations</span>}
        </div>
        <h3 className="font-display font-semibold text-lg text-on-surface mb-2">{p.title}</h3>
        <p className="font-body text-sm text-on-surface-variant mb-1">{p.authors?.join(', ')}</p>
        <p className="font-mono text-xs text-primary italic mb-3">{p.journal} · {p.date ? new Date(p.date).getFullYear() : ''}</p>
        <div className={`font-body text-sm text-on-surface-variant mb-3 ${!expanded ? 'line-clamp-3' : ''}`}>{p.abstract}</div>
        <button onClick={() => setExpanded(!expanded)} className="font-mono text-[10px] uppercase tracking-wider text-primary flex items-center gap-1 hover:text-primary-light transition-colors mb-3">
          {expanded ? <><ChevronUp size={12}/> Show Less</> : <><ChevronDown size={12}/> Read More</>}
        </button>
        {p.keywords?.length > 0 && <div className="flex flex-wrap gap-1.5 mb-4">{p.keywords.map(k=><span key={k} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full">{k}</span>)}</div>}
        <div className="flex gap-3 flex-wrap border-t border-white/10 pt-3">
          {p.paper_url && <a href={p.paper_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><BookOpen size={14}/> Read Paper</a>}
          {p.arxiv_url && <a href={p.arxiv_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><ExternalLink size={14}/> arXiv</a>}
          {p.doi && <a href={`https://doi.org/${p.doi}`} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><ExternalLink size={14}/> DOI</a>}
        </div>
      </div>
    </motion.div>
  );
}
