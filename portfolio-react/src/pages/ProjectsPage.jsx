import { useState } from 'react';
import { motion } from 'framer-motion';
import { Home, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useProjects } from '../hooks/useProjects';
import ProjectCard from '../components/projects/ProjectCard';
import ProjectFilter from '../components/projects/ProjectFilter';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function ProjectsPage() {
  const [cat, setCat] = useState('all');
  const { data: projects, isLoading } = useProjects(cat !== 'all' ? { category: cat } : {});
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="glass-card rounded-xl p-8 mb-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-grid-pattern bg-grid-sm opacity-30"/>
          <div className="relative z-10">
            <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3">
              <Link to="/" className="hover:text-primary transition-colors flex items-center gap-1"><Home size={12}/>Home</Link>
              <ChevronRight size={12}/><span className="text-primary">Projects</span>
            </nav>
            <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">My Projects</h1>
            <p className="font-body text-on-surface-variant">Engineering projects from systems design to ML models.</p>
          </div>
        </div>
        <ProjectFilter active={cat} onChange={setCat} />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? [1,2,3,4,5,6].map(i=><SkeletonCard key={i}/>) : projects?.map((p,i)=><ProjectCard key={p.id} project={p} delay={i*0.05}/>)}
        </div>
        {!isLoading && projects?.length===0 && <div className="text-center py-20 text-on-surface-variant font-mono text-xs">No projects in this category.</div>}
      </div>
    </div>
  );
}
