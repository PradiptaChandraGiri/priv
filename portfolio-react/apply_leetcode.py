import os
import re

ROOT = r"c:\Users\girip\Desktop\portfolio-react\src"

new_files = {}

# ─── 1. api/leetcode.js ────────────────────────────────────────────────────────
new_files["api/leetcode.js"] = """import axios from 'axios';

// LeetCode's public GraphQL API
const LEETCODE_API = 'https://leetcode.com/graphql';
const CORS_PROXY = 'https://corsproxy.io/?';

export const fetchLeetCodeProfile = async (username) => {
  const query = `
    query getUserProfile($username: String!) {
      allQuestionsCount { difficulty count }
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal { acSubmissionNum { difficulty count submissions } }
        profile { ranking userAvatar realName aboutMe school websites countryName company jobTitle skillTags postViewCount postViewCountDiff reputation reputationDiff solutionCount solutionCountDiff categoryDiscussCount categoryDiscussCountDiff }
        badges { id displayName icon creationDate }
        activeBadge { id displayName icon }
        userCalendar { activeYears streak totalActiveDays dccBadges { timestamp badge { name icon } } submissionCalendar }
        languageProblemCount { languageName problemsSolved }
        tagProblemCounts {
          advanced { tagName tagSlug problemsSolved }
          intermediate { tagName tagSlug problemsSolved }
          fundamental { tagName tagSlug problemsSolved }
        }
      }
    }
  `;

  const response = await axios.post(
    `${CORS_PROXY}${encodeURIComponent(LEETCODE_API)}`,
    { query, variables: { username } },
    { headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com' } }
  );

  if (response.data.errors) throw new Error(response.data.errors[0].message);
  return response.data.data;
};

export const fetchLeetCodeRecentSubmissions = async (username, limit = 15) => {
  const query = `
    query getRecentSubmissions($username: String!, $limit: Int) {
      recentSubmissionList(username: $username, limit: $limit) {
        id title titleSlug timestamp statusDisplay lang runtime memory
      }
    }
  `;

  const response = await axios.post(
    `${CORS_PROXY}${encodeURIComponent(LEETCODE_API)}`,
    { query, variables: { username, limit } },
    { headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com' } }
  );

  return response.data.data?.recentSubmissionList || [];
};
"""

# ─── 2. hooks/useLeetCode.js ───────────────────────────────────────────────────
new_files["hooks/useLeetCode.js"] = """import { useQuery } from '@tanstack/react-query';
import { fetchLeetCodeProfile, fetchLeetCodeRecentSubmissions } from '../api/leetcode';

export const useLeetCodeProfile = (username) => {
  return useQuery({
    queryKey: ['leetcode-profile', username],
    queryFn: () => fetchLeetCodeProfile(username),
    enabled: !!username,
    staleTime: 10 * 60 * 1000,
    retry: 2,
  });
};

export const useLeetCodeSubmissions = (username) => {
  return useQuery({
    queryKey: ['leetcode-submissions', username],
    queryFn: () => fetchLeetCodeRecentSubmissions(username, 15),
    enabled: !!username,
    staleTime: 10 * 60 * 1000,
    retry: 2,
  });
};
"""

# ─── 3. components/leetcode/LeetCodeStats.jsx ──────────────────────────────────
new_files["components/leetcode/LeetCodeStats.jsx"] = """import { motion } from 'framer-motion';
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
"""

# ─── 4. components/leetcode/DifficultyRing.jsx ─────────────────────────────────
new_files["components/leetcode/DifficultyRing.jsx"] = """import { motion } from 'framer-motion';

const SIZE   = 180;
const STROKE = 14;
const R      = (SIZE - STROKE) / 2;
const CIRC   = 2 * Math.PI * R;

export default function DifficultyRing({ solved, total }) {
  const easyPct   = total.Easy   > 0 ? (solved.Easy   / total.Easy)   * 100 : 0;
  const medPct    = total.Medium > 0 ? (solved.Medium / total.Medium) * 100 : 0;
  const hardPct   = total.Hard   > 0 ? (solved.Hard   / total.Hard)   * 100 : 0;
  const allPct    = total.All    > 0 ? (solved.All    / total.All)    * 100 : 0;

  const RINGS = [
    { percentage: allPct,  color: '#c0c1ff', r: 75, delay: 0   },
    { percentage: easyPct, color: '#00b8a3', r: 60, delay: 0.2 },
    { percentage: medPct,  color: '#ffc01e', r: 45, delay: 0.4 },
    { percentage: hardPct, color: '#ff375f', r: 30, delay: 0.6 },
  ];

  return (
    <div className="relative flex flex-col items-center">
      <svg width={SIZE} height={SIZE} className="drop-shadow-sm">
        {RINGS.map(({ r, color }, i) => <circle key={i} cx={SIZE / 2} cy={SIZE / 2} r={r} fill="none" stroke={color} strokeWidth={STROKE} opacity={0.1} />)}
        {RINGS.map(({ r, percentage, color, delay }, i) => {
          const c   = 2 * Math.PI * r;
          const dash = (percentage / 100) * c;
          return (
            <motion.circle key={`filled-${i}`} cx={SIZE / 2} cy={SIZE / 2} r={r} fill="none" stroke={color} strokeWidth={STROKE} strokeLinecap="round" strokeDasharray={`${c} ${c}`}
              transform={`rotate(-90 ${SIZE/2} ${SIZE/2})`} initial={{ strokeDashoffset: c }} animate={{ strokeDashoffset: c - dash }} transition={{ duration: 1.4, delay, ease: 'easeOut' }} />
          );
        })}
        <text x="50%" y="44%" textAnchor="middle" dominantBaseline="middle" fontSize="26" fontWeight="700" fill="currentColor" fontFamily="Poppins" className="text-on-surface">{solved.All}</text>
        <text x="50%" y="60%" textAnchor="middle" dominantBaseline="middle" fontSize="11" fill="currentColor" fontFamily="Inter" className="text-on-surface-variant">solved</text>
      </svg>
      <div className="flex gap-4 mt-3 flex-wrap justify-center">
        {[ { label: 'Easy', color: '#00b8a3', count: solved.Easy }, { label: 'Medium', color: '#ffc01e', count: solved.Medium }, { label: 'Hard', color: '#ff375f', count: solved.Hard }].map(({ label, color, count }) => (
          <div key={label} className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: color }} /><span className="text-xs text-on-surface-variant">{label}</span><span className="text-xs font-bold text-on-surface">{count}</span></div>
        ))}
      </div>
    </div>
  );
}
"""

# ─── 5. components/leetcode/HeatmapCalendar.jsx ────────────────────────────────
new_files["components/leetcode/HeatmapCalendar.jsx"] = """import { useMemo } from 'react';
import { motion } from 'framer-motion';

const DAYS_SHOWN = 53 * 7;
const CELL = 12;
const GAP  = 2;
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function getColor(count) {
  if (!count || count === 0) return 'rgba(255,255,255,0.05)';
  if (count === 1)  return '#e1e0ff';
  if (count <= 3)   return '#c0c1ff';
  if (count <= 6)   return '#8083ff';
  return '#4f46e5';
}

export default function HeatmapCalendar({ calendarData }) {
  const { weeks, monthLabels } = useMemo(() => {
    let parsed = {};
    try { parsed = JSON.parse(calendarData); } catch { parsed = {}; }

    const now   = new Date();
    const start = new Date(now);
    start.setDate(start.getDate() - DAYS_SHOWN + 1);
    start.setDate(start.getDate() - start.getDay());

    const weeks = [];
    const monthLabels = [];
    let cur = new Date(start);
    let lastMonth = -1;

    for (let w = 0; w < 53; w++) {
      const week = [];
      for (let d = 0; d < 7; d++) {
        const ts    = Math.floor(cur.getTime() / 1000);
        const count = parsed[ts] || 0;
        week.push({ date: new Date(cur), count });
        if (cur.getMonth() !== lastMonth) { monthLabels.push({ week: w, label: MONTHS[cur.getMonth()] }); lastMonth = cur.getMonth(); }
        cur.setDate(cur.getDate() + 1);
      }
      weeks.push(week);
    }
    return { weeks, monthLabels };
  }, [calendarData]);

  const totalWidth = 53 * (CELL + GAP);

  return (
    <div className="overflow-x-auto pb-4">
      <div style={{ minWidth: totalWidth + 40 }}>
        <div className="relative mb-1" style={{ height: 16, marginLeft: 30 }}>
          {monthLabels.map(({ week, label }) => (
            <span key={label + week} className="absolute text-[10px] text-on-surface-variant" style={{ left: week * (CELL + GAP) }}>{label}</span>
          ))}
        </div>
        <div className="flex gap-0">
          <div className="flex flex-col gap-[2px] mr-1">
            {['S','M','T','W','T','F','S'].map((d, i) => (
              <span key={i} className="text-[10px] text-on-surface-variant" style={{ height: CELL, display: 'flex', alignItems: 'center' }}>{i % 2 === 1 ? d : ''}</span>
            ))}
          </div>
          <div className="flex gap-[2px]">
            {weeks.map((week, wi) => (
              <div key={wi} className="flex flex-col gap-[2px]">
                {week.map((day, di) => (
                  <motion.div key={di} title={`${day.date.toDateString()}: ${day.count} submission${day.count !== 1 ? 's' : ''}`} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: wi * 0.005 }} style={{ width: CELL, height: CELL, background: getColor(day.count), borderRadius: 3 }} />
                ))}
              </div>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-2 mt-3 justify-end">
          <span className="text-[10px] text-on-surface-variant">Less</span>
          {[0, 1, 3, 5, 8].map(n => <div key={n} style={{ width: CELL, height: CELL, background: getColor(n), borderRadius: 3 }} />)}
          <span className="text-[10px] text-on-surface-variant">More</span>
        </div>
      </div>
    </div>
  );
}
"""

# ─── 6. components/leetcode/RecentSubmissions.jsx ──────────────────────────────
new_files["components/leetcode/RecentSubmissions.jsx"] = """import { motion } from 'framer-motion';
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
"""

# ─── 7. components/home/LeetCodePreview.jsx ────────────────────────────────────
new_files["components/home/LeetCodePreview.jsx"] = """import { motion } from 'framer-motion';
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
"""

# ─── 8. pages/CodingPage.jsx ───────────────────────────────────────────────────
new_files["pages/CodingPage.jsx"] = """import { motion } from 'framer-motion';
import { useProfile } from '../hooks/useProfile';
import { Home, ChevronRight, Code2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import LeetCodeStats from '../components/leetcode/LeetCodeStats';

export default function CodingPage() {
  const { data: profile, isLoading } = useProfile();
  const username = profile?.leetcode_username;

  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-5xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-secondary/10 pointer-events-none"/>
          <div className="relative z-10">
            <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Coding</span></nav>
            <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Competitive Coding</h1>
            <p className="font-body text-on-surface-variant max-w-xl">Live LeetCode statistics, problem-solving patterns, and submission history.</p>
            {username && (
              <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 mt-4 px-5 py-2.5 rounded-full text-xs font-semibold text-surface bg-tertiary hover:bg-tertiary/90 transition-colors">
                <img src="https://leetcode.com/favicon.ico" className="w-4 h-4" alt="" />
                @{username} on LeetCode ↗
              </a>
            )}
          </div>
        </div>

        {isLoading ? (
          <div className="text-center text-on-surface-variant font-mono text-xs">Loading profile...</div>
        ) : !username ? (
          <div className="glass-card rounded-xl p-12 text-center">
            <Code2 size={48} className="mx-auto text-on-surface-variant/30 mb-4"/>
            <p className="font-body text-on-surface mb-1">LeetCode username not set.</p>
            <p className="font-mono text-xs text-on-surface-variant">Admin -> Profile -> set LeetCode Username</p>
          </div>
        ) : (
          <LeetCodeStats username={username} />
        )}
      </div>
    </div>
  );
}
"""

# ─── 9. components/admin/LeetCodeSettings.jsx ──────────────────────────────────
new_files["components/admin/LeetCodeSettings.jsx"] = """import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import axios from '../../api/axios';
import { useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { ExternalLink, Code2 } from 'lucide-react';
import Button from '../ui/Button';

const schema = z.object({
  leetcode_username: z.string().min(1, 'Required').max(50).regex(/^[a-zA-Z0-9_-]+$/, 'Only letters, numbers, _, - allowed'),
});

export default function LeetCodeSettings({ currentUsername }) {
  const [isLoading, setIsLoading] = useState(false);
  const qc = useQueryClient();

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { leetcode_username: currentUsername || '' },
  });

  const onSave = async (data) => {
    setIsLoading(true);
    try {
      await axios.put('/profile', { leetcode_username: data.leetcode_username });
      qc.invalidateQueries(['profile']);
      qc.invalidateQueries(['leetcode-profile']);
      toast.success('LeetCode username saved!');
    } catch {
      // Mock mode fallback
      toast.success('Saved locally (Mock Mode)');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card rounded-xl p-6">
      <div className="flex items-center gap-2 mb-2">
        <Code2 size={20} className="text-primary"/>
        <h3 className="font-display font-semibold text-on-surface">LeetCode Integration</h3>
      </div>
      <p className="text-xs font-mono text-on-surface-variant mb-4">Set your public LeetCode username to display live coding stats.</p>
      
      <form onSubmit={handleSubmit(onSave)} className="flex flex-col sm:flex-row gap-3 items-start">
        <div className="flex-1 w-full">
          <div className="flex items-center bg-surface-container border border-outline-variant/40 rounded-lg overflow-hidden focus-within:border-primary/50 transition-colors">
            <span className="px-3 text-[11px] font-mono text-on-surface-variant bg-white/5 h-full flex items-center border-r border-outline-variant/40 py-2.5">leetcode.com/</span>
            <input {...register('leetcode_username')} placeholder="your_username" className="flex-1 px-3 py-2.5 bg-transparent text-on-surface font-body text-sm outline-none" />
          </div>
          {errors.leetcode_username && <p className="text-[10px] font-mono text-error mt-1">{errors.leetcode_username.message}</p>}
        </div>
        <Button type="submit" disabled={isLoading} className="whitespace-nowrap h-[42px]">{isLoading ? 'Saving...' : 'Save'}</Button>
        {currentUsername && (
          <a href={`https://leetcode.com/${currentUsername}`} target="_blank" rel="noopener noreferrer" className="h-[42px] px-3 rounded-lg border border-outline-variant/40 text-on-surface-variant hover:text-primary transition-colors flex items-center glass-panel">
            <ExternalLink size={16} />
          </a>
        )}
      </form>
    </div>
  );
}
"""

# Write all new files
for rel_path, content in new_files.items():
    abs_path = os.path.normpath(os.path.join(ROOT, rel_path))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"CREATED: {rel_path}")

# ─── UPDATE EXISTING FILES ────────────────────────────────────────────────────

def modify_file(rel_path, pattern, replacement):
    path = os.path.join(ROOT, rel_path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"MODIFIED: {rel_path}")

# 1. App.jsx: Add Route
modify_file("App.jsx", 
            r"import AboutPage from './pages/AboutPage';", 
            "import AboutPage from './pages/AboutPage';\nimport CodingPage from './pages/CodingPage';")
modify_file("App.jsx",
            r"<Route path=\"/skills\" element=\{<SkillsPage />\} />",
            "<Route path=\"/skills\" element={<SkillsPage />} />\n            <Route path=\"/coding\" element={<CodingPage />} />")

# 2. Navbar.jsx: Add Coding link
modify_file("components/layout/Navbar.jsx",
            r"\{ to: '/skills', label: 'Skills' \},",
            "{ to: '/skills', label: 'Skills' },\n  { to: '/coding', label: 'Coding' },")

# 3. HomePage.jsx: Add LeetCodePreview
modify_file("pages/HomePage.jsx",
            r"import CTASection from '../components/home/CTASection';",
            "import CTASection from '../components/home/CTASection';\nimport LeetCodePreview from '../components/home/LeetCodePreview';")

# We need to inject LeetCodePreview into StatsSection, but it's currently rendered inside StatsSection directly. Wait, the prompt says "In src/pages/HomePage.jsx, import and add <LeetCodePreview /> inside the Stats Strip section". But in our current structure, `StatsSection.jsx` has the grid. Let's just update `StatsSection.jsx`.
modify_file("components/home/StatsSection.jsx",
            r"import \{ FolderCode",
            "import LeetCodePreview from './LeetCodePreview';\nimport { FolderCode")
modify_file("components/home/StatsSection.jsx",
            r"grid-cols-2 md:grid-cols-4",
            "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5")
modify_file("components/home/StatsSection.jsx",
            r"\{stats\.map\(\(s, i\) => \(",
            "{stats.map((s, i) => (\n")
modify_file("components/home/StatsSection.jsx",
            r"\)\)}",
            "))}\n        <LeetCodePreview />")

# 4. AdminDashboardPage.jsx: Add Profile tab and LeetCodeSettings
modify_file("pages/AdminDashboardPage.jsx",
            r"import MessageList from '\.\./components/admin/MessageList';",
            "import MessageList from '../components/admin/MessageList';\nimport LeetCodeSettings from '../components/admin/LeetCodeSettings';\nimport { useProfile } from '../hooks/useProfile';")
modify_file("pages/AdminDashboardPage.jsx",
            r"const counts = \{",
            "const profileQuery = useProfile();\n  const counts = {")
modify_file("pages/AdminDashboardPage.jsx",
            r"messages: \(\) => \(<div>",
            "profile: () => (<div>\n      <h2 className=\"font-display font-bold text-2xl text-on-surface mb-6\">Profile Settings</h2>\n      <LeetCodeSettings currentUsername={profileQuery.data?.leetcode_username} />\n    </div>),\n    messages: () => (<div>")

# 5. api/profile.js: Add leetcode_username
modify_file("api/profile.js",
            r"location: 'Bhubaneswar, Odisha, India',",
            "location: 'Bhubaneswar, Odisha, India',\n  leetcode_username: 'pradiptachandragiri',")

print("SUCCESS: All LeetCode files generated and integrated.")
