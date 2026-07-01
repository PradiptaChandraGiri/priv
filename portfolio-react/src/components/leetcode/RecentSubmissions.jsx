import { motion } from 'framer-motion';
import { useLeetCodeSubmissions } from '../../hooks/useLeetCode';
import { ExternalLink, Clock } from 'lucide-react';

const STATUS_STYLES = {
  'Accepted':               'bg-success/20 text-success border border-success/30',
  'Wrong Answer':           'bg-error/20 text-error border border-error/30',
  'Time Limit Exceeded':    'bg-warning/20 text-warning border border-warning/30',
  'Runtime Error':          'bg-tertiary/20 text-tertiary border border-tertiary/30',
  'Memory Limit Exceeded':  'bg-secondary/20 text-secondary border border-secondary/30',
  'Compilation Error':      'bg-white/10 text-on-surface border border-white/20',
};

function timeAgo(ts) {
  const diff = Date.now() - ts * 1000;
  const mins  = Math.floor(diff / 60000);
  if (mins < 1)   return 'just now';
  if (mins < 60)  return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

const LANG_COLORS = {
  'python3': '#3572a5', 'python': '#3572a5',
  'cpp': '#f34b7d',     'c++': '#f34b7d',
  'java': '#b07219',    'javascript': '#f1e05a',
  'typescript': '#3178c6', 'go': '#00add8',
  'rust': '#dea584',    'c': '#555555',
};

export default function RecentSubmissions({ username }) {
  const { data: submissions, isLoading } = useLeetCodeSubmissions(username);

  if (isLoading) return <div className="glass-card rounded-2xl p-6 space-y-3"><div className="h-5 w-40 bg-surface-container rounded animate-pulse" />{[...Array(5)].map((_,i) => <div key={i} className="h-12 bg-surface-container rounded-xl animate-pulse" />)}</div>;
  if (!submissions?.length) return null;

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.55 }} className="glass-card rounded-2xl p-6">
      <h3 className="font-display font-semibold text-on-surface mb-4">Recent Submissions</h3>
      <div className="space-y-2">
        {submissions.map((sub, i) => (
          <motion.div key={sub.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.55 + i * 0.04 }} className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group border border-transparent hover:border-white/10">
            <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: sub.statusDisplay === 'Accepted' ? '#10b981' : '#ffb4ab' }} />
            <a href={`https://leetcode.com/problems/${sub.titleSlug}`} target="_blank" rel="noopener noreferrer" className="flex-1 text-sm font-medium text-on-surface hover:text-primary truncate">
              {sub.title} <ExternalLink className="inline w-3 h-3 ml-1 opacity-0 group-hover:opacity-60 transition-opacity" />
            </a>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full whitespace-nowrap ${STATUS_STYLES[sub.statusDisplay] || 'bg-white/10 text-on-surface'}`}>{sub.statusDisplay === 'Accepted' ? '✓ AC' : sub.statusDisplay.split(' ').map(w=>w[0]).join('')}</span>
            <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full hidden sm:inline" style={{ background: `${LANG_COLORS[sub.lang?.toLowerCase()] || '#c7c4d7'}22`, color: LANG_COLORS[sub.lang?.toLowerCase()] || '#c7c4d7' }}>{sub.lang}</span>
            <span className="text-[10px] text-on-surface-variant flex items-center gap-0.5 whitespace-nowrap"><Clock className="w-3 h-3" />{timeAgo(sub.timestamp)}</span>
          </motion.div>
        ))}
      </div>
      <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer" className="block text-center text-sm text-primary font-medium mt-4 hover:underline">View all on LeetCode ↗</a>
    </motion.div>
  );
}
