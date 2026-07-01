import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FolderCode, Award, BookOpen, Cpu, Trophy, Briefcase, User, FileText, MessageSquare, LogOut } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const items = [
  { label:'Overview', icon:LayoutDashboard, id:'overview' },
  { label:'Projects', icon:FolderCode, id:'projects' },
  { label:'Certificates', icon:Award, id:'certificates' },
  { label:'Research', icon:BookOpen, id:'research' },
  { label:'Skills', icon:Cpu, id:'skills' },
  { label:'Achievements', icon:Trophy, id:'achievements' },
  { label:'Experience', icon:Briefcase, id:'experience' },
  { label:'Profile', icon:User, id:'profile' },
  { label:'Resume', icon:FileText, id:'resume' },
  { label:'Messages', icon:MessageSquare, id:'messages' },
];

export default function AdminSidebar({ active, setActive, unreadCount=0 }) {
  const { logout, adminName } = useAuthStore();
  return (
    <aside className="w-64 flex-shrink-0 glass-card border-r border-outline-variant/20 flex flex-col h-full">
      <div className="p-6 border-b border-white/10">
        <div className="font-display font-bold text-lg gradient-text">Admin Panel</div>
        <div className="font-mono text-[10px] text-on-surface-variant mt-1">Welcome, {adminName}</div>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        {items.map(item => (
          <button key={item.id} onClick={() => setActive(item.id)}
            className={`w-full flex items-center gap-3 px-6 py-3 text-left transition-all duration-200 font-mono text-[11px] uppercase tracking-wider ${active===item.id ? 'bg-primary/15 text-primary border-r-2 border-primary' : 'text-on-surface-variant hover:bg-white/5 hover:text-primary'}`}>
            <item.icon size={16}/>
            <span>{item.label}</span>
            {item.id==='messages' && unreadCount>0 && <span className="ml-auto bg-primary text-on-primary text-[9px] font-bold px-1.5 py-0.5 rounded-full">{unreadCount}</span>}
          </button>
        ))}
      </nav>
      <button onClick={logout} className="flex items-center gap-3 px-6 py-4 text-on-surface-variant hover:text-error transition-colors border-t border-white/10 font-mono text-[11px] uppercase tracking-wider">
        <LogOut size={16}/> Logout
      </button>
    </aside>
  );
}
