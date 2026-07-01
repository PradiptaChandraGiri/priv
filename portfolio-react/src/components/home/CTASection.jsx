import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, FileText } from 'lucide-react';
export default function CTASection({ profile }) {
  return (
    <section className="py-20 px-5 md:px-16" style={{background:'linear-gradient(135deg,rgba(192,193,255,0.08),rgba(208,188,255,0.08))'}}>
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} className="flex flex-col md:flex-row items-center justify-between gap-8 text-center md:text-left">
          <div>
            <h2 className="font-display font-bold text-3xl md:text-4xl text-on-surface mb-3">Open to <span className="gradient-text">Opportunities</span></h2>
            <p className="font-body text-on-surface-variant max-w-lg">{profile?.available_for || 'SDE Internships, Research Roles, Open Source Contributions'}</p>
          </div>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link to="/contact" className="btn-primary shadow-glow-sm"><Mail size={16}/><span>Get In Touch</span></Link>
            <Link to="/resume" className="btn-outline"><FileText size={16}/><span>View Resume</span></Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
