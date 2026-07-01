import os

# Define the full Real LeetCode API Script
LC_SCRIPT = """
<script>
/* ── REAL LEETCODE API VIA CORS PROXY ── */
const LEETCODE_USERNAME = 'YOUR_LEETCODE_USERNAME'; /* ← WE NEED TO CHANGE THIS */
const PROXY = 'https://corsproxy.io/?';
const LC_API = 'https://leetcode.com/graphql';

async function fetchLeetCode() {
  const query = `
    query($u: String!) {
      allQuestionsCount { difficulty count }
      matchedUser(username: $u) {
        submitStats: submitStatsGlobal {
          acSubmissionNum { difficulty count }
        }
        userCalendar {
          streak
          totalActiveDays
          submissionCalendar
        }
        profile { ranking }
        languageProblemCount { languageName problemsSolved }
      }
    }
  `;
  try {
    const res = await fetch(PROXY + encodeURIComponent(LC_API), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com' },
      body: JSON.stringify({ query, variables: { u: LEETCODE_USERNAME } })
    });
    return (await res.json()).data;
  } catch (e) {
    console.warn('LeetCode API unavailable', e);
    return null;
  }
}

async function initCodingPage() {
  if (LEETCODE_USERNAME === 'YOUR_LEETCODE_USERNAME') {
     console.log("Please update LEETCODE_USERNAME");
     return;
  }

  const data = await fetchLeetCode();
  if (!data || !data.matchedUser) return;

  const user = data.matchedUser;
  const stats = user.submitStats.acSubmissionNum;
  const allQ = data.allQuestionsCount;

  /* Total Solved */
  const totalSolved = stats.find(s => s.difficulty === 'All')?.count || 0;
  const tsEl = document.querySelector('[data-total-solved] .font-display-lg');
  if (tsEl) tsEl.textContent = totalSolved;

  const getS = diff => stats.find(s => s.difficulty === diff)?.count || 0;
  const getT = diff => allQ.find(q => q.difficulty === diff)?.count || 0;

  const solved = { Easy: getS('Easy'), Medium: getS('Medium'), Hard: getS('Hard') };
  const total  = { Easy: getT('Easy'), Medium: getT('Medium'), Hard: getT('Hard') };

  const easyPct = (solved.Easy / total.Easy) * 100 || 0;
  const medPct  = (solved.Medium / total.Medium) * 100 || 0;
  const hardPct = (solved.Hard / total.Hard) * 100 || 0;

  const streak = user.userCalendar.streak;
  const ranking = user.profile.ranking;
  let langs = user.languageProblemCount || [];
  langs.sort((a,b) => b.problemsSolved - a.problemsSolved);

  let calendarData = {};
  try {
    calendarData = JSON.parse(user.userCalendar.submissionCalendar || '{}');
  } catch(e) {}

  /* Update labels */
  const streakEl = document.querySelector('[data-streak]');
  if (streakEl) streakEl.textContent = streak + ' Days';
  const rankEl = document.querySelector('[data-rank]');
  if (rankEl) rankEl.textContent = '#' + ranking;
  const easy = document.querySelector('[data-easy-solved]');
  const med  = document.querySelector('[data-med-solved]');
  const hard = document.querySelector('[data-hard-solved]');
  if (easy) easy.textContent = solved.Easy + ' / ' + total.Easy;
  if (med)  med.textContent  = solved.Medium + ' / ' + total.Medium;
  if (hard) hard.textContent = solved.Hard + ' / ' + total.Hard;

  /* Animate Rings */
  setTimeout(() => {
    const ringEasy = document.getElementById('ring-easy');
    const ringMedium = document.getElementById('ring-medium');
    const ringHard = document.getElementById('ring-hard');
    if (ringEasy) ringEasy.style.strokeDashoffset = 502 - (easyPct / 100 * 502);
    if (ringMedium) ringMedium.style.strokeDashoffset = 377 - (medPct / 100 * 377);
    if (ringHard) ringHard.style.strokeDashoffset = 251 - (hardPct / 100 * 251);
  }, 500);

  /* Build Heatmap */
  const heatmapContainer = document.getElementById('heatmap-container');
  if (heatmapContainer) {
    heatmapContainer.innerHTML = '';
    const WEEKS = 20;
    const now = new Date();
    const days = [];
    for (let i = WEEKS * 7 - 1; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const ts = Math.floor(d.getTime() / 1000);
      let count = 0;
      /* Try to match timestamps within the same day */
      for (const [timestamp, cnt] of Object.entries(calendarData)) {
         const d2 = new Date(timestamp * 1000);
         if (d.getDate() === d2.getDate() && d.getMonth() === d2.getMonth() && d.getFullYear() === d2.getFullYear()) {
            count += cnt;
         }
      }
      days.push({ ts, count });
    }
    for (let w = 0; w < WEEKS; w++) {
      const col = document.createElement('div');
      col.className = 'flex flex-col gap-1';
      for (let d = 0; d < 7; d++) {
        const { count } = days[w * 7 + d];
        const sq = document.createElement('div');
        sq.className = 'w-3 h-3 rounded-sm transition-transform hover:scale-125 cursor-pointer';
        sq.title = count + ' submission' + (count !== 1 ? 's' : '');
        if (count === 0) sq.classList.add('bg-surface-container-highest', 'opacity-40');
        else if (count <= 1) sq.style.cssText = 'background:rgba(192,193,255,0.3)';
        else if (count <= 3) sq.style.cssText = 'background:rgba(192,193,255,0.6)';
        else if (count <= 6) sq.style.cssText = 'background:#c0c1ff';
        else sq.style.cssText = 'background:#8083ff;box-shadow:0 0 6px rgba(192,193,255,0.5)';
        col.appendChild(sq);
      }
      heatmapContainer.appendChild(col);
    }
  }

  /* Language Bars */
  const langContainer = document.querySelector('[data-langs]');
  if (langContainer && langs.length > 0) {
    const maxSolved = Math.max(...langs.map(l => l.problemsSolved));
    langContainer.innerHTML = langs.map(lang => {
      const pct = Math.round((lang.problemsSolved / maxSolved) * 100);
      return `
        <div>
          <div class="flex justify-between font-code-block text-[12px] mb-2 text-on-surface">
            <span>${lang.languageName}</span>
            <span class="text-primary">${pct}%</span>
          </div>
          <div class="w-full h-2 bg-surface-container rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-primary to-inverse-primary rounded-full" style="width:${pct}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }
}
document.addEventListener('DOMContentLoaded', initCodingPage);
</script>
"""

with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to replace the fake heatmap data script.
import re

# Remove the script block containing 'setCSSVars' and 'ring-easy' and 'Generate Fake Heatmap Data'
# Also remove the script block containing 'REAL LEETCODE API VIA CORS PROXY' if it exists.
parts = html.split('<script>')
new_parts = []
for p in parts:
    if 'setCSSVars' in p or 'REAL LEETCODE API VIA CORS PROXY' in p or 'ring-easy' in p:
        continue
    new_parts.append(p)

new_html = '<script>'.join(new_parts)

# Insert before SHARED.JS
if '<!-- ============================================================\n     SHARED.JS' in new_html:
    new_html = new_html.replace('<!-- ============================================================\n     SHARED.JS', LC_SCRIPT + '\n<!-- ============================================================\n     SHARED.JS')
else:
    new_html = new_html.replace('</body>', LC_SCRIPT + '\n</body>')

with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Injected real LeetCode API script")
