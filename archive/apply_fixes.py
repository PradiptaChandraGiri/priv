"""
apply_fixes.py
==============
Run this script from inside your Portfolio_pradipta folder.
It makes all the personal info replacements + critical bug fixes
across ALL HTML files in one shot.

Usage:
  1. Open terminal / PowerShell
  2. cd C:\\Users\\girip\\Desktop\\Portfolio_pradipta
  3. python apply_fixes.py

What it does:
  - Replaces placeholder names with "Pradipta Chandra Giri"
  - Replaces placeholder emails with giripradiptachandra@gmail.com
  - Replaces generic github.com with your actual GitHub URL (set below)
  - Replaces linkedin.com with your actual LinkedIn
  - Adds onclick="toggleDarkMode()" to all dark mode toggle buttons
  - Adds onclick="toggleMobileMenu()" to mobile menu buttons that lack it
  - Adds filterProjects() function to projects.html
  - Sets backend URL constant in contact.html and admin.html
"""

import os
import re
import glob

# ======================================════════════════════════
# ← EDIT THESE BEFORE RUNNING
# ======================================════════════════════════
FOLDER          = r'C:\Users\girip\Desktop\Portfolio_pradipta'
GITHUB_USERNAME = 'PradiptaChandraGiri'          # your real GitHub username
LEETCODE_USER   = 'Pradipta_Chandra_Giri'        # your real LeetCode username
REAL_NAME       = 'Pradipta Chandra Giri'
EMAIL           = 'giripradiptachandra@gmail.com'
UNIVERSITY      = 'ITER, SOA University'           # e.g. "ITER, SOA University"
DEGREE          = 'B.Tech in Computer Science & Engineering'
GRAD_YEAR       = '2026'
CGPA            = '8.5'                            # your real CGPA
CITY            = 'Bhubaneswar, Odisha, India'
RAILWAY_URL     = 'http://localhost:5000/api'      # change to Railway URL after deploy
# ======================================════════════════════════

GITHUB_URL   = f'https://github.com/{GITHUB_USERNAME}'
LINKEDIN_URL = 'https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/'
LC_URL       = f'https://leetcode.com/{LEETCODE_USER}'

html_files = glob.glob(os.path.join(FOLDER, '*.html'))
print(f'Found {len(html_files)} HTML files in {FOLDER}\n')

stats = {'files_changed': 0, 'replacements': 0}

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # ── 1. PERSONAL INFO REPLACEMENTS ────────────────────────

    # Names
    for placeholder in ['Alex Chen', 'Alex Mercer', 'Root User', 'John Doe (Me)']:
        content = content.replace(placeholder, REAL_NAME)

    # Emails — but NOT admin@portfolio.local (that's the login form placeholder)
    content = re.sub(
        r'(?<!admin@portfolio\.)(?<!admin@system\.)[\w\.-]+@(?!portfolio\.local|system\.local)[\w\.-]+\.[a-z]{2,}',
        EMAIL,
        content
    )
    # Restore admin form placeholder if accidentally replaced
    content = content.replace(f'placeholder="{EMAIL}"', 'placeholder="your@email.com"')

    # Generic GitHub links → real GitHub
    content = re.sub(r'href=["\']https?://github\.com/?["\']', f'href="{GITHUB_URL}"', content)
    content = re.sub(r'href=["\']https?://github\.com(?!/YOUR)["\']', f'href="{GITHUB_URL}"', content)

    # Generic LinkedIn links → real LinkedIn
    content = re.sub(r'href=["\']https?://(www\.)?linkedin\.com(?!/in/pradipta)[^"\']*["\']', f'href="{LINKEDIN_URL}"', content)

    # Generic LeetCode links → real LeetCode
    content = re.sub(r'href=["\']https?://(www\.)?leetcode\.com/?["\']', f'href="{LC_URL}"', content)
    # But keep the graphql URL intact
    content = content.replace(f'href="{LC_URL}leetcode.com/graphql"', 'href="https://leetcode.com/graphql"')

    # Resume contact email text
    content = content.replace('alex.mercer@example.com', EMAIL)
    content = content.replace('hello@engineering.io', EMAIL)

    # Location
    for placeholder in ['San Francisco, CA', 'San Francisco, CA (Hybrid/Remote)', 'San Francisco']:
        content = content.replace(placeholder, CITY)

    # ── 2. FIX DARK MODE TOGGLE BUTTONS ──────────────────────
    # Find buttons with dark_mode icon but no onclick
    # Pattern: <button [no onclick] ...>..dark_mode...</button>
    def add_darkmode_onclick(m):
        tag = m.group(0)
        if 'onclick' in tag:
            return tag  # already has onclick
        if 'toggleDarkMode' in tag:
            return tag
        return tag.replace('<button ', '<button onclick="toggleDarkMode()" ', 1)

    # Match buttons that contain dark_mode icon
    content = re.sub(
        r'<button(?![^>]*onclick)[^>]*>(?:[^<]|<(?!/?button))*?dark_mode(?:[^<]|<(?!/?button))*?</button>',
        add_darkmode_onclick,
        content,
        flags=re.DOTALL
    )

    # ── 3. FIX MOBILE MENU BUTTONS ───────────────────────────
    # Buttons with menu icon but no onclick
    def add_menu_onclick(m):
        tag = m.group(0)
        if 'onclick' in tag or 'toggleMobileMenu' in tag:
            return tag
        return tag.replace('<button ', '<button onclick="toggleMobileMenu()" ', 1)

    content = re.sub(
        r'<button(?![^>]*onclick)[^>]*class=["\'][^"\']*md:hidden[^"\']*["\'][^>]*>(?:[^<]|<(?!/?button))*?menu(?:[^<]|<(?!/?button))*?</button>',
        add_menu_onclick,
        content,
        flags=re.DOTALL
    )

    # ── 4. FIX BACKEND URL ───────────────────────────────────
    if filename in ('contact.html', 'admin.html', 'dashboard.html'):
        # Already set in our fixed files. For original files:
        content = content.replace(
            "const BACKEND_URL = 'http://localhost:3001/api'",
            f"const BACKEND_URL = '{RAILWAY_URL}'"
        )

    # ── 5. FIX LEETCODE USERNAME TYPO ────────────────────────
    content = content.replace("'Pradipta_Chadnra_Giri'", f"'{LEETCODE_USER}'")
    content = content.replace('"Pradipta_Chadnra_Giri"', f'"{LEETCODE_USER}"')
    content = content.replace('YOUR_LEETCODE_USERNAME', LEETCODE_USER)
    content = content.replace('YOUR_GITHUB_USERNAME', GITHUB_USERNAME)

    # ── 6. FIX RESUME PAGE DETAILS ───────────────────────────
    if filename == 'resume.html':
        content = content.replace('Alex Mercer', REAL_NAME)
        content = content.replace('University of Technology', UNIVERSITY)
        content = content.replace('Software Systems Engineer', 'Full Stack Developer | BTech CSE')
        content = content.replace('github.com/alexmercer', f'github.com/{GITHUB_USERNAME}')
        content = content.replace('linkedin.com/in/alexmercer', 'linkedin.com/in/pradipta-chandra-giri-035b88340')

    # ── 7. FIX ABOUT PAGE ────────────────────────────────────
    if filename == 'about.html':
        content = content.replace('Institute of Technology &amp; Engineering', UNIVERSITY)
        content = content.replace('Institute of Technology & Engineering', UNIVERSITY)
        content = content.replace('2021 — 2025', f'{int(GRAD_YEAR)-4} — {GRAD_YEAR}')
        content = content.replace('CGPA: 3.8/4.0', f'CGPA: {CGPA}')
        content = content.replace('TechNova Solutions', 'Your Company Name')  # update with real internship

    # ── 8. ADD filterProjects() TO projects.html ─────────────
    if filename == 'projects.html' and 'function filterProjects' not in content:
        filter_script = """
<script>
/* ── FIX #12: filterProjects() — added by apply_fixes.py ── */
function filterProjects(category) {
  const cards = document.querySelectorAll('#projects-grid > div[data-category]');
  const noRes = document.getElementById('no-results');
  let visible = 0;
  cards.forEach(card => {
    const match = category === 'all' || card.dataset.category === category;
    if (match) {
      card.style.display = '';
      card.style.opacity = '0';
      card.style.transform = 'translateY(16px)';
      setTimeout(() => { card.style.transition = 'all 0.35s ease'; card.style.opacity = '1'; card.style.transform = 'translateY(0)'; }, 30);
      visible++;
    } else {
      card.style.opacity = '0';
      card.style.transform = 'scale(0.95)';
      setTimeout(() => { card.style.display = 'none'; }, 350);
    }
  });
  if (noRes) noRes.classList.toggle('hidden', visible > 0);
  document.querySelectorAll('button[onclick^="filterProjects"], .filter-btn').forEach(btn => {
    const isActive = btn.getAttribute('onclick')?.includes("'" + category + "'") || btn.dataset?.filter === category;
    btn.classList.toggle('bg-primary/20', isActive);
    btn.classList.toggle('text-primary', isActive);
    btn.classList.toggle('border-primary/30', isActive);
    btn.classList.toggle('bg-white/5', !isActive);
    btn.classList.toggle('text-on-surface-variant', !isActive);
    btn.classList.toggle('border-white/10', !isActive);
  });
}
</script>
"""
        content = content.replace('</body>', filter_script + '\n</body>')

    # ── 9. FIX FOOTER COPYRIGHT ──────────────────────────────
    content = content.replace(
        '© 2024 Engineering Portfolio. Built with ❤️ and Precision.',
        f'© 2024 {REAL_NAME}. Built with ❤️ and Precision.'
    )

    # ── COUNT CHANGES AND SAVE ────────────────────────────────
    if content != original:
        stats['files_changed'] += 1
        # Count approximate replacements
        diff_count = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
        stats['replacements'] += diff_count

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  OK Fixed: {filename} (~{diff_count} lines changed)')
    else:
        print(f'  - No changes: {filename}')

print(f'\n======================================')
print(f'  Done! {stats["files_changed"]} files updated.')
print(f'======================================')
print(f'\nNext steps:')
print(f'  1. Open index.html in browser — check your name appears')
print(f'  2. Open coding.html — check LeetCode username = {LEETCODE_USER}')
print(f'  3. Deploy backend to Railway, then re-run with RAILWAY_URL updated')
print(f'  4. Copy fixed files from portfolio-fixed/ folder for admin.html,')
print(f'     contact.html, coding.html, projects.html, dashboard.html')
