import os
import glob
import re

FOLDER = r'C:\Users\girip\Desktop\Portfolio_pradipta'

SHARED_JS = r"""
<!-- ============================================================
     SHARED.JS
     ============================================================ -->
<script>
/* ── 1. DARK MODE (single definition, no duplicates) ── */
(function () {
  const saved = localStorage.getItem('theme');
  document.documentElement.classList.toggle('dark', saved !== 'light');
})();

function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  /* Rotate the icon */
  const icon = document.querySelector('[data-darkmode-icon]');
  if (icon) icon.style.transform = isDark ? 'rotate(360deg)' : 'rotate(0deg)';
}

/* ── 2. MOBILE MENU ── */
function toggleMobileMenu() {
  const m = document.getElementById('mobile-menu');
  if (!m) return;
  const isHidden = m.classList.toggle('hidden');
  document.body.style.overflow = isHidden ? '' : 'hidden';
}
/* Close mobile menu on ESC */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    const m = document.getElementById('mobile-menu');
    if (m && !m.classList.contains('hidden')) toggleMobileMenu();
  }
});

/* ── 3. ALL ANIMATIONS & UTILITIES ── */
document.addEventListener('DOMContentLoaded', function () {

  /* Inject animation styles */
  const style = document.createElement('style');
  style.textContent = `
    /* Scroll reveal */
    .anim-fade-up {
      opacity: 0;
      transform: translateY(28px);
      transition: opacity 0.65s cubic-bezier(0.16,1,0.3,1),
                  transform 0.65s cubic-bezier(0.16,1,0.3,1);
    }
    .anim-fade-up.visible { opacity: 1; transform: translateY(0); }
    .anim-fade-up:nth-child(2) { transition-delay: 0.08s; }
    .anim-fade-up:nth-child(3) { transition-delay: 0.16s; }
    .anim-fade-up:nth-child(4) { transition-delay: 0.24s; }
    .anim-fade-up:nth-child(5) { transition-delay: 0.32s; }
    .anim-fade-up:nth-child(6) { transition-delay: 0.40s; }

    /* Page loader */
    #page-loader {
      position: fixed; inset: 0; z-index: 9999;
      background: #0b0f1a;
      display: flex; align-items: center; justify-content: center;
      transition: opacity 0.5s ease;
    }
    #page-loader.done { opacity: 0; pointer-events: none; }
    #page-loader .ring {
      width: 44px; height: 44px;
      border: 3px solid rgba(192,193,255,0.15);
      border-top-color: #c0c1ff;
      border-radius: 50%;
      animation: spin-ring 0.8s linear infinite;
    }
    @keyframes spin-ring { to { transform: rotate(360deg); } }

    /* Counter */
    .counter-val { display: inline-block; }

    /* Shake (admin login) */
    @keyframes shake {
      0%,100% { transform: translateX(0); }
      20% { transform: translateX(-8px); }
      40% { transform: translateX(8px); }
      60% { transform: translateX(-5px); }
      80% { transform: translateX(5px); }
    }
    .shake { animation: shake 0.45s ease; }

    /* Pop-in (contact success) */
    @keyframes pop-in {
      0% { transform: scale(0); opacity: 0; }
      70% { transform: scale(1.15); }
      100% { transform: scale(1); opacity: 1; }
    }
    .pop-in { animation: pop-in 0.4s ease forwards; }

    /* Skeleton shimmer */
    .skeleton {
      background: linear-gradient(90deg, #1f1f27 25%, #292932 50%, #1f1f27 75%);
      background-size: 800px 100%;
      animation: shimmer 1.4s infinite;
      border-radius: 8px;
    }
    @keyframes shimmer {
      0% { background-position: -400px 0; }
      100% { background-position: 400px 0; }
    }

    /* Orb float */
    @keyframes float-orb {
      0%,100% { transform: translateY(0) scale(1); }
      50% { transform: translateY(-22px) scale(1.05); }
    }
    .orb-float  { animation: float-orb  8s ease-in-out infinite; }
    .orb-float-2{ animation: float-orb 10s ease-in-out infinite 2s; }
    .orb-float-3{ animation: float-orb 12s ease-in-out infinite 4s; }

    /* Skill bars */
    .skill-bar-fill {
      width: 0 !important;
      transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
    }
    .skill-bar-fill.animated { width: var(--target-w) !important; }

    /* Navbar scroll shadow */
    .nav-scrolled { box-shadow: 0 4px 24px rgba(0,0,0,0.45) !important; }

    /* Scroll to top button */
    #scroll-top {
      position: fixed; bottom: 1.5rem; right: 1.5rem;
      width: 44px; height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, #c0c1ff, #8b5cf6);
      color: #1000a9;
      border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      opacity: 0; visibility: hidden;
      transform: translateY(10px);
      transition: all 0.3s ease;
      z-index: 999;
      box-shadow: 0 4px 16px rgba(192,193,255,0.35);
    }
    #scroll-top.visible { opacity: 1; visibility: visible; transform: translateY(0); }
    #scroll-top:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(192,193,255,0.5); }

    /* Dark mode toggle spin */
    button[onclick="toggleDarkMode()"] span {
      display: inline-block;
      transition: transform 0.6s cubic-bezier(0.34,1.56,0.64,1);
    }
    button[onclick="toggleDarkMode()"]:active span {
      transform: rotate(360deg);
    }
  `;
  document.head.appendChild(style);

  /* ── PAGE LOADER ── */
  let loader = document.getElementById('page-loader');
  if (!loader) {
    loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = '<div class="ring"></div>';
    document.body.prepend(loader);
  }
  window.addEventListener('load', () => {
    setTimeout(() => loader && loader.classList.add('done'), 400);
    setTimeout(() => loader && loader.remove(), 950);
  });

  /* ── SCROLL REVEAL ── */
  const revealTargets = document.querySelectorAll(
    'article, section > div, .glass-panel, [class*="rounded-xl"]'
  );
  revealTargets.forEach(el => {
    if (!el.closest('nav') && !el.closest('header') &&
        !el.closest('#mobile-menu') && !el.closest('#page-loader')) {
      el.classList.add('anim-fade-up');
    }
  });
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); }
    });
  }, { threshold: 0.07, rootMargin: '0px 0px -36px 0px' });
  document.querySelectorAll('.anim-fade-up').forEach(el => revealObs.observe(el));

  /* ── NAVBAR SCROLL SHADOW ── */
  const nav = document.querySelector('header, nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('nav-scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ── ANIMATED COUNTERS ── */
  const counterObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = parseInt(el.dataset.target || el.innerText, 10);
      const suffix = el.dataset.suffix || '';
      if (isNaN(target)) return;
      const start = performance.now();
      const duration = 1400;
      function tick(now) {
        const p = Math.min((now - start) / duration, 1);
        const ease = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.floor(ease * target) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      counterObs.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.counter-val').forEach(el => counterObs.observe(el));

  /* ── SKILL BARS ── */
  const barObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const w = e.target.style.width || e.target.dataset.width || '0%';
        e.target.style.setProperty('--target-w', w);
        e.target.style.width = '0';
        setTimeout(() => e.target.classList.add('skill-bar-fill', 'animated'), 50);
        barObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.fill-bar, .skill-bar-fill, [data-width]').forEach(b => barObs.observe(b));

  /* ── SCROLL TO TOP ── */
  let scrollBtn = document.getElementById('scroll-top');
  if (!scrollBtn) {
    scrollBtn = document.createElement('button');
    scrollBtn.id = 'scroll-top';
    scrollBtn.title = 'Back to top';
    scrollBtn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px">arrow_upward</span>';
    scrollBtn.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    document.body.appendChild(scrollBtn);
  }
  window.addEventListener('scroll', () => {
    scrollBtn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

}); /* end DOMContentLoaded */
</script>
"""

CODING_JS = r"""
<script>
/* ── REAL LEETCODE API VIA CORS PROXY ── */
const LEETCODE_USERNAME = 'YOUR_LEETCODE_USERNAME'; /* ← change this */
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
    console.warn('LeetCode API unavailable, using demo data');
    return null;
  }
}

async function initCodingPage() {
  /* ── 1. Animate SVG rings (set correct offsets before API loads) ── */
  const data = await fetchLeetCode();

  let easyPct = 31, medPct = 9, hardPct = 3.5;
  let totalSolved = 425, streak = 42, ranking = '—';
  let langs = [
    { languageName: 'C++', problemsSolved: 65 },
    { languageName: 'Python3', problemsSolved: 25 },
    { languageName: 'Java', problemsSolved: 10 },
  ];
  let calendarData = {};

  if (data && data.matchedUser) {
    const u = data.matchedUser;
    const stats = u.submitStats.acSubmissionNum;
    const all = data.allQuestionsCount;

    const solved = {
      All:    stats.find(s => s.difficulty === 'All')?.count    ?? 0,
      Easy:   stats.find(s => s.difficulty === 'Easy')?.count   ?? 0,
      Medium: stats.find(s => s.difficulty === 'Medium')?.count ?? 0,
      Hard:   stats.find(s => s.difficulty === 'Hard')?.count   ?? 0,
    };
    const total = {
      Easy:   all.find(s => s.difficulty === 'Easy')?.count   ?? 800,
      Medium: all.find(s => s.difficulty === 'Medium')?.count ?? 1700,
      Hard:   all.find(s => s.difficulty === 'Hard')?.count   ?? 700,
    };

    totalSolved = solved.All;
    easyPct   = total.Easy   > 0 ? (solved.Easy   / total.Easy)   * 100 : 0;
    medPct    = total.Medium > 0 ? (solved.Medium / total.Medium) * 100 : 0;
    hardPct   = total.Hard   > 0 ? (solved.Hard   / total.Hard)   * 100 : 0;
    streak    = u.userCalendar?.streak ?? 0;
    ranking   = u.profile.ranking?.toLocaleString() ?? '—';
    langs     = (u.languageProblemCount || langs).slice(0, 3);

    try { calendarData = JSON.parse(u.userCalendar?.submissionCalendar || '{}'); } catch { }

    /* Update DOM */
    const totalEl = document.querySelector('.progress-ring__circle')
      ?.closest('.relative')?.querySelector('.text-display-lg-mobile');
    if (totalEl) totalEl.textContent = totalSolved;

    /* Update streak badge */
    const streakEl = document.querySelector('[data-streak]');
    if (streakEl) streakEl.textContent = streak + ' Days';

    /* Update ranking */
    const rankEl = document.querySelector('[data-rank]');
    if (rankEl) rankEl.textContent = '#' + ranking;

    /* Update solved counts in legend */
    const easy   = document.querySelector('[data-easy-solved]');
    const med    = document.querySelector('[data-med-solved]');
    const hard   = document.querySelector('[data-hard-solved]');
    if (easy) easy.textContent   = solved.Easy   + ' / ' + total.Easy;
    if (med)  med.textContent    = solved.Medium + ' / ' + total.Medium;
    if (hard) hard.textContent   = solved.Hard   + ' / ' + total.Hard;
  }

  /* ── 2. Animate SVG rings ── */
  setTimeout(() => {
    const ringEasy   = document.getElementById('ring-easy');
    const ringMedium = document.getElementById('ring-medium');
    const ringHard   = document.getElementById('ring-hard');
    if (ringEasy)   ringEasy.style.strokeDashoffset   = 502 - (easyPct / 100 * 502);
    if (ringMedium) ringMedium.style.strokeDashoffset = 377 - (medPct  / 100 * 377);
    if (ringHard)   ringHard.style.strokeDashoffset   = 251 - (hardPct / 100 * 251);
  }, 500);

  /* ── 3. Real submission heatmap ── */
  const heatmapContainer = document.getElementById('heatmap-container');
  if (heatmapContainer) {
    heatmapContainer.innerHTML = '';
    const WEEKS = 20;
    const now = new Date();

    /* Build array of last 20*7 days */
    const days = [];
    for (let i = WEEKS * 7 - 1; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const ts = Math.floor(d.getTime() / 1000);
      days.push({ ts, count: calendarData[ts] || 0 });
    }

    /* Group into weeks */
    for (let w = 0; w < WEEKS; w++) {
      const col = document.createElement('div');
      col.className = 'flex flex-col gap-1';
      for (let d = 0; d < 7; d++) {
        const { count } = days[w * 7 + d];
        const sq = document.createElement('div');
        sq.className = 'w-3 h-3 rounded-sm transition-transform hover:scale-125 cursor-pointer';
        sq.title = count + ' submission' + (count !== 1 ? 's' : '');
        if      (count === 0) sq.classList.add('bg-surface-container-highest', 'opacity-40');
        else if (count <= 1)  sq.style.cssText = 'background:rgba(192,193,255,0.3)';
        else if (count <= 3)  sq.style.cssText = 'background:rgba(192,193,255,0.6)';
        else if (count <= 6)  sq.style.cssText = 'background:#c0c1ff';
        else                  sq.style.cssText = 'background:#8083ff;box-shadow:0 0 6px rgba(192,193,255,0.5)';
        col.appendChild(sq);
      }
      heatmapContainer.appendChild(col);
    }
  }

  /* ── 4. Language bars ── */
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
            <div class="h-full bg-gradient-to-r from-primary to-inverse-primary rounded-full"
                 style="width:${pct}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }
}

/* ── Run on load ── */
document.addEventListener('DOMContentLoaded', initCodingPage);

/* ── Scroll reveal for coding page ── */
document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal-up');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('active'); obs.unobserve(e.target); } });
  }, { threshold: 0.1 });
  els.forEach(el => obs.observe(el));
});
</script>
"""

ADMIN_JS = r"""
<script>
/* Admin login — fixed (no more missing btnLoader reference) */
const ADMIN_EMAIL = 'admin@portfolio.local';
const ADMIN_PASS  = 'Admin@1234'; /* Change this before deploying */

function handleLogin(event) {
  event.preventDefault();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const btn      = document.getElementById('loginBtn');
  const btnText  = document.getElementById('btnText');
  const card     = btn?.closest('.rounded-xl');

  if (!btn || !btnText) return;

  /* Loading state */
  btnText.textContent = 'AUTHENTICATING...';
  btn.style.opacity = '0.7';
  btn.style.pointerEvents = 'none';

  setTimeout(() => {
    if (email === ADMIN_EMAIL && password === ADMIN_PASS) {
      /* ✅ SUCCESS */
      localStorage.setItem('admin_token', btoa(email + ':' + Date.now()));
      btnText.textContent = 'ACCESS GRANTED ✓';
      btn.style.background = 'linear-gradient(90deg, #10b981, #059669)';
      btn.style.boxShadow = '0 0 20px rgba(16,185,129,0.4)';
      setTimeout(() => { window.location.href = 'dashboard.html'; }, 700);
    } else {
      /* ❌ FAIL — shake card */
      if (card) {
        card.classList.add('shake');
        card.addEventListener('animationend', () => card.classList.remove('shake'), { once: true });
      }
      /* Flash inputs red */
      ['email', 'password'].forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        el.style.borderColor = '#ef4444';
        el.style.boxShadow = '0 0 0 2px rgba(239,68,68,0.25)';
        setTimeout(() => { el.style.borderColor = ''; el.style.boxShadow = ''; }, 1400);
      });
      /* Toast */
      showToast('⚠️ Invalid credentials. Access denied.');
      /* Reset button */
      btnText.textContent = 'Initialize Session';
      btn.style.opacity = '';
      btn.style.pointerEvents = '';
      btn.style.background = '';
      btn.style.boxShadow = '';
    }
  }, 1000);
}

function showToast(msg) {
  let t = document.getElementById('login-toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'login-toast';
    t.style.cssText = `
      position:fixed; bottom:24px; right:24px; z-index:9999;
      background:#1f1f27; border:1px solid #ef4444;
      color:#fca5a5; padding:12px 20px; border-radius:12px;
      font-size:13px; box-shadow:0 4px 20px rgba(0,0,0,0.4);
      transition: opacity 0.4s ease, transform 0.4s ease;
      opacity:0; transform:translateY(16px);
    `;
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  t.style.transform = 'translateY(0)';
  clearTimeout(t._timer);
  t._timer = setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(16px)';
  }, 3200);
}

/* Wire the form's onsubmit to handleLogin */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('adminLoginForm');
  if (form && !form.getAttribute('onsubmit')) {
    form.addEventListener('submit', handleLogin);
  }
  /* If already logged in, skip to dashboard */
  if (localStorage.getItem('admin_token')) {
    window.location.replace('dashboard.html');
  }
});
</script>
"""

CONTACT_JS = r"""
<script>
/* Contact form — complete validation + success animation */

function validateField(id, test, errMsg) {
  const el  = document.getElementById(id);
  if (!el) return true;
  const ok  = test(el.value.trim());
  const err = document.getElementById(id + '-err');
  el.classList.toggle('border-error', !ok);
  el.classList.toggle('border-primary/50', ok && el.value.trim().length > 0);
  if (err) { err.textContent = ok ? '' : errMsg; err.style.display = ok ? 'none' : 'block'; }
  return ok;
}

function injectFieldErrors() {
  ['name', 'email', 'message'].forEach(id => {
    const el = document.getElementById(id);
    if (!el || document.getElementById(id + '-err')) return;
    const err = document.createElement('span');
    err.id   = id + '-err';
    err.style.cssText = 'color:#ffb4ab;font-size:11px;margin-top:3px;display:none;font-family:Inter,sans-serif;';
    el.parentNode.appendChild(err);
  });
}

function liveValidate(id) {
  const rules = {
    name:    { test: v => v.length >= 2,                         msg: 'Name must be at least 2 characters.' },
    email:   { test: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), msg: 'Please enter a valid email address.' },
    message: { test: v => v.length >= 10,                        msg: 'Message too short (minimum 10 characters).' },
  };
  const r = rules[id];
  if (r) validateField(id, r.test, r.msg);
}

function submitForm() {
  const nameOk  = validateField('name',    v => v.length >= 2,                          'Name is required.');
  const emailOk = validateField('email',   v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),  'Valid email required.');
  const msgOk   = validateField('message', v => v.length >= 10,                         'Please write a message (min 10 chars).');
  if (!nameOk || !emailOk || !msgOk) return;

  const form    = document.getElementById('contactForm');
  const btn     = document.getElementById('submitBtn');
  const success = document.getElementById('successState');
  if (!form || !btn || !success) return;

  btn.disabled = true;
  btn.innerHTML = `<span style="display:inline-flex;align-items:center;gap:8px;">
    <span class="material-symbols-outlined" style="animation:spin-contact 1s linear infinite;display:inline-block;">sync</span>
    Processing...
  </span>`;
  btn.style.opacity = '0.75';

  /* Simulate send — wire to your real API endpoint here */
  setTimeout(() => {
    form.style.display = 'none';
    success.classList.remove('hidden');
    success.classList.add('flex');
    success.style.cssText = 'opacity:0;transform:translateY(16px);transition:all 0.4s ease;';
    requestAnimationFrame(() => {
      success.style.opacity = '1';
      success.style.transform = 'translateY(0)';
    });
    const icon = success.querySelector('.material-symbols-outlined');
    if (icon) icon.classList.add('pop-in');
  }, 1200);
}

function resetForm() {
  const form    = document.getElementById('contactForm');
  const btn     = document.getElementById('submitBtn');
  const success = document.getElementById('successState');
  if (!form) return;
  form.reset();
  form.style.display = '';
  success && success.classList.add('hidden') && success.classList.remove('flex');
  btn.disabled = false;
  btn.style.opacity = '';
  btn.innerHTML = `
    <span class="relative z-10 flex items-center gap-2 font-bold tracking-wide">
      Execute Post Request
      <span class="material-symbols-outlined">send</span>
    </span>`;
}

document.addEventListener('DOMContentLoaded', () => {
  injectFieldErrors();
  /* Live blur validation */
  ['name', 'email', 'message'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('blur', () => liveValidate(id));
  });
  /* Wire form if no onsubmit */
  const form = document.getElementById('contactForm');
  if (form && !form.onsubmit) {
    form.addEventListener('submit', e => { e.preventDefault(); submitForm(); });
  }
});

/* Spin animation for the loading state */
const s = document.createElement('style');
s.textContent = '@keyframes spin-contact { to { transform: rotate(360deg); } }';
document.head.appendChild(s);
</script>
"""

DASHBOARD_MENU = r"""
<div id="mobile-menu" class="fixed inset-0 z-[60] hidden md:hidden">
  <div class="absolute inset-0 bg-background/90 backdrop-blur-md" onclick="toggleMobileMenu()"></div>
  <!-- Mobile sidebar — mirrors the desktop sidebar -->
  <div class="absolute left-0 top-0 h-full w-72 flex flex-col p-6 pt-6 border-r border-outline-variant/20"
       style="background:#1f1f27;">
    <div class="flex items-center justify-between mb-8">
      <span class="font-display-lg-mobile text-display-lg-mobile bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent">SYS.ADMIN</span>
      <button onclick="toggleMobileMenu()" class="text-on-surface-variant hover:text-primary">
        <span class="material-symbols-outlined">close</span>
      </button>
    </div>
    <nav class="flex flex-col gap-1">
      <a class="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary-container/10 text-primary font-label-caps text-label-caps border-l-2 border-primary" href="dashboard.html">
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">dashboard</span> Overview</a>
      <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-projects.html">
        <span class="material-symbols-outlined">folder_open</span> Projects</a>
      <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-certs.html">
        <span class="material-symbols-outlined">workspace_premium</span> Certificates</a>
      <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-research.html">
        <span class="material-symbols-outlined">science</span> Research</a>
      <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-skills.html">
        <span class="material-symbols-outlined">code</span> Skills</a>
      <div class="border-t border-outline-variant/20 mt-4 pt-4">
        <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-profile.html">
          <span class="material-symbols-outlined">person</span> Profile</a>
        <a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:text-primary hover:bg-surface-container-high font-label-caps text-label-caps transition-all" href="dashboard-messages.html">
          <span class="material-symbols-outlined">mail</span> Messages
          <span class="ml-auto bg-error text-on-error font-label-caps text-label-caps px-2 py-0.5 rounded-full text-[10px]">3</span></a>
      </div>
    </nav>
    <div class="mt-auto pt-4 border-t border-outline-variant/20">
      <button onclick="adminLogout()" class="flex items-center gap-3 px-4 py-3 rounded-lg text-error hover:bg-error/10 font-label-caps text-label-caps transition-all w-full">
        <span class="material-symbols-outlined">logout</span> Sign Out
      </button>
    </div>
  </div>
</div>
"""

DASHBOARD_JS = r"""
<script>
/* ── DASHBOARD AUTH GUARD ── */
(function() {
  if (!localStorage.getItem('admin_token')) {
    window.location.replace('admin.html');
  }
})();

function adminLogout() {
  if (confirm('Sign out of admin session?')) {
    localStorage.removeItem('admin_token');
    window.location.href = 'admin.html';
  }
}

/* ── Wire the logout icon in sidebar ── */
document.addEventListener('DOMContentLoaded', () => {
  /* Desktop logout link (the <a> with logout icon) */
  const logoutLink = document.querySelector('a[href="admin.html"] .material-symbols-outlined');
  if (logoutLink?.textContent.trim() === 'logout') {
    logoutLink.closest('a').addEventListener('click', e => {
      e.preventDefault();
      adminLogout();
    });
  }

  /* Mobile menu hamburger in header */
  const mobileToggle = document.querySelector('.md\\:hidden button, button.md\\:hidden');
  if (mobileToggle) mobileToggle.onclick = toggleMobileMenu;
});

/* ── ADD PROJECT MODAL ── */
function openAddModal() {
  const m = document.getElementById('add-modal');
  if (m) {
    m.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}
function closeAddModal() {
  const m = document.getElementById('add-modal');
  if (m) {
    m.classList.add('hidden');
    document.body.style.overflow = '';
  }
}
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeAddModal();
});
</script>
"""

html_files = glob.glob(os.path.join(FOLDER, "*.html"))

for file in html_files:
    basename = os.path.basename(file)
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all scripts
    # We want to remove scripts that contain 'toggleDarkMode' or 'revealTargets' etc.
    def repl_script(m):
        code = m.group(1)
        if any(x in code for x in ['toggleDarkMode', 'revealTargets', 'handleLogin', 'adminLogout', 'validateField']):
            return '' # remove
        return m.group(0) # keep
    
    # Remove existing conflicting scripts
    content = re.sub(r'<script(?:[^>]*(?!src=)[^>]*)?>(.*?)</script>', repl_script, content, flags=re.DOTALL)
    
    # Append SHARED_JS before </body>
    content = content.replace('</body>', SHARED_JS + '\n</body>')

    if basename == 'coding.html':
        content = re.sub(r'<a href="#"([^>]*View LeetCode Profile.*?)>', r'<a href="https://leetcode.com/YOUR_USERNAME" target="_blank" rel="noopener noreferrer"\1>', content)
        content = content.replace('</body>', CODING_JS + '\n</body>')
    
    elif basename == 'admin.html':
        content = content.replace('</body>', ADMIN_JS + '\n</body>')
        
    elif basename == 'contact.html':
        content = content.replace('class="mb-unit-xl animate-slide-up text-center md:text-left hidden"', 'class="mb-unit-xl animate-slide-up text-center md:text-left"')
        content = content.replace('</body>', CONTACT_JS + '\n</body>')
        
    elif basename == 'dashboard.html':
        # Replace the entire <div id="mobile-menu"...</div>
        # A simple regex to replace it:
        content = re.sub(r'<div id="mobile-menu".*?</div>\s*</div>\s*</div>', DASHBOARD_MENU, content, flags=re.DOTALL)
        content = content.replace('</body>', DASHBOARD_JS + '\n</body>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied fixes to {basename}")
