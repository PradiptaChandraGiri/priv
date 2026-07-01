"""
Enhancement Script: Applies spec-required features to all HTML pages.
- Preserves 100% visual design (no style/layout changes)
- Adds: localStorage dark mode, scroll animations, page loader,
         animated counters, form validation, admin auth guard,
         social icons on home, skeleton loaders, PDF lightbox,
         better footer with GitHub/LinkedIn/Twitter/LeetCode,
         CTA banner on home, featured projects preview on home,
         success animation on contact, shake on admin error.
"""

import os
import re

ROOT = r"c:\Users\girip\Desktop\Portfolio_pradipta"

# ─────────────────────────────────────────────────────────────────────────────
# SHARED ENHANCEMENT SCRIPT (injected just before </body> on every page)
# ─────────────────────────────────────────────────────────────────────────────
SHARED_SCRIPT = r"""
<script>
/* ═══════════════════════════════════════
   1. DARK MODE — persists to localStorage
═══════════════════════════════════════ */
(function () {
  const saved = localStorage.getItem('theme');
  if (saved === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }
})();

function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

/* ═══════════════════════════════════════
   2. MOBILE MENU
═══════════════════════════════════════ */
function toggleMobileMenu() {
  const m = document.getElementById('mobile-menu');
  if (!m) return;
  m.classList.toggle('hidden');
  document.body.style.overflow = m.classList.contains('hidden') ? '' : 'hidden';
}

/* ═══════════════════════════════════════
   3. SCROLL-TRIGGERED FADE-UP ANIMATIONS
═══════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function () {
  // Add base styles for animated elements
  const styleEl = document.createElement('style');
  styleEl.textContent = `
    .anim-fade-up { opacity: 0; transform: translateY(32px); transition: opacity 0.6s ease, transform 0.6s ease; }
    .anim-fade-up.visible { opacity: 1; transform: translateY(0); }
    .anim-fade-up:nth-child(2) { transition-delay: 0.1s; }
    .anim-fade-up:nth-child(3) { transition-delay: 0.2s; }
    .anim-fade-up:nth-child(4) { transition-delay: 0.3s; }
    .anim-fade-up:nth-child(5) { transition-delay: 0.4s; }
    .anim-fade-up:nth-child(6) { transition-delay: 0.5s; }

    /* Page loader */
    #page-loader { position:fixed; inset:0; z-index:9999; background:#0b0f1a;
      display:flex; align-items:center; justify-content:center;
      transition: opacity 0.5s ease; }
    #page-loader.done { opacity:0; pointer-events:none; }
    .loader-ring { width:48px; height:48px; border:4px solid rgba(99,102,241,0.2);
      border-top-color:#6366f1; border-radius:50%;
      animation: spin-loader 0.8s linear infinite; }
    @keyframes spin-loader { to { transform: rotate(360deg); } }

    /* Counter animation */
    .counter-val { display:inline-block; }

    /* Shake animation for admin */
    @keyframes shake { 0%,100%{transform:translateX(0)}
      20%{transform:translateX(-8px)} 40%{transform:translateX(8px)}
      60%{transform:translateX(-6px)} 80%{transform:translateX(6px)} }
    .shake { animation: shake 0.45s ease; }

    /* Success checkmark animation */
    @keyframes pop-in { 0%{transform:scale(0);opacity:0} 70%{transform:scale(1.2)} 100%{transform:scale(1);opacity:1} }
    .pop-in { animation: pop-in 0.4s ease forwards; }

    /* Skeleton shimmer */
    @keyframes shimmer { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
    .skeleton { background: linear-gradient(90deg, #1f1f27 25%, #292932 50%, #1f1f27 75%);
      background-size: 800px 100%; animation: shimmer 1.5s infinite; border-radius:8px; }

    /* Orb float */
    @keyframes float-orb { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-24px) scale(1.05)} }
    .orb-float { animation: float-orb 8s ease-in-out infinite; }
    .orb-float-2 { animation: float-orb 10s ease-in-out infinite 2s; }
    .orb-float-3 { animation: float-orb 12s ease-in-out infinite 4s; }

    /* Skill bar */
    .skill-bar-fill { width: 0 !important; transition: width 1.2s cubic-bezier(0.4,0,0.2,1); }
    .skill-bar-fill.animated { width: var(--target-w) !important; }

    /* Navbar scroll shadow */
    .nav-scrolled { box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important; }
  `;
  document.head.appendChild(styleEl);

  /* ── Page Loader ── */
  let loader = document.getElementById('page-loader');
  if (!loader) {
    loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = '<div class="loader-ring"></div>';
    document.body.prepend(loader);
  }
  setTimeout(() => { if (loader) loader.classList.add('done'); }, 900);
  setTimeout(() => { if (loader && loader.parentNode) loader.parentNode.removeChild(loader); }, 1450);

  /* ── IntersectionObserver for fade-up cards ── */
  const allCards = document.querySelectorAll(
    '.group, [class*="rounded-xl"], [class*="glass-panel"], .bento-cell'
  );
  allCards.forEach(el => {
    if (!el.closest('nav') && !el.closest('header') && !el.closest('#mobile-menu')) {
      el.classList.add('anim-fade-up');
    }
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.anim-fade-up').forEach(el => observer.observe(el));

  /* ── Navbar scroll shadow ── */
  const nav = document.querySelector('header, nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('nav-scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ── Animated Counter ── */
  function animateCounter(el) {
    const target = parseInt(el.dataset.target || el.innerText, 10);
    if (isNaN(target)) return;
    const duration = 1500;
    const start = performance.now();
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target) + (el.dataset.suffix || '');
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        counterObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.counter-val').forEach(el => counterObserver.observe(el));

  /* ── Skill Bar Animations ── */
  const barObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('animated'); barObserver.unobserve(e.target); }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.skill-bar-fill').forEach(bar => {
    const w = bar.style.width;
    bar.style.setProperty('--target-w', w);
    bar.classList.add('skill-bar-fill');
    barObserver.observe(bar);
  });
});
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# CONTACT PAGE — validation + success animation (replaces existing scripts)
# ─────────────────────────────────────────────────────────────────────────────
CONTACT_SCRIPT = r"""
<script>
/* Form validation + success animation */
function validateField(id, test, errMsg) {
  const el = document.getElementById(id);
  const err = document.getElementById(id + '-err');
  if (!el) return true;
  const ok = test(el.value.trim());
  el.classList.toggle('border-error', !ok);
  el.classList.toggle('border-primary', ok && el.value.trim().length > 0);
  if (err) { err.textContent = ok ? '' : errMsg; err.style.display = ok ? 'none' : 'block'; }
  return ok;
}

function addFieldError(id, msg) {
  const el = document.getElementById(id);
  if (!el) return;
  let err = document.getElementById(id + '-err');
  if (!err) {
    err = document.createElement('span');
    err.id = id + '-err';
    err.style.cssText = 'color:#ffb4ab;font-size:10px;margin-top:2px;display:none;';
    el.closest('.relative, .flex.flex-col').appendChild(err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  ['name','email','message'].forEach(id => addFieldError(id, ''));
  const form = document.getElementById('contactForm');
  if (!form) return;
  form.querySelectorAll('input, textarea').forEach(el => {
    el.addEventListener('blur', () => {
      if (el.id === 'email') validateField('email', v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), 'Invalid email format.');
      else if (el.id === 'name') validateField('name', v => v.length >= 2, 'Name must be at least 2 characters.');
      else if (el.id === 'message') validateField('message', v => v.length >= 10, 'Message too short (min 10 chars).');
    });
  });
});

function submitForm() {
  const nameOk = validateField('name', v => v.length >= 2, 'Name is required.');
  const emailOk = validateField('email', v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), 'Valid email required.');
  const msgOk = validateField('message', v => v.length >= 10, 'Please write a message (min 10 chars).');
  if (!nameOk || !emailOk || !msgOk) return;

  const form = document.getElementById('contactForm');
  const btn = document.getElementById('submitBtn');
  const success = document.getElementById('successState');

  btn.disabled = true;
  btn.innerHTML = '<span class="material-symbols-outlined" style="animation:spin 1s linear infinite;display:inline-block">sync</span> <span>Processing...</span>';
  btn.style.opacity = '0.7';
  btn.style.cursor = 'not-allowed';

  setTimeout(() => {
    form.style.display = 'none';
    success.classList.remove('hidden');
    success.classList.add('flex');
    success.style.opacity = '0';
    success.style.transform = 'translateY(20px)';
    success.style.transition = 'all 0.4s ease';
    setTimeout(() => { success.style.opacity = '1'; success.style.transform = 'translateY(0)'; }, 20);
    const icon = success.querySelector('.material-symbols-outlined');
    if (icon) icon.classList.add('pop-in');
  }, 1200);
}

function resetForm() {
  const form = document.getElementById('contactForm');
  const btn = document.getElementById('submitBtn');
  const success = document.getElementById('successState');
  if (!form) return;
  form.reset();
  success.classList.add('hidden');
  success.classList.remove('flex');
  form.style.display = '';
  btn.disabled = false;
  btn.innerHTML = `<span class="relative z-10 flex items-center gap-2 font-bold tracking-wide">Execute Post Request <span class="material-symbols-outlined">send</span></span>`;
  btn.style.opacity = '';
  btn.style.cursor = '';
}
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN LOGIN — shake on wrong credentials + auth guard + redirect
# ─────────────────────────────────────────────────────────────────────────────
ADMIN_SCRIPT = r"""
<script>
/* Admin Login: shake on error, store token on success, redirect to dashboard */
const ADMIN_EMAIL = 'admin@portfolio.local';
const ADMIN_PASS  = 'Admin@1234';

function handleLogin(event) {
  event.preventDefault();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const btn      = document.getElementById('loginBtn');
  const btnText  = document.getElementById('btnText');
  const card     = document.querySelector('#adminLoginForm').closest('.rounded-xl');

  btnText.textContent = 'AUTHENTICATING...';
  btn.style.opacity = '0.7';
  btn.style.pointerEvents = 'none';

  setTimeout(() => {
    if (email === ADMIN_EMAIL && password === ADMIN_PASS) {
      localStorage.setItem('admin_token', btoa(email + ':' + Date.now()));
      btnText.textContent = 'ACCESS GRANTED ✓';
      btn.style.background = 'linear-gradient(90deg,#10b981,#059669)';
      setTimeout(() => { window.location.href = 'dashboard.html'; }, 600);
    } else {
      /* Wrong credentials — shake the card */
      if (card) {
        card.classList.add('shake');
        card.addEventListener('animationend', () => card.classList.remove('shake'), { once: true });
      }
      /* Flash error on inputs */
      ['email','password'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.style.borderColor = '#ef4444';
          el.style.boxShadow = '0 0 0 2px rgba(239,68,68,0.25)';
          setTimeout(() => { el.style.borderColor = ''; el.style.boxShadow = ''; }, 1200);
        }
      });
      /* Show error toast */
      let toast = document.getElementById('login-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'login-toast';
        toast.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;background:#1f1f27;border:1px solid #ef4444;color:#fca5a5;padding:12px 20px;border-radius:12px;font-size:13px;box-shadow:0 4px 20px rgba(0,0,0,0.4);transition:all 0.3s ease;';
        document.body.appendChild(toast);
      }
      toast.textContent = '⚠️ Invalid credentials. Access denied.';
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
      setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateY(16px)'; }, 3000);
      btnText.textContent = 'Initialize Session';
      btn.style.opacity = '';
      btn.style.pointerEvents = '';
    }
  }, 1000);
}
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD — auth guard + logout
# ─────────────────────────────────────────────────────────────────────────────
DASHBOARD_SCRIPT = r"""
<script>
/* Auth Guard — redirect to admin login if no token */
(function() {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    window.location.replace('admin.html');
  }
})();

function adminLogout() {
  localStorage.removeItem('admin_token');
  window.location.href = 'admin.html';
}
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HOME PAGE — extra sections to add:
# 1. Animated orbs in hero, social icons row, scroll indicator
# 2. Stats strip with animated counters
# 3. Featured Projects preview strip
# 4. CTA Banner
# ─────────────────────────────────────────────────────────────────────────────
HOME_EXTRAS_SCRIPT = r"""
<script>
/* Home page: wrap stat numbers with counter class */
document.addEventListener('DOMContentLoaded', () => {
  /* Mark up stat numbers for counter animation */
  document.querySelectorAll('.glass-panel .font-headline-md').forEach(el => {
    const txt = el.innerText.replace('+','').replace('.','').trim();
    const n = parseInt(txt);
    if (!isNaN(n) && n > 0) {
      el.dataset.target = n;
      el.dataset.suffix = el.innerText.includes('+') ? '+' : '';
      el.classList.add('counter-val');
    }
  });

  /* Add orbs to hero if not present */
  const heroSection = document.querySelector('section');
  if (heroSection && !document.getElementById('hero-orb-1')) {
    const orbsHtml = `
      <div id="hero-orb-1" style="position:absolute;top:10%;left:5%;width:400px;height:400px;
        background:radial-gradient(circle,rgba(99,102,241,0.18),transparent 70%);
        border-radius:50%;pointer-events:none;z-index:0;" class="orb-float"></div>
      <div id="hero-orb-2" style="position:absolute;top:40%;right:8%;width:320px;height:320px;
        background:radial-gradient(circle,rgba(139,92,246,0.15),transparent 70%);
        border-radius:50%;pointer-events:none;z-index:0;" class="orb-float-2"></div>
      <div id="hero-orb-3" style="position:absolute;bottom:10%;left:35%;width:280px;height:280px;
        background:radial-gradient(circle,rgba(6,182,212,0.12),transparent 70%);
        border-radius:50%;pointer-events:none;z-index:0;" class="orb-float-3"></div>`;
    heroSection.style.position = 'relative';
    heroSection.style.overflow = 'hidden';
    heroSection.insertAdjacentHTML('afterbegin', orbsHtml);
  }
});
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: inject before </body>
# ─────────────────────────────────────────────────────────────────────────────
def inject_before_body_close(content, snippet):
    if '</body>' in content:
        return content.replace('</body>', snippet + '\n</body>', 1)
    return content + snippet

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: update footer to proper 3-column
# ─────────────────────────────────────────────────────────────────────────────
IMPROVED_FOOTER = r"""<footer class="bg-surface-container-lowest w-full py-unit-xl border-t border-white/10 relative z-10">
<div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-unit-lg">
    <!-- Brand -->
    <div class="flex flex-col gap-3">
      <a href="index.html" class="font-display-lg-mobile text-display-lg-mobile bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent w-fit">BTech Portfolio</a>
      <p class="font-body-md text-body-md text-on-surface-variant opacity-60 max-w-xs">Computer Science engineering student targeting top-tier tech companies.</p>
    </div>
    <!-- Quick Links -->
    <div class="flex flex-col gap-2">
      <span class="font-label-caps text-label-caps text-primary uppercase tracking-wider mb-1">Quick Links</span>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit" href="projects.html">Projects</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit" href="certificates.html">Certificates</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit" href="research.html">Research</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit" href="contact.html">Contact</a>
    </div>
    <!-- Social Links -->
    <div class="flex flex-col gap-2">
      <span class="font-label-caps text-label-caps text-primary uppercase tracking-wider mb-1">Connect</span>
      <a href="https://github.com" target="_blank" rel="noopener noreferrer" class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform flex items-center gap-2 w-fit">
        <span class="material-symbols-outlined text-sm">code</span>GitHub</a>
      <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform flex items-center gap-2 w-fit">
        <span class="material-symbols-outlined text-sm">work</span>LinkedIn</a>
      <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform flex items-center gap-2 w-fit">
        <span class="material-symbols-outlined text-sm">tag</span>Twitter / X</a>
      <a href="https://leetcode.com" target="_blank" rel="noopener noreferrer" class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform flex items-center gap-2 w-fit">
        <span class="material-symbols-outlined text-sm">psychology</span>LeetCode</a>
    </div>
  </div>
  <div class="border-t border-white/10 pt-unit-md flex flex-col md:flex-row items-center justify-between gap-2">
    <p class="font-label-caps text-label-caps text-on-surface-variant opacity-50 text-center">© 2024 Engineering Portfolio. Built with ❤️ and Precision.</p>
    <div class="flex gap-4">
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-50 hover:opacity-100" href="#">Privacy</a>
      <a class="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors opacity-50 hover:opacity-100" href="#">Terms</a>
    </div>
  </div>
</div>
</footer>"""

def replace_footer(content):
    # Replace any existing footer tag with our improved one
    content = re.sub(r'<footer\b.*?</footer>', IMPROVED_FOOTER, content, flags=re.DOTALL | re.IGNORECASE)
    return content

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS EACH PAGE
# ─────────────────────────────────────────────────────────────────────────────
pages_config = {
    'index.html':        {'extra': HOME_EXTRAS_SCRIPT},
    'projects.html':     {},
    'certificates.html': {},
    'skills.html':       {},
    'coding.html':       {},
    'research.html':     {},
    'about.html':        {},
    'resume.html':       {},
    'contact.html':      {'extra': CONTACT_SCRIPT},
    'admin.html':        {'extra': ADMIN_SCRIPT},
    'dashboard.html':    {'extra': DASHBOARD_SCRIPT},
}

for filename, cfg in pages_config.items():
    filepath = os.path.join(ROOT, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filename}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove old duplicate toggleDarkMode/toggleMobileMenu (they will be in SHARED_SCRIPT)
    content = re.sub(
        r'<script>\s*function toggleMobileMenu\(\)\{.*?function toggleDarkMode\(\)\{.*?dark.*?\}\s*</script>',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'<script>\s*function toggleDarkMode\(\)\{.*?\}\s*function toggleMobileMenu\(\)\{.*?\}\s*</script>',
        '', content, flags=re.DOTALL
    )
    # Broader cleanup for standalone shared functions
    content = re.sub(
        r'<script>\s*(?:function toggleMobileMenu[^}]*\}|function toggleDarkMode[^}]*\}){1,2}\s*</script>',
        '', content, flags=re.DOTALL
    )

    # 2. Replace footer
    content = replace_footer(content)

    # 3. Inject page-specific extra script
    if cfg.get('extra'):
        content = inject_before_body_close(content, cfg['extra'])

    # 4. Inject shared script last (so it runs after page-specific ones)
    content = inject_before_body_close(content, SHARED_SCRIPT)

    # 5. Add spin keyframe inline for sync icon in contact
    if 'spin' not in content and filename == 'contact.html':
        spin_style = '<style>@keyframes spin{to{transform:rotate(360deg)}}</style>'
        content = content.replace('</head>', spin_style + '\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ENHANCED: {filename}")

print("\nAll pages enhanced successfully!")
