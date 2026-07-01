import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useSkills } from '../../hooks/useSkills';
import SectionHeader from '../ui/SectionHeader';

export default function SkillsPreview() {
  const { data: skills } = useSkills();
  const top = skills?.slice(0, 12) || [];
  return (
    <section className="py-20 px-5 md:px-16 border-y border-outline-variant/10">
      <div className="max-w-7xl mx-auto">
        <SectionHeader title="My Tech Stack" subtitle="Technologies I work with daily" viewAll="View All Skills" viewAllLink="/skills" />
        <div className="flex flex-wrap justify-center gap-3">
          {top.map((s, i) => (
            <motion.div key={s.id} initial={{opacity:0,y:10}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.05}} whileHover={{y:-4,scale:1.05}}
              className="glass-panel px-4 py-2.5 rounded-full flex items-center gap-2 cursor-pointer hover:border-primary/40 hover:shadow-glow-sm transition-all">
              <span className="text-lg">{s.icon}</span>
              <span className="font-mono text-xs text-primary">{s.name}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
