import { useMemo } from 'react';
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
