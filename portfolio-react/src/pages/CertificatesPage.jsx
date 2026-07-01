import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home, ChevronRight } from 'lucide-react';
import { useCertificates } from '../hooks/useCertificates';
import CertificateCard from '../components/certificates/CertificateCard';
import SkeletonCard from '../components/ui/SkeletonCard';

const cats = ['All', 'Cloud', 'AI/ML', 'Web Dev', 'DSA', 'Core CS', 'Other'];

export default function CertificatesPage() {
  const [cat, setCat] = useState('All');
  const { data: certs, isLoading } = useCertificates(cat !== 'All' ? { category: cat } : {});
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12">
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Certificates</span></nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Certifications & Credentials</h1>
          <p className="font-body text-on-surface-variant">Verified achievements from world-class platforms.</p>
        </div>
        {/* Filter */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 mb-8">
          {cats.map(c=><button key={c} onClick={()=>setCat(c)} className={`whitespace-nowrap px-5 py-2 rounded-full font-mono text-[10px] uppercase tracking-wider border transition-all ${cat===c?'bg-primary/20 text-primary border-primary/40 shadow-glow-sm':'bg-white/5 text-on-surface-variant border-white/10 hover:bg-white/10'}`}>{c}</button>)}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? [1,2,3,4,5,6].map(i=><SkeletonCard key={i}/>) : certs?.map((c,i)=><CertificateCard key={c.id} cert={c} delay={i*0.05}/>)}
        </div>
      </div>
    </div>
  );
}
