import { motion } from 'framer-motion';

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
