import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ExternalLink, ArrowRight } from 'lucide-react';
import { Github } from '../icons/BrandIcons';
import { useProjects } from '../../hooks/useProjects';
import SkeletonCard from '../ui/SkeletonCard';
import Badge from '../ui/Badge';
import SectionHeader from '../ui/SectionHeader';

const catColor = { web:'primary', ml:'secondary', systems:'tertiary', mobile:'accent' };

export default function FeaturedProjects() {
  const { data: projects, isLoading } = useProjects({ featured: true });
  return (
    <section className="py-20 px-5 md:px-16 bg-surface/30">
      <div className="max-w-7xl mx-auto">
        <SectionHeader title="Featured Projects" subtitle="A selection of my most impactful technical work" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {isLoading ? [1,2,3].map(i => <SkeletonCard key={i}/>) : projects?.slice(0,3).map((p, i) => (
            <motion.div key={p.id} initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.1}} whileHover={{y:-6, scale:1.01}}
              className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300 border-t-4"
              style={{borderTopColor: p.category==='ml'?'#d0bcff':p.category==='systems'?'#ffb783':'#c0c1ff'}}>
              {(p.thumbnail_url || p.thumbnail) && <img src={p.thumbnail_url || p.thumbnail} alt={p.title} loading="lazy" className="h-40 w-full object-cover opacity-80"/>}
              {!(p.thumbnail_url || p.thumbnail) && <div className="h-40 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center"><span className="font-display font-bold text-5xl text-primary/40">{p.title[0]}</span></div>}
              <div className="p-5 flex flex-col flex-1">
                <Badge variant={catColor[p.category]||'primary'} className="mb-2 w-fit">{p.category}</Badge>
                <h3 className="font-display font-semibold text-on-surface mb-2">{p.title}</h3>
                <p className="font-body text-sm text-on-surface-variant mb-4 flex-1 line-clamp-2">{p.description}</p>
                <div className="flex flex-wrap gap-1.5 mb-4">{p.tech_stack?.slice(0,3).map(t => <span key={t} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full uppercase">{t}</span>)}</div>
                <div className="flex items-center gap-3 border-t border-white/10 pt-3 mt-auto">
                  {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><Github size={16}/></a>}
                  {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><ExternalLink size={16}/></a>}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        <div className="text-center"><Link to="/projects" className="btn-outline mx-auto w-fit">View All Projects <ArrowRight size={14}/></Link></div>
      </div>
    </section>
  );
}
