import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useLeetCodeProfile } from '../../hooks/useLeetCode';
import { useProfile } from '../../hooks/useProfile';

export default function LeetCodePreview() {
  const { data: profile } = useProfile();
  const username = profile?.leetcode_username;
  const { data, isLoading } = useLeetCodeProfile(username);

  if (!username) return null;
  if (isLoading) return <HomePreviewSkeleton />;

  const user = data?.matchedUser;
  if (!user) return null;

  const stats = user.submitStats.acSubmissionNum;
  const solved  = stats.find(s => s.difficulty === 'All')?.count ?? 0;
  const easy    = stats.find(s => s.difficulty === 'Easy')?.count ?? 0;
  const medium  = stats.find(s => s.difficulty === 'Medium')?.count ?? 0;
  const hard    = stats.find(s => s.difficulty === 'Hard')?.count ?? 0;
  const streak  = user.userCalendar?.streak ?? 0;
  const ranking = user.profile.ranking;

  return (
    <motion.div whileHover={{ y: -4 }} className="glass-card rounded-xl p-6 relative overflow-hidden group">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none"/>
      <div className="flex items-center justify-between mb-4 relative z-10">
        <div className="flex items-center gap-2">
          <img src="https://leetcode.com/static/images/LeetCode_logo_rvs_dark.png" alt="LeetCode" className="w-5 h-5 object-contain" />
          <span className="font-display font-semibold text-on-surface">LeetCode</span>
        </div>
        <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer" className="text-xs text-primary hover:underline">@{username} ↗</a>
      </div>
      <div className="flex items-end gap-3 mb-4 relative z-10">
        <span className="text-4xl font-bold font-display text-on-surface">{solved}</span>
        <div className="mb-1"><div className="text-[10px] text-on-surface-variant uppercase tracking-wider">solved</div><div className="text-[10px] text-primary">Rank #{ranking?.toLocaleString()}</div></div>
        <div className="ml-auto text-right"><div className="text-base font-bold text-tertiary">🔥 {streak}</div><div className="text-[10px] text-on-surface-variant uppercase tracking-wider">day streak</div></div>
      </div>
      <div className="flex gap-2 mb-4 relative z-10">
        {[ { label: 'Easy', count: easy, color: '#00b8a3' }, { label: 'Med', count: medium, color: '#ffc01e' }, { label: 'Hard', count: hard, color: '#ff375f' }].map(({ label, count, color }) => (
          <div key={label} className="flex-1 rounded-lg py-1.5 px-2 text-center bg-surface-container border border-white/5">
            <div className="text-sm font-bold" style={{ color }}>{count}</div>
            <div className="text-[9px] text-on-surface-variant uppercase">{label}</div>
          </div>
        ))}
      </div>
      <div className="space-y-1.5 mb-4 relative z-10">
        {[ { diff: 'Easy', val: easy, max: 800, color: '#00b8a3' }, { diff: 'Medium', val: medium, max: 1700, color: '#ffc01e' }, { diff: 'Hard', val: hard, max: 700, color: '#ff375f' }].map(({ diff, val, max, color }) => (
          <div key={diff} className="h-1.5 bg-surface-container rounded-full overflow-hidden">
            <motion.div initial={{ width: 0 }} animate={{ width: `${Math.min((val/max)*100, 100)}%` }} transition={{ duration: 1, ease: 'easeOut' }} className="h-full rounded-full" style={{ background: color }} />
          </div>
        ))}
      </div>
      <Link to="/coding" className="block text-center text-xs font-semibold text-on-primary rounded-lg py-2.5 transition-all bg-primary hover:bg-primary-light shadow-glow-sm relative z-10">
        View Full Stats →
      </Link>
    </motion.div>
  );
}
function HomePreviewSkeleton() { return <div className="glass-card rounded-xl p-6 animate-pulse"><div className="h-5 w-32 bg-surface-container rounded mb-4" /><div className="h-10 w-24 bg-surface-container rounded mb-4" /><div className="flex gap-2 mb-4">{[1,2,3].map(i=><div key={i} className="flex-1 h-12 bg-surface-container rounded-lg"/>)}</div><div className="h-8 bg-surface-container rounded-lg" /></div>; }
