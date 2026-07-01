import os

API_BASE = "http://localhost:5000/api" # Use localhost for local dev initially

index_script = f"""
<script>
/* ── HOME — load profile data from backend ── */
const _API = '{API_BASE}';
async function _loadHomeProfile() {{
  try {{
    const r = await fetch(_API + '/profile');
    const d = await r.json();
    if (!d.success || !d.data) return;
    const p = d.data;
    /* Name */
    const nameEls = document.querySelectorAll('h1 .text-primary, [data-profile-name]');
    nameEls.forEach(el => {{ if (p.name) el.textContent = p.name.split(' ').pop(); }});
    /* Photo */
    const photo = document.querySelector('img[alt="Profile Picture"]');
    if (photo && p.profile_image_url) photo.src = p.profile_image_url;
    /* GitHub / LinkedIn / LeetCode social links */
    const gh = document.querySelector('#footer-github, a[title="GitHub"]');
    if (gh && p.github_url) gh.href = p.github_url;
    const li = document.querySelector('#footer-linkedin, a[title="LinkedIn"]');
    if (li && p.linkedin_url) li.href = p.linkedin_url;
    const lc = document.querySelector('#footer-leetcode, a[title="LeetCode"]');
    if (lc && p.leetcode_username) lc.href = 'https://leetcode.com/' + p.leetcode_username;
    /* CGPA stat */
    const cgpaEl = document.querySelector('[data-cgpa]');
    if (cgpaEl && p.cgpa) cgpaEl.textContent = p.cgpa;
  }} catch(e) {{ console.warn('Profile load failed', e); }}
}}
_loadHomeProfile();
</script>
"""

projects_script = f"""
<script>
/* ── PROJECTS — load from backend ── */
const _API = '{API_BASE}';
async function _loadProjects(category) {{
  const grid = document.getElementById('projects-grid');
  if (!grid) return;
  grid.innerHTML = '<div class="col-span-full flex justify-center py-16"><div class="skeleton w-8 h-8 rounded-full"></div></div>';
  try {{
    const url = _API + '/projects' + (category && category !== 'all' ? '?category=' + encodeURIComponent(category) : '');
    const r = await fetch(url);
    const d = await r.json();
    if (!d.success || !d.data.length) {{
      grid.innerHTML = '<div class="col-span-full text-center py-16 text-on-surface-variant"><p class="text-4xl mb-4">🚀</p><p>No projects yet. Add some from the admin dashboard.</p></div>';
      return;
    }}
    grid.innerHTML = d.data.map(p => `
      <div class="group relative bg-surface-container/30 backdrop-blur-xl rounded-xl border border-white/10
                  overflow-hidden transition-all duration-300 hover:-translate-y-2
                  hover:shadow-[0_10px_40px_rgba(0,0,0,0.5)] flex flex-col cursor-pointer"
           data-category="${{p.category?.toLowerCase().replace(/[^a-z]/g,'-')}}"
           data-title="${{p.title}}"
           data-description="${{(p.description||'').replace(/"/g,'&quot;')}}"
           data-tech="${{(p.tech_stack||[]).join(',')}}"
           data-github="${{p.github_url||''}}"
           data-live="${{p.live_url||''}}"
           onclick="openProjectModal(this)">
        <div class="h-48 w-full overflow-hidden relative">
          <img src="${{p.thumbnail_url || 'https://placehold.co/400x200/1f1f27/c0c1ff?text=' + encodeURIComponent(p.title)}}"
               alt="${{p.title}}" class="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"/>
          <div class="absolute inset-0 bg-gradient-to-t from-surface-container/90 via-transparent to-transparent"></div>
          <div class="absolute top-4 right-4 bg-background/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10">
            <span class="font-label-caps text-label-caps text-primary uppercase">${{p.category}}</span>
          </div>
        </div>
        <div class="p-unit-md flex-grow flex flex-col">
          <h3 class="font-headline-md text-headline-md text-on-surface mb-2">${{p.title}}</h3>
          <p class="text-on-surface-variant text-sm line-clamp-3 mb-4">${{p.description||''}}</p>
          <div class="mt-auto flex flex-wrap gap-2 mb-3">
            ${{(p.tech_stack||[]).slice(0,3).map(t =>
              `<span class="px-2 py-1 bg-primary/10 text-primary border border-primary/20 rounded-full font-code-block text-[10px] uppercase">${{t}}</span>`
            ).join('')}}
          </div>
          <div class="flex items-center justify-between border-t border-white/10 pt-3">
            ${{p.github_url ? `<a class="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-1 font-label-caps text-label-caps" href="${{p.github_url}}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()"><span class="material-symbols-outlined" style="font-size:18px">code</span>Repo</a>` : '<span></span>'}}
            <span class="text-primary opacity-0 group-hover:opacity-100 transition-opacity material-symbols-outlined">arrow_forward</span>
          </div>
        </div>
      </div>
    `).join('');
  }} catch(e) {{ console.warn('Projects load failed', e); }}
}}
window._loadProjects = _loadProjects;
document.addEventListener('DOMContentLoaded', () => _loadProjects('all'));
</script>
"""

certificates_script = f"""
<script>
/* ── CERTIFICATES — load from backend ── */
const _API = '{API_BASE}';
async function _loadCerts(category) {{
  const grid = document.querySelector('.grid.grid-cols-1.md\\\\:grid-cols-2.lg\\\\:grid-cols-3');
  if (!grid) return;
  grid.innerHTML = '<div class="col-span-full flex justify-center py-12"><div class="skeleton w-8 h-8 rounded-full"></div></div>';
  try {{
    const url = _API + '/certificates' + (category && category !== 'all' ? '?category=' + encodeURIComponent(category) : '');
    const r = await fetch(url);
    const d = await r.json();
    if (!d.success || !d.data.length) {{
      grid.innerHTML = '<div class="col-span-full text-center py-12 text-on-surface-variant"><p class="text-4xl mb-4">🏆</p><p>No certificates yet. Add from the admin dashboard.</p></div>';
      return;
    }}
    grid.innerHTML = d.data.map(c => `
      <article class="glass-panel rounded-xl p-unit-md flex flex-col glow-hover transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden group border border-outline-variant/30 hover:border-primary/50 bg-surface-container-low/50">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary opacity-80"></div>
        <div class="flex items-start justify-between mb-unit-md relative z-10">
          <div class="w-12 h-12 rounded bg-surface-container flex items-center justify-center p-2 border border-outline-variant/20 shadow-inner overflow-hidden">
            ${{c.image_url
              ? `<img src="${{c.image_url}}" alt="${{c.issuer}}" class="w-full h-full object-contain"/>`
              : `<span class="material-symbols-outlined text-primary">workspace_premium</span>`}}
          </div>
          <span class="font-label-caps text-label-caps text-tertiary uppercase flex items-center gap-1">
            <span class="w-2 h-2 rounded-full bg-tertiary shadow-[0_0_8px_rgba(255,183,131,0.8)]"></span>
            ${{c.issue_date ? new Date(c.issue_date).getFullYear() : 'Valid'}}
          </span>
        </div>
        <h3 class="font-headline-md text-headline-md mb-unit-xs relative z-10">${{c.title}}</h3>
        <p class="font-body-md text-body-md text-on-surface-variant mb-unit-md flex-grow relative z-10">${{c.issuer}}</p>
        <div class="flex flex-wrap gap-unit-xs mb-unit-lg relative z-10">
          ${{(c.skills||[]).slice(0,3).map(s =>
            `<span class="chip px-2 py-1 rounded text-primary font-code-block text-code-block border border-primary/20 bg-primary/5">${{s}}</span>`
          ).join('')}}
        </div>
        <div class="flex gap-unit-sm mt-auto pt-unit-md border-t border-outline-variant/20 relative z-10">
          ${{c.pdf_url || c.image_url
            ? `<button class="flex-1 bg-primary text-on-primary py-2 rounded font-label-caps text-label-caps uppercase hover:bg-primary-container transition-colors" onclick="window.open('${{c.pdf_url || c.image_url}}','_blank')">View</button>`
            : ''}}
          ${{c.credential_url
            ? `<a class="px-3 py-2 rounded border border-outline-variant/50 text-on-surface hover:text-primary hover:border-primary transition-colors flex items-center justify-center glass-panel" href="${{c.credential_url}}" target="_blank" rel="noopener noreferrer"><span class="material-symbols-outlined text-[18px]">verified</span></a>`
            : ''}}
        </div>
      </article>
    `).join('');
  }} catch(e) {{ console.warn('Certs load failed', e); }}
}}
document.addEventListener('DOMContentLoaded', () => _loadCerts('all'));
</script>
"""

research_script = f"""
<script>
/* ── RESEARCH — load from backend ── */
const _API = '{API_BASE}';
async function _loadResearch() {{
  const list = document.querySelector('.flex.flex-col.gap-unit-lg, main .flex.flex-col');
  if (!list) return;
  try {{
    const r = await fetch(_API + '/research');
    const d = await r.json();
    if (!d.success || !d.data.length) return; /* Keep static demo cards */
    const STATUS_COLOR = {{ Published:'text-primary bg-primary/10 border-primary/20', 'Under Review':'text-tertiary bg-tertiary/10 border-tertiary/20', Preprint:'text-secondary bg-secondary/10 border-secondary/20' }};
    const accentColor  = {{ Published:'from-primary to-primary/40', 'Under Review':'from-tertiary to-tertiary/40', Preprint:'from-secondary to-secondary/40' }};
    list.innerHTML = d.data.map(p => `
      <article class="glass-panel rounded-xl relative overflow-hidden flex flex-col md:flex-row gap-unit-md p-unit-lg group transition-all duration-300 hover:-translate-y-1 border border-white/10">
        <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-gradient-to-b ${{accentColor[p.status]||accentColor.Published}}"></div>
        <div class="flex-grow flex flex-col relative z-10">
          <div class="flex flex-wrap items-center gap-unit-sm mb-unit-sm">
            <span class="font-code-block text-[10px] px-3 py-1 rounded-full border ${{STATUS_COLOR[p.status]||STATUS_COLOR.Published}} uppercase tracking-widest">${{p.status}}</span>
            <span class="text-on-surface-variant font-code-block text-xs opacity-60">${{p.year||''}}</span>
            ${{p.citation_count ? `<span class="ml-auto font-code-block text-[10px] text-primary/60">${{p.citation_count}} Citations</span>` : ''}}
          </div>
          <h2 class="font-headline-md text-headline-md text-on-surface mb-2">${{p.title}}</h2>
          <p class="font-body-md text-on-surface-variant mb-1">${{(p.authors||[]).join(', ')}}</p>
          ${{p.journal ? `<p class="font-body-md text-tertiary italic mb-unit-md">${{p.journal}}</p>` : ''}}
          ${{p.abstract ? `<details class="mb-unit-md"><summary class="font-label-caps text-label-caps text-on-surface-variant cursor-pointer hover:text-primary transition-colors uppercase tracking-widest">Abstract</summary><p class="mt-2 font-body-md text-on-surface-variant bg-surface-container-low/50 p-unit-md rounded-lg border border-outline-variant/20">${{p.abstract}}</p></details>` : ''}}
          <div class="flex flex-wrap items-center gap-unit-sm border-t border-outline-variant/10 pt-unit-md">
            ${{p.pdf_url ? `<button class="bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 font-label-caps text-[10px] uppercase tracking-widest px-5 py-2 rounded-lg flex items-center gap-2 transition-all" onclick="window.open('${{p.pdf_url}}','_blank')"><span class="material-symbols-outlined text-[16px]">menu_book</span>Read Paper</button>` : ''}}
            ${{p.doi ? `<a class="text-on-surface-variant hover:text-on-surface border border-outline-variant/20 font-label-caps text-[10px] uppercase px-4 py-2 rounded-lg flex items-center gap-2" href="https://doi.org/${{p.doi}}" target="_blank"><span class="material-symbols-outlined text-[16px]">link</span>DOI</a>` : ''}}
            ${{p.arxiv_url ? `<a class="text-on-surface-variant hover:text-on-surface border border-outline-variant/20 font-label-caps text-[10px] uppercase px-4 py-2 rounded-lg flex items-center gap-2" href="${{p.arxiv_url}}" target="_blank"><span class="material-symbols-outlined text-[16px]">open_in_new</span>arXiv</a>` : ''}}
          </div>
        </div>
      </article>
    `).join('');
  }} catch(e) {{ console.warn('Research load failed', e); }}
}}
document.addEventListener('DOMContentLoaded', _loadResearch);
</script>
"""

skills_script = f"""
<script>
/* ── SKILLS — load from backend ── */
const _API = '{API_BASE}';
async function _loadSkills() {{
  try {{
    const r = await fetch(_API + '/skills');
    const d = await r.json();
    if (!d.success || !d.data.length) return; /* Keep static cards */
    /* Group by category */
    const grouped = {{}};
    d.data.forEach(s => {{ if (!grouped[s.category]) grouped[s.category]=[]; grouped[s.category].push(s); }});
    /* Find the bento grid (3 skill category sections) and replace if dynamic data available */
    const grid = document.querySelector('.grid.grid-cols-1.lg\\\\:grid-cols-2.xl\\\\:grid-cols-3');
    if (!grid) return;
    grid.innerHTML = Object.entries(grouped).map(([cat, skills]) => `
      <section class="glass-panel rounded-xl p-unit-lg flex flex-col gap-unit-md glow-hover transition-all duration-300">
        <div class="flex items-center gap-unit-sm mb-unit-sm">
          <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary">
            <span class="material-symbols-outlined" style="font-size:28px">code</span>
          </div>
          <h2 class="font-headline-md text-headline-md text-inverse-surface">${{cat}}</h2>
        </div>
        <div class="flex flex-col gap-unit-md">
          ${{skills.slice(0,4).map(s => `
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="font-code-block text-code-block text-cyan-400 bg-cyan-400/10 px-3 py-1 rounded-md border border-cyan-400/20">${{s.name}}</span>
                <span class="font-code-block text-code-block text-on-surface-variant">${{s.proficiency}}%</span>
              </div>
              <div class="w-full h-2 bg-surface-highest/50 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-primary to-cyan-400 rounded-full" data-width="${{s.proficiency}}%" style="width:${{s.proficiency}}%"></div>
              </div>
            </div>
          `).join('')}}
        </div>
      </section>
    `).join('');
  }} catch(e) {{ console.warn('Skills load failed', e); }}
}}
document.addEventListener('DOMContentLoaded', _loadSkills);
</script>
"""

# Apply the scripts
import os

def inject(filename, script):
    path = os.path.join('C:/Users/girip/Desktop/Portfolio_pradipta', filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # insert before shared script or before </body>
    if '<!-- ============================================================\n     SHARED.JS' in html:
        html = html.replace('<!-- ============================================================\n     SHARED.JS', script + '\n<!-- ============================================================\n     SHARED.JS')
    else:
        html = html.replace('</body>', script + '\n</body>')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Injected into {filename}")

inject('index.html', index_script)
inject('projects.html', projects_script)
inject('certificates.html', certificates_script)
inject('research.html', research_script)
inject('skills.html', skills_script)

