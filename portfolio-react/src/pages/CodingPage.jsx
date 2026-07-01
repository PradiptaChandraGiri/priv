import { useState, useEffect, useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { ExternalLink, RefreshCw, Trophy, Flame, Calendar, Code2, Tag, Home, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useProfile } from '../hooks/useProfile';

// API endpoint — routes through YOUR backend (no CORS issues)
const BACKEND = import.meta.env.VITE_API_URL || '/api';
const LC_PROXY = BACKEND.endsWith('/api') ? `${BACKEND}/leetcode-proxy` : `${BACKEND}/api/leetcode-proxy`;

// ── GraphQL Queries ────────────────────────────────────────────
const PROFILE_QUERY = `
  query($u: String!) {
    allQuestionsCount { difficulty count }
    matchedUser(username: $u) {
      username
      submitStats: submitStatsGlobal {
        acSubmissionNum { difficulty count submissions }
      }
      userCalendar {
        streak
        totalActiveDays
        submissionCalendar
      }
      profile { ranking userAvatar }
      languageProblemCount { languageName problemsSolved }
      badges { id displayName icon creationDate }
      tagProblemCounts {
        advanced { tagName tagSlug problemsSolved }
        intermediate { tagName tagSlug problemsSolved }
      }
    }
  }
`;

const SUBMISSIONS_QUERY = `
  query($u: String!, $limit: Int) {
    recentSubmissionList(username: $u, limit: $limit) {
      id title titleSlug timestamp statusDisplay lang
    }
  }
`;

// ── API Fetchers ───────────────────────────────────────────────
async function fetchLCProfile(username) {
  const res = await fetch(LC_PROXY, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ query: PROFILE_QUERY, variables: { u: username } }),
  });
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  const json = await res.json();
  if (json.errors) throw new Error(json.errors[0].message);
  return json.data;
}

async function fetchLCSubmissions(username) {
  const res = await fetch(LC_PROXY, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ query: SUBMISSIONS_QUERY, variables: { u: username, limit: 12 } }),
  });
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  const json = await res.json();
  return json.data?.recentSubmissionList || [];
}

// ── Helpers ────────────────────────────────────────────────────
function timeAgo(ts) {
  const d = Date.now() - ts * 1000;
  if (d < 60000)         return 'just now';
  if (d < 3600000)       return Math.floor(d/60000)  + 'm ago';
  if (d < 86400000)      return Math.floor(d/3600000) + 'h ago';
  return Math.floor(d/86400000) + 'd ago';
}

const DIFF_COLOR = { Easy: '#00b8a3', Medium: '#ffc01e', Hard: '#ff375f' };
const LANG_COLOR = { python3:'#3572a5', python:'#3572a5', cpp:'#f34b7d', java:'#b07219', javascript:'#f1e05a', typescript:'#3178c6', c:'#555555', go:'#00add8' };
const STATUS_STYLE = {
  'Accepted':            'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
  'Wrong Answer':        'bg-red-500/15 text-red-400 border border-red-500/30',
  'Time Limit Exceeded': 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
  'Runtime Error':       'bg-orange-500/15 text-orange-400 border border-orange-500/30',
};

// ── Sub-components ─────────────────────────────────────────────

// Concentric SVG rings
function DifficultyRings({ solved, total }) {
  const RINGS = [
    { r: 75, color: '#6366f1', key: 'All',    delay: 0   },
    { r: 60, color: '#00b8a3', key: 'Easy',   delay: 0.2 },
    { r: 45, color: '#ffc01e', key: 'Medium', delay: 0.4 },
    { r: 30, color: '#ff375f', key: 'Hard',   delay: 0.6 },
  ];
  const ref    = useRef(null);
  const inView = useInView(ref, { once: true });

  return (
    <div ref={ref} className="flex flex-col items-center gap-5">
      <svg width="180" height="180" className="drop-shadow-sm">
        {RINGS.map(({ r, color }) => {
          const c = 2 * Math.PI * r;
          return <circle key={r+'track'} cx="90" cy="90" r={r} fill="none" stroke={color} strokeWidth="12" opacity="0.1"/>
        })}
        {RINGS.map(({ r, color, key, delay }) => {
          const c   = 2 * Math.PI * r;
          const tot = total[key] || (key === 'All' ? 3500 : key === 'Easy' ? 800 : key === 'Medium' ? 1700 : 700);
          const pct = tot > 0 ? Math.min((solved[key] || 0) / tot, 1) : 0;
          const dash = pct * c;
          return (
            <motion.circle key={r+'fill'} cx="90" cy="90" r={r} fill="none" stroke={color}
              strokeWidth="12" strokeLinecap="round" strokeDasharray={`${c} ${c}`}
              transform="rotate(-90 90 90)"
              initial={{ strokeDashoffset: c }}
              animate={inView ? { strokeDashoffset: c - dash } : {}}
              transition={{ duration: 1.4, delay, ease: 'easeOut' }}
            />
          );
        })}
        <text x="90" y="84" textAnchor="middle" fontSize="28" fontWeight="700" fill="#e4e1ed" fontFamily="Poppins">{solved.All || 0}</text>
        <text x="90" y="104" textAnchor="middle" fontSize="11" fill="#9ca3af" fontFamily="Inter">solved</text>
      </svg>
      {/* Legend */}
      <div className="flex gap-4 flex-wrap justify-center">
        {['Easy','Medium','Hard'].map(d => (
          <div key={d} className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: DIFF_COLOR[d] }}/>
            <span className="text-xs text-on-surface-variant">{d}</span>
            <span className="text-xs font-bold text-on-surface">{solved[d] || 0}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// Heatmap calendar (last 20 weeks)
function HeatmapCalendar({ calendarJson }) {
  const data = (() => { try { return JSON.parse(calendarJson || '{}') } catch { return {} } })();
  const WEEKS = 20;
  const now   = new Date();
  const days  = [];
  for (let i = WEEKS * 7 - 1; i >= 0; i--) {
    const d  = new Date(now); d.setDate(d.getDate() - i);
    const ts = Math.floor(d.getTime() / 1000);
    days.push({ date: d, count: data[ts] || 0 });
  }

  function cellColor(n) {
    if (!n) return 'rgba(57,56,65,0.6)';
    if (n === 1) return 'rgba(192,193,255,0.3)';
    if (n <= 3)  return 'rgba(192,193,255,0.6)';
    if (n <= 6)  return '#c0c1ff';
    return '#8083ff';
  }

  return (
    <div className="overflow-x-auto">
      <div className="flex gap-1 min-w-[260px]">
        {Array.from({ length: WEEKS }, (_, w) => (
          <div key={w} className="flex flex-col gap-1">
            {days.slice(w * 7, w * 7 + 7).map((day, d) => (
              <motion.div key={d} title={`${day.date.toDateString()}: ${day.count} submission${day.count !== 1 ? 's' : ''}`}
                className="w-3 h-3 rounded-sm cursor-pointer hover:scale-125 transition-transform"
                style={{ background: cellColor(day.count) }}
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: w * 0.01 }}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="flex items-center gap-1.5 mt-2 justify-end">
        <span className="text-[10px] text-on-surface-variant">Less</span>
        {[0,1,3,5,8].map(n => (
          <div key={n} className="w-3 h-3 rounded-sm" style={{ background: cellColor(n) }}/>
        ))}
        <span className="text-[10px] text-on-surface-variant">More</span>
      </div>
    </div>
  );
}

// Recent submissions table row
function SubmissionRow({ sub, i }) {
  const isAC = sub.statusDisplay === 'Accepted';
  return (
    <motion.tr initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
      transition={{ delay: i * 0.04 }}
      className="hover:bg-surface-container-high/30 transition-colors group border-b border-outline-variant/10 last:border-0">
      <td className="px-4 py-3">
        <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${STATUS_STYLE[sub.statusDisplay] || 'bg-gray-500/10 text-gray-400 border border-gray-500/20'}`}>
          {isAC ? '✓' : '✕'} {isAC ? 'AC' : sub.statusDisplay?.split(' ').map(w=>w[0]).join('')}
        </span>
      </td>
      <td className="px-4 py-3">
        <a href={`https://leetcode.com/problems/${sub.titleSlug}`} target="_blank" rel="noopener noreferrer"
          className="text-sm text-on-surface group-hover:text-primary transition-colors hover:underline flex items-center gap-1">
          {sub.title}
          <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-50 transition-opacity flex-shrink-0"/>
        </a>
      </td>
      <td className="px-4 py-3 hidden sm:table-cell">
        <span className="text-[11px] font-mono px-2 py-0.5 rounded"
          style={{ background: `${LANG_COLOR[sub.lang?.toLowerCase()] || '#6b7280'}18`, color: LANG_COLOR[sub.lang?.toLowerCase()] || '#9ca3af' }}>
          {sub.lang}
        </span>
      </td>
      <td className="px-4 py-3 hidden md:table-cell text-[11px] text-on-surface-variant">{timeAgo(sub.timestamp)}</td>
    </motion.tr>
  );
}

// ── Main Component ─────────────────────────────────────────────
export default function CodingPage() {
  const { data: profile, isLoading: profileLoading } = useProfile();
  const username = profile?.leetcode_username || 'Pradipta_Chadnra_Giri';

  const { data: profileData, isLoading: lcProfileLoading, isError: profileError, refetch: refetchProfile } =
    useQuery({
      queryKey:  ['lc-profile', username],
      queryFn:   () => fetchLCProfile(username),
      enabled:   !!username,
      staleTime: 10 * 60 * 1000,
      retry:     2,
    });

  const { data: submissions = [], isLoading: subsLoading } =
    useQuery({
      queryKey:  ['lc-submissions', username],
      queryFn:   () => fetchLCSubmissions(username),
      enabled:   !!username,
      staleTime: 10 * 60 * 1000,
      retry:     2,
    });

  // Derived data
  const user     = profileData?.matchedUser;
  const allQ     = profileData?.allQuestionsCount || [];
  const stats    = user?.submitStats?.acSubmissionNum || [];
  const cal      = user?.userCalendar;
  const langs    = (user?.languageProblemCount || []).slice(0, 5);
  const tags     = [...(user?.tagProblemCounts?.advanced||[]), ...(user?.tagProblemCounts?.intermediate||[])]
                     .sort((a,b) => b.problemsSolved - a.problemsSolved).slice(0, 10);
  const badges   = user?.badges || [];

  const solved = {
    All:    stats.find(s=>s.difficulty==='All')?.count    || 0,
    Easy:   stats.find(s=>s.difficulty==='Easy')?.count   || 0,
    Medium: stats.find(s=>s.difficulty==='Medium')?.count || 0,
    Hard:   stats.find(s=>s.difficulty==='Hard')?.count   || 0,
  };
  const total = {
    All:    allQ.find(s=>s.difficulty==='All')?.count    || 3500,
    Easy:   allQ.find(s=>s.difficulty==='Easy')?.count   || 800,
    Medium: allQ.find(s=>s.difficulty==='Medium')?.count || 1700,
    Hard:   allQ.find(s=>s.difficulty==='Hard')?.count   || 700,
  };

  // ── RENDER ────────────────────────────────────────────────────
  if (profileLoading || lcProfileLoading) return <CodingPageSkeleton />;

  if (profileError || !user) return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="text-center max-w-md">
        <div className="text-6xl mb-4">⚠️</div>
        <h2 className="font-['Poppins'] text-2xl font-bold text-on-surface mb-3">LeetCode Stats Unavailable</h2>
        <p className="text-on-surface-variant mb-2">Could not load stats for <strong className="text-primary">@{username}</strong></p>
        <p className="text-sm text-on-surface-variant mb-6">
          Make sure your backend is running and the <code className="text-primary bg-primary/10 px-1 rounded">/api/leetcode-proxy</code> route is active.
        </p>
        <button onClick={() => refetchProfile()}
          className="inline-flex items-center gap-2 bg-primary text-on-primary px-6 py-3 rounded-full font-bold hover:opacity-90 transition-opacity">
          <RefreshCw className="w-4 h-4"/> Try Again
        </button>
        <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer"
          className="block mt-3 text-sm text-primary hover:underline">
          View directly on LeetCode ↗
        </a>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background pt-24 pb-16 px-5 md:px-10 lg:px-16 max-w-[1280px] mx-auto">

      {/* ── Page Header ── */}
      <motion.section initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} className="mb-12">
        <div className="glass-card rounded-xl p-8 mb-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-secondary/10 pointer-events-none" />
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3">
            <Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link>
            <ChevronRight size={12}/>
            <span className="text-primary">Coding</span>
          </nav>
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Competitive Coding</h1>
              <p className="font-body text-on-surface-variant max-w-xl">
                Live LeetCode statistics, problem-solving patterns, and submission history.
              </p>
            </div>
            <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer"
              className="self-start md:self-auto inline-flex items-center gap-2 bg-[#ffc01e]/10 hover:bg-[#ffc01e]/20 text-[#ffc01e] border border-[#ffc01e]/30 px-5 py-2.5 rounded-full text-sm font-bold transition-all">
              <img src="https://leetcode.com/favicon.ico" className="w-4 h-4" alt=""/>
              @{username}
              <ExternalLink className="w-3.5 h-3.5"/>
            </a>
          </div>
        </div>
      </motion.section>

      {/* ── Row 1: Rings + Stat Cards ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

        {/* Rings card */}
        <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.1}}
          className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6 flex flex-col items-center justify-center gap-4">
          <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface self-start">Problems Solved</h3>
          <DifficultyRings solved={solved} total={total} />
        </motion.div>

        {/* 4 stat mini-cards */}
        <div className="grid grid-cols-2 gap-4">
          {[
            { icon: <Trophy className="w-5 h-5"/>,  label: 'Global Rank',    value: '#' + (user.profile?.ranking?.toLocaleString() || '—'), color: 'text-[#ffc01e]' },
            { icon: <Code2 className="w-5 h-5"/>,   label: 'Total Solved',   value: solved.All,                                              color: 'text-primary'   },
            { icon: <Flame className="w-5 h-5"/>,   label: 'Current Streak', value: (cal?.streak || 0) + ' days',                            color: 'text-orange-400'},
            { icon: <Calendar className="w-5 h-5"/>,label: 'Active Days',    value: cal?.totalActiveDays || 0,                               color: 'text-[#10b981]' },
          ].map((s, i) => (
            <motion.div key={s.label} initial={{opacity:0,scale:0.9}} animate={{opacity:1,scale:1}} transition={{delay:0.15+i*0.05}}
              className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-4 flex flex-col gap-2">
              <span className={s.color}>{s.icon}</span>
              <span className="font-['Poppins'] text-2xl font-bold text-on-surface">{s.value}</span>
              <span className="text-[11px] text-on-surface-variant font-medium">{s.label}</span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* ── Row 2: Difficulty bars ── */}
      <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.2}}
        className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6 mb-6">
        <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface mb-5">Difficulty Breakdown</h3>
        <div className="space-y-4">
          {['Easy','Medium','Hard'].map((diff, i) => {
            const pct = total[diff] > 0 ? Math.round((solved[diff] / total[diff]) * 100) : 0;
            return (
              <div key={diff}>
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="font-semibold" style={{ color: DIFF_COLOR[diff] }}>{diff}</span>
                  <span className="text-on-surface-variant">
                    <span className="font-bold text-on-surface">{solved[diff]}</span> / {total[diff]}
                    <span className="ml-2 text-outline">({pct}%)</span>
                  </span>
                </div>
                <div className="h-2.5 bg-surface-container-highest rounded-full overflow-hidden">
                  <motion.div className="h-full rounded-full"
                    style={{ background: DIFF_COLOR[diff] }}
                    initial={{ width: 0 }}
                    animate={{ width: pct + '%' }}
                    transition={{ duration: 1.1, delay: 0.25 + i * 0.1, ease: 'easeOut' }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* ── Row 3: Heatmap ── */}
      {cal?.submissionCalendar && (
        <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.3}}
          className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface">Submission Activity</h3>
            <div className="flex gap-3 text-xs text-on-surface-variant">
              <span>🔥 {cal.streak || 0} day streak</span>
              <span>📅 {cal.totalActiveDays || 0} active days</span>
            </div>
          </div>
          <HeatmapCalendar calendarJson={cal.submissionCalendar} />
        </motion.div>
      )}

      {/* ── Row 4: Languages + Tags ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

        {/* Languages */}
        {langs.length > 0 && (
          <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.35}}
            className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6">
            <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface mb-4">Languages Used</h3>
            <div className="space-y-3">
              {langs.map((lang, i) => {
                const maxS = langs[0].problemsSolved;
                const pct  = Math.round((lang.problemsSolved / maxS) * 100);
                const col  = LANG_COLOR[lang.languageName.toLowerCase()] || '#6366f1';
                return (
                  <div key={lang.languageName}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-on-surface font-medium">{lang.languageName}</span>
                      <span className="text-on-surface-variant">{lang.problemsSolved} solved</span>
                    </div>
                    <div className="h-2 bg-surface-container-highest rounded-full overflow-hidden">
                      <motion.div className="h-full rounded-full"
                        style={{ background: col }}
                        initial={{ width: 0 }}
                        animate={{ width: pct + '%' }}
                        transition={{ duration: 0.9, delay: 0.4 + i * 0.1 }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}

        {/* Tags */}
        {tags.length > 0 && (
          <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.4}}
            className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6">
            <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface mb-4 flex items-center gap-2">
              <Tag className="w-4 h-4 text-primary"/> Top Problem Topics
            </h3>
            <div className="flex flex-wrap gap-2">
              {tags.map(tag => (
                <span key={tag.tagSlug}
                  className="px-3 py-1.5 rounded-full text-xs font-semibold cursor-default hover:bg-primary/20 transition-colors"
                  style={{ background:'rgba(99,102,241,0.1)', color:'#c0c1ff', border:'1px solid rgba(99,102,241,0.2)' }}>
                  {tag.tagName}
                  <span className="ml-1 opacity-50">{tag.problemsSolved}</span>
                </span>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* ── Badges ── */}
      {badges.length > 0 && (
        <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.45}}
          className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl p-6 mb-6">
          <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface mb-4">
            Badges <span className="text-sm text-on-surface-variant font-normal ml-1">({badges.length})</span>
          </h3>
          <div className="flex flex-wrap gap-5">
            {badges.map(badge => (
              <div key={badge.id} className="flex flex-col items-center gap-1.5 group">
                <img src={badge.icon} alt={badge.displayName}
                  className="w-14 h-14 object-contain group-hover:scale-110 transition-transform drop-shadow-md"
                  loading="lazy"/>
                <span className="text-[10px] text-on-surface-variant text-center max-w-[60px] leading-tight">{badge.displayName}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* ── Recent Submissions ── */}
      <motion.div initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:0.5}}
        className="bg-surface-container/40 backdrop-blur-xl border border-white/8 rounded-2xl overflow-hidden">
        <div className="flex items-center justify-between p-5 border-b border-white/8">
          <h3 className="font-['Poppins'] text-lg font-semibold text-on-surface">Recent Submissions</h3>
          <a href={`https://leetcode.com/${username}`} target="_blank" rel="noopener noreferrer"
            className="text-xs text-primary hover:underline flex items-center gap-1">
            View all <ExternalLink className="w-3 h-3"/>
          </a>
        </div>
        {subsLoading ? (
          <div className="p-6 space-y-3">
            {[...Array(6)].map((_,i) => <div key={i} className="h-10 bg-surface-container rounded-xl animate-pulse"/>)}
          </div>
        ) : submissions.length === 0 ? (
          <div className="p-8 text-center text-on-surface-variant text-sm">No submissions found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-white/5">
                <tr className="text-[11px] text-on-surface-variant uppercase tracking-wider font-semibold">
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Problem</th>
                  <th className="px-4 py-3 text-left hidden sm:table-cell">Language</th>
                  <th className="px-4 py-3 text-left hidden md:table-cell">Time</th>
                </tr>
              </thead>
              <tbody>
                {submissions.map((sub, i) => <SubmissionRow key={sub.id} sub={sub} i={i}/>)}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>

    </div>
  );
}

// ── Skeleton loader ────────────────────────────────────────────
function CodingPageSkeleton() {
  return (
    <div className="min-h-screen bg-background pt-24 pb-16 px-5 md:px-10 lg:px-16 max-w-[1280px] mx-auto space-y-6 animate-pulse">
      <div className="h-12 w-72 bg-surface-container rounded-xl"/>
      <div className="h-6 w-96 bg-surface-container rounded-xl"/>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="h-72 bg-surface-container rounded-2xl"/>
        <div className="grid grid-cols-2 gap-4">
          {[1,2,3,4].map(i=><div key={i} className="h-32 bg-surface-container rounded-2xl"/>)}
        </div>
      </div>
      <div className="h-44 bg-surface-container rounded-2xl"/>
      <div className="h-52 bg-surface-container rounded-2xl"/>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="h-48 bg-surface-container rounded-2xl"/>
        <div className="h-48 bg-surface-container rounded-2xl"/>
      </div>
      <div className="h-64 bg-surface-container rounded-2xl"/>
    </div>
  );
}
