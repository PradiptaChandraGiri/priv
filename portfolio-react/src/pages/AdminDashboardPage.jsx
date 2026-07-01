import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Plus, Trash2, Edit3, LayoutDashboard, FolderCode, Award, BookOpen, Cpu, MessageSquare } from 'lucide-react';
import toast from 'react-hot-toast';
import AdminSidebar from '../components/admin/AdminSidebar';
import ProjectForm from '../components/admin/ProjectForm';
import CertificateForm from '../components/admin/CertificateForm';
import ResearchForm from '../components/admin/ResearchForm';
import SkillForm from '../components/admin/SkillForm';
import ProfileForm from '../components/admin/ProfileForm';
import MessageList from '../components/admin/MessageList';
import AchievementForm from '../components/admin/AchievementForm';
import ExperienceForm from '../components/admin/ExperienceForm';
import Modal from '../components/ui/Modal';
import Badge from '../components/ui/Badge';
import { getProjects, createProject, updateProject, deleteProject } from '../api/projects';
import { getCertificates, createCertificate, updateCertificate, deleteCertificate } from '../api/certificates';
import { getResearch, createResearch, updateResearch, deleteResearch } from '../api/research';
import { getSkills, createSkill, updateSkill, deleteSkill } from '../api/skills';
import { getProfile, updateProfile, uploadProfileResume } from '../api/profile';
import { getMessages, markRead } from '../api/contact';
import { getAchievements, createAchievement, updateAchievement, deleteAchievement } from '../api/achievements';
import { getExperience, createExperience, updateExperience, deleteExperience } from '../api/experience';

const stats = [
  { label:'Projects', icon:FolderCode, key:'projects', color:'text-primary' },
  { label:'Certificates', icon:Award, key:'certificates', color:'text-tertiary' },
  { label:'Research', icon:BookOpen, key:'research', color:'text-secondary' },
  { label:'Messages', icon:MessageSquare, key:'messages', color:'text-success' },
];

function DataTable({ data=[], columns, onDelete, onEdit, entityKey }) {
  const qc = useQueryClient();
  const del = useMutation({ mutationFn: onDelete, onSuccess: () => { qc.invalidateQueries([entityKey]); toast.success('Deleted!'); } });
  return (
    <div className="space-y-2 mt-4">
      {data.map(item => (
        <div key={item.id} className="glass-card rounded-xl p-4 flex items-center justify-between hover:border-outline-variant/40 transition-all">
          <div className="flex-1 min-w-0">
            {columns.map(col => (
              <div key={col.key} className={col.primary ? 'font-body font-semibold text-on-surface text-sm' : 'font-mono text-[10px] text-on-surface-variant mt-0.5'}>{item[col.key] ?? ''}</div>
            ))}
          </div>
          <div className="flex items-center gap-1.5 ml-4">
            <button onClick={() => onEdit(item)} className="p-2 text-on-surface-variant hover:text-primary transition-colors"><Edit3 size={16}/></button>
            <button onClick={() => { if(window.confirm(`Delete "${item[columns[0].key]}"?`)) del.mutate(item.id); }} className="p-2 text-on-surface-variant hover:text-error transition-colors"><Trash2 size={16}/></button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default function AdminDashboardPage() {
  const [active, setActive] = useState('overview');
  const [modal, setModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const qc = useQueryClient();

  const projects = useQuery({ queryKey:['projects'], queryFn: getProjects });
  const certificates = useQuery({ queryKey:['certificates'], queryFn: getCertificates });
  const research = useQuery({ queryKey:['research'], queryFn: getResearch });
  const skills = useQuery({ queryKey:['skills'], queryFn: getSkills });
  const messages = useQuery({ queryKey:['messages'], queryFn: getMessages });
  const profile = useQuery({ queryKey:['profile'], queryFn: getProfile });
  const achievements = useQuery({ queryKey:['achievements'], queryFn: getAchievements });
  const experience = useQuery({ queryKey:['experience'], queryFn: getExperience });

  const unread = messages.data?.filter(m=>!m.read).length || 0;
  const counts = { projects: projects.data?.length||0, certificates: certificates.data?.length||0, research: research.data?.length||0, messages: messages.data?.length||0 };

  const addMutation = (fn, key) => useMutation({ mutationFn: fn, onSuccess: () => { qc.invalidateQueries([key]); setModal(false); toast.success('Added!'); } });
  const addProject = addMutation(createProject, 'projects');
  const addCert = addMutation(createCertificate, 'certificates');
  const addResearch = addMutation(createResearch, 'research');
  const addSkill = addMutation(createSkill, 'skills');
  const addAchievement = addMutation(createAchievement, 'achievements');
  const addExperience = addMutation(createExperience, 'experience');

  const editMutation = (fn, key) => useMutation({ 
    mutationFn: ({ id, data }) => fn(id, data), 
    onSuccess: () => { qc.invalidateQueries([key]); setModal(false); setEditingItem(null); toast.success('Updated!'); } 
  });
  const editProject = editMutation(updateProject, 'projects');
  const editCert = editMutation(updateCertificate, 'certificates');
  const editResearch = editMutation(updateResearch, 'research');
  const editSkill = editMutation(updateSkill, 'skills');
  const editAchievement = editMutation(updateAchievement, 'achievements');
  const editExperience = editMutation(updateExperience, 'experience');

  const updateProfileMut = useMutation({ 
    mutationFn: updateProfile, 
    onSuccess: () => { qc.invalidateQueries(['profile']); toast.success('Profile updated!'); } 
  });

  const markReadMut = useMutation({ mutationFn: markRead, onSuccess: () => qc.invalidateQueries(['messages']) });

  const sections = {
    overview: () => (
      <div>
        <h2 className="font-display font-bold text-2xl text-on-surface mb-6">Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map(s=>(
            <motion.div key={s.key} whileHover={{y:-2}} className="glass-card rounded-xl p-5 flex flex-col items-center text-center gap-2">
              <s.icon size={24} className={s.color}/>
              <div className={`font-display font-bold text-3xl ${s.color}`}>{counts[s.key]}</div>
              <div className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    ),
    projects: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Projects</h2>
        <button onClick={() => { setEditingItem(null); setModal('project'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Project</button>
      </div>
      <DataTable data={projects.data||[]} columns={[{key:'title',primary:true},{key:'category'},{key:'status'}]} onDelete={deleteProject} onEdit={(item) => { setEditingItem(item); setModal('project'); }} entityKey="projects"/>
      <Modal open={modal==='project'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Project" : "Add Project"}>
        <ProjectForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editProject.mutate({ id: editingItem.id, data: d }) : addProject.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    certificates: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Certificates</h2>
        <button onClick={() => { setEditingItem(null); setModal('cert'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Certificate</button>
      </div>
      <DataTable data={certificates.data||[]} columns={[{key:'title',primary:true},{key:'issuing_org'},{key:'category'}]} onDelete={deleteCertificate} onEdit={(item) => { setEditingItem(item); setModal('cert'); }} entityKey="certificates"/>
      <Modal open={modal==='cert'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Certificate" : "Add Certificate"}>
        <CertificateForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editCert.mutate({ id: editingItem.id, data: d }) : addCert.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    research: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Research Papers</h2>
        <button onClick={() => { setEditingItem(null); setModal('research'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Paper</button>
      </div>
      <DataTable data={research.data||[]} columns={[{key:'title',primary:true},{key:'journal'},{key:'status'}]} onDelete={deleteResearch} onEdit={(item) => { setEditingItem(item); setModal('research'); }} entityKey="research"/>
      <Modal open={modal==='research'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Research Paper" : "Add Research Paper"}>
        <ResearchForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editResearch.mutate({ id: editingItem.id, data: d }) : addResearch.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    skills: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Skills</h2>
        <button onClick={() => { setEditingItem(null); setModal('skill'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Skill</button>
      </div>
      <DataTable data={skills.data||[]} columns={[{key:'name',primary:true},{key:'category'},{key:'proficiency'}]} onDelete={deleteSkill} onEdit={(item) => { setEditingItem(item); setModal('skill'); }} entityKey="skills"/>
      <Modal open={modal==='skill'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Skill" : "Add Skill"}>
        <SkillForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editSkill.mutate({ id: editingItem.id, data: d }) : addSkill.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    profile: () => (<div>
      <h2 className="font-display font-bold text-2xl text-on-surface mb-6">Profile Settings</h2>
      {profile.isLoading ? (
        <div className="font-mono text-xs text-on-surface-variant">Loading details...</div>
      ) : (
        <ProfileForm onSubmit={d => updateProfileMut.mutate(d)} defaultValues={profile.data}/>
      )}
    </div>),
    messages: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Messages</h2>
        {unread > 0 && <Badge variant="primary">{unread} unread</Badge>}
      </div>
      <MessageList messages={messages.data||[]} onMarkRead={id => markReadMut.mutate(id)}/>
    </div>),
    achievements: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Achievements</h2>
        <button onClick={() => { setEditingItem(null); setModal('achievement'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Achievement</button>
      </div>
      <DataTable data={achievements.data||[]} columns={[{key:'title',primary:true},{key:'date'},{key:'description'}]} onDelete={deleteAchievement} onEdit={(item) => { setEditingItem(item); setModal('achievement'); }} entityKey="achievements"/>
      <Modal open={modal==='achievement'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Achievement" : "Add Achievement"}>
        <AchievementForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editAchievement.mutate({ id: editingItem.id, data: d }) : addAchievement.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    experience: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Experience</h2>
        <button onClick={() => { setEditingItem(null); setModal('experience'); }} className="btn-primary py-2 px-4"><Plus size={16}/>Add Experience</button>
      </div>
      <DataTable data={experience.data||[]} columns={[{key:'company',primary:true},{key:'role'},{key:'start_date'}]} onDelete={deleteExperience} onEdit={(item) => { setEditingItem(item); setModal('experience'); }} entityKey="experience"/>
      <Modal open={modal==='experience'} onClose={() => { setModal(false); setEditingItem(null); }} title={editingItem ? "Edit Experience" : "Add Experience"}>
        <ExperienceForm key={editingItem ? `edit-${editingItem.id}` : 'add'} onSubmit={d => editingItem ? editExperience.mutate({ id: editingItem.id, data: d }) : addExperience.mutate(d)} defaultValues={editingItem || undefined}/>
      </Modal>
    </div>),
    resume: () => {
      const [file, setFile] = useState(null);
      const [uploading, setUploading] = useState(false);
      const handleUpload = async () => {
        if (!file) return toast.error('Select a PDF first');
        setUploading(true);
        try {
          await uploadProfileResume(file);
          toast.success('Resume updated!');
          qc.invalidateQueries(['profile']);
          setFile(null);
        } catch (e) { toast.error(e.response?.data?.message || 'Upload failed'); }
        finally { setUploading(false); }
      };
      return (
        <div>
          <h2 className="font-display font-bold text-2xl text-on-surface mb-6">Resume PDF Management</h2>
          <div className="glass-card p-6 rounded-xl border border-white/5 max-w-xl space-y-6">
            {profile.data?.resume_url && (
              <div className="flex flex-col items-center p-4 bg-surface-container rounded-lg border border-outline-variant/30">
                <span className="text-4xl mb-2">📄</span>
                <span className="font-body text-sm font-semibold text-on-surface mb-2">Currently Active Resume</span>
                <a href={profile.data.resume_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-xs">View Uploaded PDF</a>
              </div>
            )}
            <div className="bg-surface-container border border-dashed border-outline-variant/40 rounded-lg p-8 flex flex-col items-center justify-center text-center cursor-pointer hover:border-primary/40 transition-colors">
              <input type="file" id="resume-tab-file-input" accept=".pdf" className="hidden" onChange={e => setFile(e.target.files[0])}/>
              <label htmlFor="resume-tab-file-input" className="cursor-pointer w-full h-full flex flex-col items-center justify-center">
                <span className="text-3xl mb-2">📤</span>
                {file ? (
                  <span className="font-body text-sm text-primary font-medium">{file.name}</span>
                ) : (
                  <>
                    <span className="font-body text-sm text-on-surface font-medium">Click to select new resume PDF</span>
                    <span className="font-mono text-[9px] text-on-surface-variant/60 mt-1 uppercase">PDF Files Only</span>
                  </>
                )}
              </label>
            </div>
            <button onClick={handleUpload} disabled={uploading || !file} className="btn-primary w-full justify-center py-2.5">
              {uploading ? 'Uploading to Cloudinary...' : 'Upload New Resume'}
            </button>
          </div>
        </div>
      );
    },
  };

  const ActiveSection = sections[active] || sections.overview;

  return (
    <div className="min-h-screen bg-background flex">
      <AdminSidebar active={active} setActive={setActive} unreadCount={unread}/>
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="h-16 border-b border-outline-variant/20 flex items-center px-8 glass-card rounded-none">
          <h1 className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant">Admin Dashboard</h1>
          <div className="ml-auto flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-success animate-pulse"/><span className="font-mono text-[10px] text-on-surface-variant">System Online</span></div>
        </div>
        <div className="flex-1 overflow-y-auto p-8">
          <motion.div key={active} initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} transition={{duration:0.2}}>
            <ActiveSection/>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
