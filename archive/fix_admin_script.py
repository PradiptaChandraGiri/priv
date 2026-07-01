import re

with open('C:/Users/girip/Desktop/Portfolio_pradipta/admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

SCRIPT = """
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

# add the script right before <!-- ============================================================
#     SHARED.JS
html = html.replace('<!-- ============================================================', SCRIPT + '\n<!-- ============================================================')

with open('C:/Users/girip/Desktop/Portfolio_pradipta/admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
