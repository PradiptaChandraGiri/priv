import { useState } from 'react';
import { ChevronDown, ChevronUp, Check } from 'lucide-react';
import Badge from '../ui/Badge';
export default function MessageList({ messages=[], onMarkRead }) {
  const [expanded, setExpanded] = useState(null);
  return (
    <div className="space-y-3">
      {messages.length === 0 && <div className="text-center py-12 text-on-surface-variant font-mono text-xs">No messages yet.</div>}
      {messages.map(m => (
        <div key={m.id} className={`glass-card rounded-xl overflow-hidden border ${!m.read ? 'border-primary/30' : 'border-white/10'}`}>
          <div className="flex items-center gap-4 p-4 cursor-pointer hover:bg-white/5 transition-colors" onClick={() => setExpanded(expanded===m.id?null:m.id)}>
            {!m.read && <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0"/>}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3"><span className="font-body font-semibold text-on-surface text-sm">{m.name}</span><Badge variant="neutral" size="sm">{m.subject}</Badge></div>
              <span className="font-mono text-[10px] text-on-surface-variant">{m.email} · {m.date}</span>
            </div>
            {expanded===m.id ? <ChevronUp size={16} className="text-on-surface-variant"/> : <ChevronDown size={16} className="text-on-surface-variant"/>}
          </div>
          {expanded===m.id && (
            <div className="px-4 pb-4 border-t border-white/10">
              <p className="font-body text-sm text-on-surface-variant my-3">{m.message}</p>
              {!m.read && <button onClick={() => onMarkRead(m.id)} className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-success hover:text-success/80 transition-colors"><Check size={14}/> Mark as Read</button>}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
