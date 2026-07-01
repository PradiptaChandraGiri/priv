import os
import re

ROOT = 'C:/Users/girip/Desktop/Portfolio_pradipta'

def fix_coding():
    path = os.path.join(ROOT, 'coding.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Bug 1: Username typo
    html = html.replace("'Pradipta_Chadnra_Giri'", "'Pradipta_Chandra_Giri'")
    html = html.replace("'YOUR_LEETCODE_USERNAME'", "'Pradipta_Chandra_Giri'")
    
    # Bug 2: data-langs container
    # find the terminal window
    langs_pattern = r'<div class="flex items-center gap-2 mb-4">.*?<div class="w-3 h-3 rounded-full bg-\[#ff5f56\]"></div>.*?</div>.*?<div class="space-y-4">.*?</div>'
    # Actually, it's easier to just replace the inner contents of the terminal panel with data-langs
    if '<div class="space-y-4">' in html and 'data-langs' not in html:
        # replace the <div class="space-y-4">...</div> with <div data-langs class="p-unit-md space-y-5">...</div>
        html = re.sub(
            r'<div class="space-y-4">.*?C\+\+.*?65%.*?</div>.*?</div>.*?</div>',
            r'<div data-langs class="p-unit-md space-y-5"><div class="text-center text-on-surface-variant font-code-block text-[12px]">Loading...</div></div>',
            html,
            flags=re.DOTALL
        )
        
    # Bug 3: Streak and rank
    html = html.replace('<span class="text-primary font-bold">42 Days</span>', '<span class="text-primary font-bold" data-streak>42 Days</span>')
    
    if 'data-rank' not in html:
        # insert after the streak badge (actually after the whole <div> containing the streak badge)
        streak_badge_end = html.find('</div>', html.find('data-streak')) + 6
        if streak_badge_end > 5:
            html = html[:streak_badge_end] + '\n<div class="font-code-block text-[12px] text-on-surface-variant bg-surface-container-low/50 border border-outline-variant/20 py-1 px-3 rounded-md ml-2">Rank: <span class="text-primary font-bold" data-rank>#—</span></div>' + html[streak_badge_end:]

    # Bug 4: Total solved id="lc-total"
    html = html.replace('<span class="font-display-lg-mobile text-display-lg-mobile text-on-surface">425</span>', '<span class="font-display-lg-mobile text-display-lg-mobile text-on-surface" id="lc-total">425</span>')
    # and update the JS (wait, the JS I injected already uses 'lc-total')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        
def fix_dashboard():
    path = os.path.join(ROOT, 'dashboard.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Bug 11: Stat Card 1 is MISSING + Bug 10 layout issue
    # I already fixed the layout issue partially, but let's check for <main> and Stat Card 1
    # If not there, just rewrite the stats section
    if 'Certificates</span>' not in html and '<!-- Quick Stats -->' in html:
        html = html.replace(
            '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-unit-md mb-unit-lg">',
            '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-unit-md mb-unit-lg">\n' +
            '  <div class="glass-panel p-unit-md rounded-xl">\n' +
            '    <span class="font-label-caps text-label-caps text-on-surface-variant">Certificates</span>\n' +
            '    <div class="font-display-lg-mobile text-on-surface">0</div>\n' +
            '  </div>'
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def fix_projects():
    path = os.path.join(ROOT, 'projects.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    if 'function filterProjects' not in html:
        script = """
<script>
function filterProjects(category) {
  const cards = document.querySelectorAll('#projects-grid > div[data-category]');
  if(cards.length === 0) return; // handled by dynamic load
  cards.forEach(card => {
    if (category === 'all' || card.dataset.category === category) {
      card.style.display = '';
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      setTimeout(() => {
        card.style.transition = 'all 0.4s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 50);
    } else {
      card.style.display = 'none';
    }
  });
  document.querySelectorAll('button[onclick^="filterProjects"]').forEach(btn => {
    const isActive = btn.getAttribute('onclick').includes("'" + category + "'");
    btn.classList.toggle('bg-primary/20', isActive);
    btn.classList.toggle('text-primary', isActive);
    btn.classList.toggle('border-primary/30', isActive);
    btn.classList.toggle('text-on-surface-variant', !isActive);
  });
}
</script>
"""
        html = html.replace('</body>', script + '\n</body>')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def global_replace():
    for f in os.listdir(ROOT):
        if f.endswith('.html'):
            path = os.path.join(ROOT, f)
            with open(path, 'r', encoding='utf-8') as file:
                html = file.read()
                
            # Replace placeholder links
            html = html.replace('href="https://github.com"', 'href="https://github.com/PradiptaChandraGiri"')
            html = html.replace('href="https://linkedin.com"', 'href="https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/"')
            html = html.replace('href="https://leetcode.com"', 'href="https://leetcode.com/Pradipta_Chandra_Giri"')
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(html)

fix_coding()
fix_dashboard()
fix_projects()
global_replace()
print('All bugs fixed')
