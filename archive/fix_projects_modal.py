import re

with open('C:/Users/girip/Desktop/Portfolio_pradipta/projects.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The script to inject
SCRIPT = """
<script>
function openProjectModal(card) {
  const title    = card.dataset.title    || 'Project Details';
  const desc     = card.dataset.description || '';
  const tech     = (card.dataset.tech || '').split(',').filter(Boolean);
  const github   = card.dataset.github  || '#';
  const live     = card.dataset.live    || '';
  const team     = card.dataset.team    || '';
  const catLabel = card.dataset.categoryLabel || card.dataset.category || '';
  const img      = card.querySelector('img')?.src || '';

  /* Inject into modal */
  const modal = document.getElementById('project-modal');
  const panel = document.getElementById('modal-panel');
  if (!modal || !panel) return;

  /* Update image */
  const modalImg = panel.querySelector('img');
  if (modalImg && img) modalImg.src = img;

  /* Update title */
  const modalTitle = panel.querySelector('h2');
  if (modalTitle) modalTitle.textContent = title;

  /* Update category badge */
  const badges = panel.querySelectorAll('[class*="rounded-full"]');
  if (badges[0]) badges[0].textContent = catLabel;
  if (badges[1] && team) badges[1].innerHTML =
    `<span class="material-symbols-outlined" style="font-size:14px">group</span> Team: ${team}`;

  /* Update description */
  const descEl = panel.querySelector('.prose p');
  if (descEl) descEl.textContent = desc;

  /* Update tech tags in modal (if you have a tech list area) */
  const techList = panel.querySelector('[data-modal-tech]');
  if (techList) {
    techList.innerHTML = tech.map(t =>
      `<span class="px-2 py-1 bg-primary/10 text-primary border border-primary/20 rounded-full font-code-block text-[10px] uppercase">${t}</span>`
    ).join('');
  }

  /* Update GitHub link */
  const ghLink = panel.querySelector('a[href="#"]');
  if (ghLink && github !== '#') ghLink.href = github;

  /* Update live demo link */
  const liveLink = panel.querySelectorAll('a[href="#"]')[1];
  if (liveLink && live) { liveLink.href = live; liveLink.style.display = ''; }
  else if (liveLink)    { liveLink.style.display = 'none'; }

  /* Show modal */
  modal.classList.remove('opacity-0', 'pointer-events-none');
  panel.classList.remove('scale-95');
  panel.classList.add('scale-100');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const modal = document.getElementById('project-modal');
  const panel = document.getElementById('modal-panel');
  if (!modal || !panel) return;
  modal.classList.add('opacity-0', 'pointer-events-none');
  panel.classList.remove('scale-100');
  panel.classList.add('scale-95');
  document.body.style.overflow = '';
}

function filterProjects(category) {
  const cards   = document.querySelectorAll('#projects-grid > div[data-category]');
  const buttons = document.querySelectorAll('[onclick^="filterProjects"]');

  buttons.forEach(btn => {
    btn.classList.remove('bg-primary/20', 'text-primary', 'border-primary/30',
      'shadow-[0_0_15px_rgba(192,193,255,0.15)]');
    btn.classList.add('bg-white/5', 'text-on-surface-variant', 'border-white/10');
  });
  event.currentTarget.classList.add('bg-primary/20', 'text-primary', 'border-primary/30',
    'shadow-[0_0_15px_rgba(192,193,255,0.15)]');
  event.currentTarget.classList.remove('bg-white/5', 'text-on-surface-variant', 'border-white/10');

  cards.forEach(card => {
    card.style.display = (category === 'all' || card.dataset.category === category) ? '' : 'none';
  });
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
</script>
"""

# Replace any existing openProjectModal script
html = re.sub(r'<script>\s*function openProjectModal.*?</script>', SCRIPT, html, flags=re.DOTALL)

with open('C:/Users/girip/Desktop/Portfolio_pradipta/projects.html', 'w', encoding='utf-8') as f:
    f.write(html)
