import { Link } from 'react-router-dom';
import { Code2 } from 'lucide-react';
import { Github, Linkedin, Twitter } from '../icons/BrandIcons';

const quickLinks = [
  { to: '/projects', label: 'Projects' },
  { to: '/certificates', label: 'Certificates' },
  { to: '/research', label: 'Research' },
  { to: '/coding', label: 'Coding' },
  { to: '/contact', label: 'Contact' },
];

const socials = [
  { href: 'https://github.com', icon: Github, label: 'GitHub' },
  { href: 'https://linkedin.com', icon: Linkedin, label: 'LinkedIn' },
  { href: 'https://twitter.com', icon: Twitter, label: 'Twitter' },
  { href: 'https://leetcode.com', icon: Code2, label: 'LeetCode' },
];

export default function Footer() {
  return (
    <footer className="bg-background border-t border-white/10 w-full py-12">
      <div className="max-w-7xl mx-auto px-5 md:px-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div className="flex flex-col gap-3">
            <Link to="/" className="font-display font-bold text-2xl bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent w-fit">BTech Portfolio</Link>
            <p className="font-body text-sm text-on-surface-variant opacity-60 max-w-xs">CS engineering student targeting top-tier tech companies, research institutes, and competitive internship programs.</p>
          </div>
          <div className="flex flex-col gap-2">
            <span className="font-mono text-[11px] uppercase tracking-wider text-primary mb-1">Quick Links</span>
            {quickLinks.map(l => (
              <Link key={l.to} to={l.to} className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit">{l.label}</Link>
            ))}
          </div>
          <div className="flex flex-col gap-2">
            <span className="font-mono text-[11px] uppercase tracking-wider text-primary mb-1">Connect</span>
            {socials.map(s => (
              <a key={s.label} href={s.href} target="_blank" rel="noopener noreferrer"
                className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-all opacity-80 hover:opacity-100 hover:-translate-y-0.5 flex items-center gap-2 w-fit">
                <s.icon size={14} />{s.label}
              </a>
            ))}
          </div>
        </div>
        <div className="border-t border-white/10 pt-6 flex flex-col md:flex-row items-center justify-between gap-2">
          <p className="font-mono text-[10px] text-on-surface-variant opacity-40">© 2024 Engineering Portfolio. Built with ❤️ and React.</p>
          <div className="flex gap-4">
            <a href="#" className="font-mono text-[10px] text-on-surface-variant hover:text-primary transition-colors opacity-40 hover:opacity-100">Privacy</a>
            <a href="#" className="font-mono text-[10px] text-on-surface-variant hover:text-primary transition-colors opacity-40 hover:opacity-100">Terms</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
