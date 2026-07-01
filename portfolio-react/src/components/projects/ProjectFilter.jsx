const filters = ['All', 'Web Dev', 'ML/AI', 'Systems', 'Mobile', 'Other'];
const map = { 'All':'all', 'Web Dev':'web', 'ML/AI':'ml', 'Systems':'systems', 'Mobile':'mobile', 'Other':'other' };

export default function ProjectFilter({ active, onChange }) {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2 mb-8">
      {filters.map(f => (
        <button key={f} onClick={() => onChange(map[f])}
          className={`whitespace-nowrap px-5 py-2 rounded-full font-mono text-[10px] uppercase tracking-wider border transition-all ${active===map[f] ? 'bg-primary/20 text-primary border-primary/40 shadow-glow-sm' : 'bg-white/5 text-on-surface-variant border-white/10 hover:bg-white/10'}`}>
          {f}
        </button>
      ))}
    </div>
  );
}
