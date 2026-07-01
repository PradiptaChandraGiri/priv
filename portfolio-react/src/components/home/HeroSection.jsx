import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Download, Code2, ChevronDown } from 'lucide-react';
import { Github, Linkedin, Twitter } from '../icons/BrandIcons';

const roles = ['Full Stack Developer', 'ML Enthusiast', 'System Architect', 'Open Source Contributor'];

export default function HeroSection({ profile }) {
  const [roleIdx, setRoleIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);
  const [displayText, setDisplayText] = useState('');

  useEffect(() => {
    const curr = roles[roleIdx];
    const speed = deleting ? 40 : 80;
    const timer = setTimeout(() => {
      if (!deleting) {
        setDisplayText(curr.slice(0, charIdx + 1));
        if (charIdx + 1 === curr.length) setTimeout(() => setDeleting(true), 2000);
        else setCharIdx(c => c + 1);
      } else {
        setDisplayText(curr.slice(0, charIdx - 1));
        if (charIdx - 1 === 0) { setDeleting(false); setRoleIdx(i => (i + 1) % roles.length); setTimeout(() => setCharIdx(0), 400); }
        else setCharIdx(c => c - 1);
      }
    }, speed);
    return () => clearTimeout(timer);
  }, [charIdx, deleting, roleIdx]);

  const socials = [
    { href: profile?.github || '#', icon: Github, label: 'GitHub' },
    { href: profile?.linkedin || '#', icon: Linkedin, label: 'LinkedIn' },
    { href: profile?.twitter || '#', icon: Twitter, label: 'Twitter' },
    { href: profile?.leetcode || '#', icon: Code2, label: 'LeetCode' },
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-16 pb-12 px-5 md:px-16 overflow-hidden">
      {/* Animated orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-float-slow pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-secondary/10 rounded-full blur-3xl animate-float-med pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 w-72 h-72 bg-accent/8 rounded-full blur-3xl animate-float-fast pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center w-full">
        {/* Text */}
        <motion.div className="flex flex-col gap-6 order-2 md:order-1 text-center md:text-left" initial={{ opacity: 0, x: -40 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/20 w-fit mx-auto md:mx-0 font-mono text-xs">
            <span>⚡</span> Hello, I'm
          </motion.div>
          <div>
            <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="font-display font-bold text-4xl md:text-6xl text-on-surface mb-2">
              {profile?.name?.split(' ')[0] || 'Pradipta'} <span className="gradient-text">{profile?.name?.split(' ').slice(1).join(' ') || 'Chandra'}</span>
            </motion.h1>
            <motion.h2 initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="font-display text-xl md:text-2xl text-on-surface-variant h-8 flex items-center justify-center md:justify-start gap-1">
              {displayText}<span className="animate-blink text-primary">|</span>
            </motion.h2>
          </div>
          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} className="font-body text-on-surface-variant max-w-xl leading-relaxed">
            {profile?.bio?.slice(0, 160) || 'CS Engineering student specializing in scalable architectures and ML integrations.'}...
          </motion.p>
          {/* Stats */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="flex gap-6 justify-center md:justify-start glass-panel rounded-xl p-4 w-fit mx-auto md:mx-0">
            <div className="text-center px-4 border-r border-outline-variant/30"><div className="font-display font-bold text-2xl text-primary">12+</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">Projects</div></div>
            <div className="text-center px-4 border-r border-outline-variant/30"><div className="font-display font-bold text-2xl text-tertiary">8+</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">Certs</div></div>
            <div className="text-center px-4"><div className="font-display font-bold text-2xl text-secondary">{profile?.cgpa || '8.9'}</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">CGPA</div></div>
          </motion.div>
          {/* CTAs */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.7 }} className="flex flex-wrap gap-4 justify-center md:justify-start">
            <Link to="/projects" className="btn-primary shadow-glow-sm"><span>View My Work</span><ArrowRight size={16}/></Link>
            <a href={profile?.resume_url || '#'} className="btn-outline"><Download size={16}/><span>Download Resume</span></a>
          </motion.div>
          {/* Social icons */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }} className="flex gap-3 justify-center md:justify-start">
            {socials.map(s => (
              <a key={s.label} href={s.href} target="_blank" rel="noopener noreferrer" title={s.label}
                className="w-11 h-11 glass-panel rounded-full flex items-center justify-center text-on-surface-variant hover:text-primary hover:border-primary/40 hover:-translate-y-1 hover:shadow-glow-sm transition-all">
                <s.icon size={18}/>
              </a>
            ))}
          </motion.div>
        </motion.div>
        {/* Profile Photo */}
        <motion.div className="order-1 md:order-2 flex justify-center" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.7 }}>
          <div className="w-64 h-64 md:w-80 md:h-80 rounded-full p-2 bg-gradient-to-tr from-primary to-secondary animate-pulse-ring">
            <img src={profile?.profile_image_url} alt={profile?.name} loading="lazy" className="w-full h-full rounded-full object-cover border-4 border-surface" onError={e => { e.target.style.display='none'; }} />
          </div>
        </motion.div>
      </div>
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-50">
        <span className="font-mono text-[9px] uppercase tracking-widest text-on-surface-variant">Scroll</span>
        <ChevronDown size={20} className="text-on-surface-variant animate-bounce" />
      </div>
    </section>
  );
}
