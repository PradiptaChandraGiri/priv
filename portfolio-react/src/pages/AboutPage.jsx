import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Home, ChevronRight, MapPin, Download, Mail, GraduationCap } from 'lucide-react';
import { useProfile } from '../hooks/useProfile';
import Badge from '../components/ui/Badge';

const interests = [
  { icon:'🌐', title:'Web Development', desc:'Full-stack apps with React & Node.js' },
  { icon:'🧠', title:'Machine Learning', desc:'Deep learning and model deployment' },
  { icon:'⚙️', title:'System Design', desc:'Scalable distributed systems' },
  { icon:'📖', title:'Open Source', desc:'Contributing to OSS projects' },
  { icon:'🏆', title:'Competitive Programming', desc:'LeetCode, Codeforces' },
  { icon:'🔬', title:'Research', desc:'AI & systems research' },
];

export default function AboutPage() {
  const { data: profile } = useProfile();
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Intro */}
        <div className="glass-card rounded-xl p-8 mb-12 grid grid-cols-1 md:grid-cols-5 gap-8 items-center">
          <div className="md:col-span-2 flex justify-center">
            <div className="w-64 h-64 rounded-xl overflow-hidden border-2 border-primary/30 shadow-glow">
              <img src={profile?.profile_image_url} alt={profile?.name} className="w-full h-full object-cover"/>
            </div>
          </div>
          <div className="md:col-span-3 space-y-4">
            <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">About</span></nav>
            <h1 className="font-display font-bold text-3xl md:text-4xl text-on-surface">{profile?.name || 'Pradipta Chandra Giri'}</h1>
            <p className="font-mono text-sm text-primary">Full Stack Developer | BTech CSE</p>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse"/>
              <Badge variant="success">Open to Work</Badge>
            </div>
            <p className="font-body text-on-surface-variant">{profile?.bio || 'Passionate CS undergrad building scalable systems.'}</p>
            <div className="flex items-center gap-2 font-mono text-xs text-on-surface-variant"><MapPin size={14}/>{profile?.location || 'Bhubaneswar, Odisha, India'}</div>
            <div className="flex gap-3 flex-wrap">
              <a href={profile?.resume_url||'#'} className="btn-primary py-2 px-5"><Download size={14}/>Download Resume</a>
              <Link to="/contact" className="btn-outline py-2 px-5"><Mail size={14}/>Contact Me</Link>
            </div>
          </div>
        </div>

        {/* Education */}
        <div className="mb-12">
          <h2 className="font-display font-bold text-2xl gradient-text mb-6 flex items-center gap-2"><GraduationCap size={24}/>Education</h2>
          <div className="glass-card rounded-xl p-6 border-l-4 border-primary">
            <div className="flex flex-col md:flex-row md:justify-between md:items-start mb-2">
              <h3 className="font-display font-semibold text-lg text-on-surface">{profile?.degree || 'B.Tech Computer Science & Engineering'}</h3>
              <span className="font-mono text-xs text-primary">2024 — {profile?.graduation_year || 2028}</span>
            </div>
            <p className="font-body text-on-surface-variant mb-3">{profile?.university || 'Institute of Technology & Engineering'}</p>
            <Badge variant="success">CGPA: {profile?.cgpa || '8.9'}/10</Badge>
          </div>
        </div>

        {/* Areas of Interest */}
        <div className="mb-12">
          <h2 className="font-display font-bold text-2xl gradient-text mb-6">Areas of Interest</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {interests.map((item,i)=>(
              <motion.div key={item.title} initial={{opacity:0,y:10}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.05}} whileHover={{y:-4}}
                className="glass-card rounded-xl p-4 text-center hover:border-primary/30 hover:shadow-glow-sm transition-all">
                <div className="text-3xl mb-2">{item.icon}</div>
                <div className="font-display font-semibold text-sm text-on-surface mb-1">{item.title}</div>
                <div className="font-body text-[11px] text-on-surface-variant">{item.desc}</div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Looking For */}
        <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} className="glass-card rounded-xl p-8 border border-primary/20">
          <h2 className="font-display font-bold text-2xl gradient-text mb-3">What I'm Looking For</h2>
          <p className="font-body text-on-surface-variant mb-4">Targeting top-tier tech companies and impactful research opportunities.</p>
          <ul className="space-y-2">
            {['🎯 A fast-learning environment with challenging problems','🌍 Real-world impact and production systems','🤝 Collaborative engineering teams','📈 Growth in both technical depth and breadth'].map(b=>(
              <li key={b} className="flex items-center gap-2 font-body text-on-surface-variant text-sm"><span className="text-lg">{b.slice(0,2)}</span>{b.slice(2)}</li>
            ))}
          </ul>
        </motion.div>
      </div>
    </div>
  );
}
