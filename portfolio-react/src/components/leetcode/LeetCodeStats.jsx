import { motion } from 'framer-motion';
import { useLeetCodeProfile } from '../../hooks/useLeetCode';
import DifficultyRing from './DifficultyRing';
import HeatmapCalendar from './HeatmapCalendar';
import RecentSubmissions from './RecentSubmissions';

const DIFF_COLORS = {
  Easy:   { bg: '#00b8a3', text: '#00b8a3', dark: '#00ffa3' },
  Medium: { bg: '#ffc01e', text: '#ffc01e', dark: '#ffd700' },
  Hard:   { bg: '#ff375f', text: '#ff375f', dark: '#ff6b8a' },
  All:    { bg: '#6366f1', text: '#6366f1', dark: '#818cf8' },
};

export default function LeetCodeStats({ username }) {
  const { data, isLoading, isError, refetch } = useLeetCodeProfile(username);

  if (isLoading) return <LeetCodeSkeleton />;

  if (isError || !data?.matchedUser) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <span className="text-5xl mb-4">⚠️</span>
        <p className="text-on-surface-variant mb-4">Could not load LeetCode stats for <strong className="text-on-surface">@{username}</strong>.<br/>LeetCode may be temporarily unavailable.</p>
        <button onClick={refetch} className="px-4 py-2 rounded-full bg-primary text-white text-sm font-medium hover:bg-primary-dark transition">Try Again</button>
      </div>
    );
  }

  const user = data.matchedUser;
  const allCount = data.allQuestionsCount;
  const stats = user.submitStats.acSubmissionNum;

  const solved = {
    All:    stats.find(s => s.difficulty === 'All')?.count ?? 0,
    Easy:   stats.find(s => s.difficulty === 'Easy')?.count ?? 0,
    Medium: stats.find(s => s.difficulty === 'Medium')?.count ?? 0,
    Hard:   stats.find(s => s.difficulty === 'Hard')?.count ?? 0,
  };
  const total = {
    All:    allCount.find(s => s.difficulty === 'All')?.count ?? 0,
    Easy:   allCount.find(s => s.difficulty === 'Easy')?.count ?? 0,
    Medium: allCount.find(s => s.difficulty === 'Medium')?.count ?? 0,
    Hard:   allCount.find(s => s.difficulty === 'Hard')?.count ?? 0,
  };

  const cal = user.userCalendar;
  const topLangs = user.languageProblemCount?.slice(0, 5) || [];
  const topTags  = [...(user.tagProblemCounts?.advanced || []), ...(user.tagProblemCounts?.intermediate || [])].sort((a,b) => b.problemsSolved - a.problemsSolved).slice(0, 8);

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card rounded-2xl p-6 flex flex-col items-center justify-center gap-4">
          <DifficultyRing solved={solved} total={total} />
          <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer" className="text-sm text-primary font-medium hover:underline">View full profile ↗</a>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="grid grid-cols-2 gap-4">
          {[
            { label: 'Global Rank',   value: `#${user.profile.ranking?.toLocaleString() || 'N/A'}`, icon: '🏆' },
            { label: 'Total Solved',  value: solved.All,        icon: '✅' },
            { label: 'Current Streak',value: `${cal?.streak ?? 0}d`,     icon: '🔥' },
            { label: 'Active Days',   value: cal?.totalActiveDays ?? 0,  icon: '📅' },
          ].map((stat, i) => (
            <motion.div key={stat.label} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 + i * 0.05 }} className="glass-card rounded-2xl p-4 flex flex-col gap-1">
              <span className="text-2xl">{stat.icon}</span>
              <span className="text-2xl font-bold font-display text-on-surface">{stat.value}</span>
              <span className="text-xs text-on-surface-variant font-medium">{stat.label}</span>
            </motion.div>
          ))}
        </motion.div>
      </div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card rounded-2xl p-6">
        <h3 className="font-display font-semibold text-on-surface mb-5">Difficulty Breakdown</h3>
        <div className="space-y-4">
          {['Easy', 'Medium', 'Hard'].map((diff, i) => {
            const pct = total[diff] > 0 ? Math.round((solved[diff] / total[diff]) * 100) : 0;
            return (
              <div key={diff}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-semibold" style={{ color: DIFF_COLORS[diff].bg }}>{diff}</span>
                  <span className="text-sm text-on-surface-variant"><span className="font-bold text-on-surface">{solved[diff]}</span> / {total[diff]}<span className="ml-2 text-on-surface-variant/70">({pct}%)</span></span>
                </div>
                <div className="h-2.5 bg-surface-container rounded-full overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 1, delay: 0.3 + i * 0.1, ease: 'easeOut' }} className="h-full rounded-full" style={{ background: DIFF_COLORS[diff].bg }}/>
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>

      {cal?.submissionCalendar && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card rounded-2xl p-6">
          <h3 className="font-display font-semibold text-on-surface mb-5">Submission Activity</h3>
          <HeatmapCalendar calendarData={cal.submissionCalendar} />
        </motion.div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {topLangs.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card rounded-2xl p-6">
            <h3 className="font-display font-semibold text-on-surface mb-4">Languages Used</h3>
            <div className="space-y-3">
              {topLangs.map((lang, i) => {
                const maxSolved = topLangs[0].problemsSolved;
                const pct = Math.round((lang.problemsSolved / maxSolved) * 100);
                return (
                  <div key={lang.languageName}>
                    <div className="flex justify-between text-sm mb-1"><span className="text-on-surface font-medium">{lang.languageName}</span><span className="text-on-surface-variant">{lang.problemsSolved} solved</span></div>
                    <div className="h-2 bg-surface-container rounded-full overflow-hidden">
                      <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 0.8, delay: 0.4 + i * 0.1 }} className="h-full rounded-full bg-gradient-to-r from-primary to-secondary"/>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}

        {topTags.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }} className="glass-card rounded-2xl p-6">
            <h3 className="font-display font-semibold text-on-surface mb-4">Top Problem Topics</h3>
            <div className="flex flex-wrap gap-2">
              {topTags.map(tag => (
                <span key={tag.tagSlug} className="px-3 py-1.5 rounded-full text-xs font-semibold bg-primary/10 text-primary border border-primary/20">{tag.tagName}<span className="ml-1.5 opacity-60">{tag.problemsSolved}</span></span>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {user.badges?.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="glass-card rounded-2xl p-6">
          <h3 className="font-display font-semibold text-on-surface mb-4">Badges Earned<span className="ml-2 text-sm text-on-surface-variant font-normal">({user.badges.length})</span></h3>
          <div className="flex flex-wrap gap-4">
            {user.badges.map(badge => (
              <div key={badge.id} className="flex flex-col items-center gap-1 group">
                <img src={badge.icon} alt={badge.displayName} className="w-12 h-12 object-contain group-hover:scale-110 transition-transform" />
                <span className="text-[10px] text-on-surface-variant text-center max-w-[56px] leading-tight">{badge.displayName}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <RecentSubmissions username={username} />
    </div>
  );
}

function LeetCodeSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6"><div className="h-64 bg-surface-container rounded-2xl" /><div className="grid grid-cols-2 gap-4">{[1,2,3,4].map(i => <div key={i} className="h-28 bg-surface-container rounded-2xl" />)}</div></div>
      <div className="h-40 bg-surface-container rounded-2xl" />
      <div className="h-48 bg-surface-container rounded-2xl" />
    </div>
  );
}
