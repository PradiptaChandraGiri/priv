import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion, useInView } from 'framer-motion';
import { 
  Home, ChevronRight, Terminal, Cpu, Code2, Globe, Layers, Server, Database 
} from 'lucide-react';
import { useSkills } from '../hooks/useSkills';
import { useProjects } from '../hooks/useProjects';
import SkeletonCard from '../components/ui/SkeletonCard';

const skillConfig = {
  'Python': { color: 'text-cyan-400', bg: 'bg-cyan-500/10', border: 'hover:border-cyan-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(34,211,238,0.15)]' },
  'C++': { color: 'text-blue-400', bg: 'bg-blue-500/10', border: 'hover:border-blue-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(96,165,250,0.15)]' },
  'JavaScript': { color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'hover:border-yellow-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(250,204,21,0.15)]' },
  'React.js': { color: 'text-cyan-400', bg: 'bg-cyan-500/10', border: 'hover:border-cyan-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(34,211,238,0.15)]' },
  'HTML5 / CSS3': { color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'hover:border-orange-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(251,146,60,0.15)]' },
  'Tailwind CSS': { color: 'text-teal-400', bg: 'bg-teal-500/10', border: 'hover:border-teal-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(45,212,191,0.15)]' },
  'Node.js / Express': { color: 'text-green-400', bg: 'bg-green-500/10', border: 'hover:border-green-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(74,222,128,0.15)]' },
  'Flask': { color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'hover:border-emerald-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(52,211,153,0.15)]' },
  'MySQL': { color: 'text-sky-400', bg: 'bg-sky-500/10', border: 'hover:border-sky-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(56,189,248,0.15)]' },
  'Firebase': { color: 'text-amber-500', bg: 'bg-amber-500/10', border: 'hover:border-amber-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]' },
  'C': { color: 'text-indigo-400', bg: 'bg-indigo-500/10', border: 'hover:border-indigo-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(129,140,248,0.15)]' },
  'Java': { color: 'text-red-400', bg: 'bg-red-500/10', border: 'hover:border-red-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(248,113,113,0.15)]' },
  'SQL': { color: 'text-purple-400', bg: 'bg-purple-500/10', border: 'hover:border-purple-500/30', shadow: 'hover:shadow-[0_0_20px_rgba(192,132,252,0.15)]' },
};

const getSkillConfig = (name) => {
  return skillConfig[name] || { color: 'text-primary', bg: 'bg-primary/10', border: 'hover:border-primary/30', shadow: 'hover:shadow-[0_0_20px_rgba(99,102,241,0.15)]' };
};

const iconMap = {
  'Python': Terminal,
  'C++': Cpu,
  'JavaScript': Code2,
  'React.js': Layers,
  'HTML5 / CSS3': Globe,
  'Tailwind CSS': Layers,
  'Node.js / Express': Server,
  'Flask': Server,
  'MySQL': Database,
  'Firebase': Database,
  'C': Cpu,
  'Java': Code2,
  'SQL': Database,
};

const getIcon = (name, category) => {
  if (iconMap[name]) return iconMap[name];
  if (category === 'Languages') return Terminal;
  if (category === 'Frontend') return Globe;
  if (category === 'Backend') return Server;
  if (category === 'Databases') return Database;
  return Code2;
};

function SkillCard({ skill, projects, delay }) {
  const Icon = getIcon(skill.name, skill.category);
  const cfg = getSkillConfig(skill.name);
  const radius = 14;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (skill.proficiency / 100) * circumference;

  const relatedProjects = projects?.filter(p => 
    p.tech_stack?.some(t => {
      const tLower = t.toLowerCase();
      const sLower = skill.name.toLowerCase();
      return tLower === sLower || tLower.includes(sLower) || sLower.includes(tLower);
    })
  ) || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay }}
      whileHover={{ y: -4 }}
      className={`glass-card rounded-xl p-5 flex flex-col justify-between border border-white/5 bg-surface/30 backdrop-blur-md hover:bg-surface/50 ${cfg.border} ${cfg.shadow} transition-all duration-300 group cursor-pointer h-full`}
    >
      <div>
        <div className="flex items-start justify-between mb-4">
          <div className={`w-12 h-12 rounded-xl ${cfg.bg} flex items-center justify-center ${cfg.color} border border-white/5 transition-transform duration-300 group-hover:scale-110 shadow-inner`}>
            <Icon size={24} />
          </div>
          <div className="relative w-10 h-10 flex items-center justify-center" title={`Proficiency: ${skill.proficiency}%`}>
            <svg className="w-10 h-10 transform -rotate-90">
              <circle cx="20" cy="20" r={radius} className="text-white/5" strokeWidth="2.5" stroke="currentColor" fill="transparent" />
              <circle cx="20" cy="20" r={radius} className={cfg.color} strokeWidth="2.5" stroke="currentColor" fill="transparent"
                      strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" />
            </svg>
            <span className="absolute font-mono text-[9px] font-bold text-on-surface/80">{skill.proficiency}%</span>
          </div>
        </div>
        <div>
          <h3 className="font-display font-semibold text-on-surface text-base group-hover:text-primary transition-colors">{skill.name}</h3>
          <span className="font-mono text-[9px] uppercase tracking-wider text-on-surface-variant opacity-60">{skill.category}</span>
        </div>
      </div>
      
      {relatedProjects.length > 0 && (
        <div className="mt-4 border-t border-white/5 pt-3">
          <span className="font-mono text-[8px] uppercase tracking-wider text-on-surface-variant opacity-60 block mb-1.5">Used In</span>
          <div className="flex flex-wrap gap-1">
            {relatedProjects.map(proj => (
              <span key={proj.id} className="font-sans text-[9px] font-semibold px-2 py-0.5 bg-white/5 hover:bg-primary/10 text-on-surface/80 hover:text-primary rounded border border-white/5 hover:border-primary/20 transition-all">
                {proj.title}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

function SkillBar({ skill }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  const cfg = getSkillConfig(skill.name);
  return (
    <div ref={ref} className="space-y-2 p-4 rounded-xl border border-white/5 bg-surface/20 backdrop-blur-sm">
      <div className="flex justify-between items-center font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">
        <span className="flex items-center gap-1.5 font-bold text-on-surface"><span className={cfg.color}>●</span> {skill.name}</span>
        <span className="text-primary font-bold">{skill.proficiency}%</span>
      </div>
      <div className="h-2 bg-surface-container rounded-full overflow-hidden p-0.5 border border-white/5">
        <motion.div 
          className="h-full bg-gradient-to-r from-primary via-secondary to-tertiary rounded-full shadow-[0_0_10px_rgba(192,193,255,0.5)]" 
          initial={{ width: 0 }} 
          animate={{ width: inView ? `${skill.proficiency}%` : 0 }} 
          transition={{ duration: 1.4, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}

export default function SkillsPage() {
  const { data: skills, isLoading: skillsLoading } = useSkills();
  const { data: projects, isLoading: projectsLoading } = useProjects();
  
  const categories = skills ? [...new Set(skills.map(s => s.category))] : [];
  
  // Custom category sorting order
  const catOrder = ['Languages', 'Frontend', 'Backend', 'Databases', 'Other'];
  const sortedCategories = categories.sort((a, b) => {
    const idxA = catOrder.indexOf(a);
    const idxB = catOrder.indexOf(b);
    if (idxA === -1) return 1;
    if (idxB === -1) return -1;
    return idxA - idxB;
  });

  const isLoading = skillsLoading || projectsLoading;

  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-secondary/10 pointer-events-none" />
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3">
            <Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link>
            <ChevronRight size={12}/>
            <span className="text-primary">Skills</span>
          </nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Skills & Technologies</h1>
          <p className="font-body text-on-surface-variant">Technologies I build with daily.</p>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[1,2,3,4,5,6,7,8].map(i => <SkeletonCard key={i} height="h-24"/>)}
          </div>
        ) : (
          <>
            {sortedCategories.map(cat => (
              <div key={cat} className="mb-12">
                <div className="flex items-center gap-3 mb-6">
                  <h2 className="font-display font-bold text-2xl text-on-surface">{cat}</h2>
                  <div className="h-[1px] bg-white/10 flex-1" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {skills.filter(s => s.category === cat).map((s, i) => (
                    <SkillCard key={s.id} skill={s} projects={projects} delay={i * 0.05} />
                  ))}
                </div>
              </div>
            ))}

            <div className="mt-16">
              <div className="flex items-center gap-3 mb-8">
                <h2 className="font-display font-bold text-2xl text-on-surface">Proficiency Overview</h2>
                <div className="h-[1px] bg-white/10 flex-1" />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[...skills]
                  .sort((a, b) => b.proficiency - a.proficiency)
                  .map(s => <SkillBar key={s.id} skill={s} />)}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
