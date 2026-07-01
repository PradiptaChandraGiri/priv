import { useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Download } from 'lucide-react';
import Badge from '../ui/Badge';
import Modal from '../ui/Modal';

const catColor = { 'AI/ML':'secondary', 'Cloud':'primary', 'Web Dev':'tertiary', 'DSA':'warning', 'Core CS':'neutral' };

export default function CertificateCard({ cert: c, delay=0 }) {
  const [open, setOpen] = useState(false);
  const date = c.issue_date ? new Date(c.issue_date).toLocaleDateString('en-US',{month:'short',year:'numeric'}) : '';
  return (
    <>
      <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}} whileHover={{y:-4}}
        className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300 h-full">
        <div className={`h-1.5 w-full bg-gradient-to-r from-primary to-secondary`}/>
        
        {c.image_url && (
          <div className="h-44 w-full overflow-hidden relative border-b border-outline-variant/10 bg-surface-container-low group">
            <img src={c.image_url} alt={c.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div className="absolute top-3 right-3">
              <Badge variant={catColor[c.category]||'primary'} size="sm">{c.category}</Badge>
            </div>
          </div>
        )}

        <div className="p-5 flex flex-col flex-1 justify-between">
          <div>
            <div className="flex items-start gap-3 mb-3">
              <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center flex-shrink-0 font-display font-bold text-primary text-sm">
                {c.issuing_org?.[0]}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-display font-semibold text-on-surface text-sm leading-tight line-clamp-2">{c.title}</h3>
                <p className="font-mono text-[10px] text-on-surface-variant mt-0.5">{c.issuing_org}</p>
              </div>
              {c.featured && <Badge variant="warning" size="sm">⭐</Badge>}
            </div>

            <div className="flex items-center justify-between mb-3">
              {!c.image_url && <Badge variant={catColor[c.category]||'primary'} size="sm">{c.category}</Badge>}
              {date && <span className="font-mono text-[10px] text-on-surface-variant ml-auto">{date}</span>}
            </div>

            {c.skills_gained?.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-4">
                {c.skills_gained.slice(0,3).map(s => <span key={s} className="font-mono text-[9px] px-2 py-0.5 bg-secondary/10 text-secondary border border-secondary/20 rounded-full">{s}</span>)}
                {c.skills_gained.length > 3 && <span className="font-mono text-[9px] text-on-surface-variant">+{c.skills_gained.length-3}</span>}
              </div>
            )}
          </div>

          <div className="flex items-center gap-2 border-t border-white/10 pt-3 mt-4">
            <button onClick={() => setOpen(true)} className="btn-outline py-1.5 px-3 text-[10px] flex-1">View Certificate</button>
            {c.credential_url && <a href={c.credential_url} target="_blank" rel="noopener noreferrer" className="p-2 text-on-surface-variant hover:text-primary transition-colors" title="Verify"><ExternalLink size={14}/></a>}
          </div>
        </div>
      </motion.div>

      <Modal open={open} onClose={() => setOpen(false)} title={c.title}>
        <div className="space-y-4 text-center">
          {c.image_url ? (
            <div className="my-4 max-h-[60vh] overflow-y-auto rounded-lg border border-outline-variant/30 bg-surface-container-low p-2">
              <img src={c.image_url} alt={c.title} className="w-full h-auto object-contain mx-auto rounded-md shadow-md" />
            </div>
          ) : (
            <div className="w-16 h-16 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto font-display font-bold text-primary text-2xl">{c.issuing_org?.[0]}</div>
          )}
          <div>
            <h3 className="font-display font-semibold text-xl text-on-surface">{c.title}</h3>
            <p className="text-on-surface-variant font-mono text-xs mt-1">{c.issuing_org}</p>
          </div>
          <div className="flex justify-center gap-2">
            <Badge variant={catColor[c.category]||'primary'}>{c.category}</Badge>
            {date && <Badge variant="neutral">{date}</Badge>}
          </div>
          {c.skills_gained?.length > 0 && (
            <div className="flex flex-wrap gap-2 justify-center">
              {c.skills_gained.map(s => <span key={s} className="font-mono text-xs px-3 py-1 bg-secondary/10 text-secondary border border-secondary/20 rounded-full">{s}</span>)}
            </div>
          )}
          {c.credential_url && (
            <a href={c.credential_url} target="_blank" rel="noopener noreferrer" className="btn-primary mx-auto w-fit flex items-center gap-2">
              <ExternalLink size={16}/> Verify Certificate
            </a>
          )}
        </div>
      </Modal>
    </>
  );
}
