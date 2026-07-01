import { useProfile } from '../hooks/useProfile';
import { Download, ExternalLink, Printer } from 'lucide-react';
import { useSkills } from '../hooks/useSkills';
import { useQuery } from '@tanstack/react-query';
import { getExperience } from '../api/experience';
import { getAchievements } from '../api/achievements';

export default function ResumePage() {
  const { data: profile } = useProfile();
  const { data: skills } = useSkills();
  const { data: experiences } = useQuery({ queryKey: ['experience'], queryFn: getExperience });
  const { data: achievements } = useQuery({ queryKey: ['achievements'], queryFn: getAchievements });

  const topSkills = skills?.slice(0,10).map(s=>s.name).join(', ') || 'React, Node.js, Python, PostgreSQL, Docker';
  
  const sectionsList = [
    { title: 'OBJECTIVE', content: <p className="font-body text-on-surface-variant print:text-gray-700">{profile?.bio || 'Passionate CS engineer seeking impactful roles.'}</p> },
    { title: 'EDUCATION', content: <div><div className="flex justify-between"><span className="font-body font-semibold text-on-surface print:text-black">{profile?.degree || 'B.Tech CSE'}</span><span className="font-mono text-xs text-primary print:text-indigo-600">2024—{profile?.graduation_year||2028}</span></div><p className="font-body text-sm text-on-surface-variant print:text-gray-700">{profile?.university} · CGPA {profile?.cgpa}</p></div> }
  ];

  if (experiences && experiences.length > 0) {
    sectionsList.push({
      title: 'EXPERIENCE',
      content: (
        <div className="space-y-4">
          {experiences.map(exp => (
            <div key={exp.id}>
              <div className="flex justify-between">
                <span className="font-body font-semibold text-on-surface print:text-black">{exp.role} @ {exp.company}</span>
                <span className="font-mono text-xs text-primary print:text-indigo-600">
                  {exp.start_date ? exp.start_date.substring(0, 7) : ''} — {exp.is_current ? 'Present' : (exp.end_date ? exp.end_date.substring(0, 7) : '')}
                </span>
              </div>
              {exp.description && (
                <ul className="list-disc list-inside mt-1 space-y-0.5">
                  {exp.description.split('\n').filter(Boolean).map((line, idx) => (
                    <li key={idx} className="font-body text-xs text-on-surface-variant print:text-gray-700">{line}</li>
                  ))}
                </ul>
              )}
              {exp.tech_used && exp.tech_used.length > 0 && (
                <p className="font-mono text-[10px] text-primary/70 mt-1">Tech Stack: {Array.isArray(exp.tech_used) ? exp.tech_used.join(', ') : exp.tech_used}</p>
              )}
            </div>
          ))}
        </div>
      )
    });
  }

  if (achievements && achievements.length > 0) {
    sectionsList.push({
      title: 'ACHIEVEMENTS',
      content: (
        <div className="space-y-3">
          {achievements.map(ach => (
            <div key={ach.id} className="flex justify-between items-start gap-4">
              <div>
                <span className="font-body font-semibold text-on-surface print:text-black">{ach.title}</span>
                {ach.description && <p className="font-body text-xs text-on-surface-variant print:text-gray-700 mt-0.5">{ach.description}</p>}
              </div>
              <span className="font-mono text-xs text-primary print:text-indigo-600 shrink-0">{ach.date}</span>
            </div>
          ))}
        </div>
      )
    });
  }

  sectionsList.push({ title: 'SKILLS', content: <p className="font-mono text-sm text-on-surface-variant print:text-gray-700">{topSkills}</p> });
  sectionsList.push({ title: 'AVAILABLE FOR', content: <p className="font-body text-on-surface-variant print:text-gray-700">{profile?.available_for || 'SDE Internships, Research Roles, Open Source'}</p> });

  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-4xl mx-auto">
        {/* Action Bar */}
        <div className="glass-card rounded-xl p-4 mb-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20"><span className="text-primary text-lg">📄</span></div>
            <div><div className="font-mono text-sm text-on-surface font-semibold">Resume.pdf</div><div className="font-mono text-[10px] text-on-surface-variant">Last updated: June 2024</div></div>
          </div>
          <div className="flex gap-3">
            <a href={profile?.resume_url || '#'} download className="btn-primary py-2 px-5"><Download size={16}/>Download PDF</a>
            <a href={profile?.resume_url || '#'} target="_blank" rel="noopener noreferrer" className="btn-outline py-2 px-5"><ExternalLink size={16}/>Open Tab</a>
            <button onClick={() => window.print()} className="btn-outline py-2 px-5"><Printer size={16}/>Print</button>
          </div>
        </div>

        {/* Resume Content */}
        <div id="resume-print" className="glass-card rounded-xl p-8 md:p-12 print:bg-white print:shadow-none print:text-black space-y-8">
          {/* Header */}
          <div className="text-center border-b border-white/10 pb-6 print:border-gray-300">
            <h1 className="font-display font-bold text-3xl text-on-surface print:text-black">{profile?.name || 'Pradipta Chandra Giri'}</h1>
            <p className="font-mono text-sm text-primary print:text-indigo-600 mt-1">{profile?.degree || 'B.Tech CSE'} | {profile?.university || 'ITE'}</p>
            <div className="flex justify-center gap-4 mt-3 flex-wrap">
              {[profile?.email, profile?.github && 'GitHub', profile?.linkedin && 'LinkedIn'].filter(Boolean).map(l=><span key={l} className="font-mono text-xs text-on-surface-variant print:text-gray-600">{l}</span>)}
            </div>
          </div>

          {/* Sections */}
          {sectionsList.map(({title, content}) => (
            <div key={title}>
              <h2 className="font-display font-bold text-sm uppercase tracking-widest text-primary print:text-indigo-600 mb-2 border-b border-primary/20 print:border-indigo-200 pb-1">{title}</h2>
              {content}
            </div>
          ))}
        </div>
      </div>
      <style>{`@media print { body { background: white !important; } .glass-card { background: white !important; box-shadow: none !important; } nav, header, footer { display: none !important; } }`}</style>
    </div>
  );
}
