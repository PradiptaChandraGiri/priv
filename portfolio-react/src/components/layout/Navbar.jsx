import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Menu, X, FileText } from 'lucide-react';
import { useThemeStore } from '../../store/themeStore';

const links = [
  { to: '/', label: 'Home' },
  { to: '/projects', label: 'Projects' },
  { to: '/certificates', label: 'Certificates' },
  { to: '/research', label: 'Research' },
  { to: '/coding', label: 'Coding' },
  { to: '/skills', label: 'Skills' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
];

export default function Navbar() {
  const { isDark, toggle } = useThemeStore();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const loc = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => { setMenuOpen(false); }, [loc.pathname]);

  const isActive = (to) => to === '/' ? loc.pathname === '/' : loc.pathname.startsWith(to);

  return (
    <>
      <header className={`fixed top-0 w-full z-50 transition-all duration-300 border-b border-white/10 bg-surface/60 backdrop-blur-xl ${scrolled ? 'shadow-[0_4px_24px_rgba(0,0,0,0.4)]' : ''}`}>
        <div className="flex justify-between items-center h-16 px-5 md:px-16 max-w-7xl mx-auto">
          <Link to="/" className="font-display font-bold text-2xl bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent">BTech Portfolio</Link>
          <nav className="hidden md:flex items-center gap-6">
            {links.map(l => (
              <Link key={l.to} to={l.to} className={`font-mono text-[11px] uppercase tracking-wider transition-colors duration-300 px-2 py-1 ${isActive(l.to) ? 'text-primary font-semibold border-b-2 border-primary pb-0' : 'text-on-surface-variant hover:text-primary'}`}>{l.label}</Link>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <button onClick={toggle} className="p-2 rounded-full text-on-surface-variant hover:text-primary transition-all duration-300 hover:rotate-180">
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            <Link to="/resume" className="hidden md:flex p-2 rounded-full text-on-surface-variant hover:text-primary transition-all"><FileText size={18} /></Link>
            <Link to="/contact" className="hidden md:block bg-primary text-on-primary font-mono text-[11px] uppercase tracking-wider px-5 py-2 rounded-full hover:bg-primary-light transition-all hover:shadow-glow-sm font-semibold">Hire Me</Link>
            <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2 text-on-surface-variant hover:text-primary transition-colors">
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {menuOpen && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-40 md:hidden">
            <div className="absolute inset-0 bg-background/90 backdrop-blur-md" onClick={() => setMenuOpen(false)} />
            <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }} transition={{ type: 'tween', duration: 0.3 }}
              className="absolute right-0 top-0 h-full w-72 bg-surface-container border-l border-outline-variant/30 flex flex-col p-6 pt-20">
              {links.map(l => (
                <Link key={l.to} to={l.to} className={`py-3 border-b border-outline-variant/20 font-mono text-[11px] uppercase tracking-wider transition-colors ${isActive(l.to) ? 'text-primary font-bold' : 'text-on-surface-variant hover:text-primary'}`}>{l.label}</Link>
              ))}
              <Link to="/resume" className="py-3 border-b border-outline-variant/20 font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors">Resume</Link>
              <Link to="/contact" className="mt-6 bg-primary text-on-primary px-4 py-3 rounded-lg font-mono text-[11px] uppercase tracking-wider text-center hover:bg-primary-light transition-all font-semibold">Hire Me</Link>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
