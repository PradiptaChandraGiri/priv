import { Link } from 'react-router-dom';
import { Home, ChevronRight, Rocket } from 'lucide-react';
import { useResearch } from '../hooks/useResearch';
import ResearchCard from '../components/research/ResearchCard';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function ResearchPage() {
  const { data: papers, isLoading } = useResearch();
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-4xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12">
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Research</span></nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Research & Publications</h1>
          <p className="font-body text-on-surface-variant">Academic work, papers, and contributions to the field.</p>
        </div>
        <div className="space-y-6">
          {isLoading ? [1,2].map(i=><SkeletonCard key={i} height="h-48"/>) : papers?.length === 0 ? (
            <div className="text-center py-20"><Rocket size={48} className="mx-auto text-on-surface-variant/30 mb-4"/><p className="font-mono text-xs text-on-surface-variant uppercase tracking-wider">No publications yet. Research coming soon!</p></div>
          ) : papers?.map((p,i)=><ResearchCard key={p.id} paper={p} delay={i*0.1}/>)}
        </div>
      </div>
    </div>
  );
}
