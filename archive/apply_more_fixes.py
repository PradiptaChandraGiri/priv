import os
import glob
import re

FOLDER = r'C:\Users\girip\Desktop\Portfolio_pradipta'

html_files = glob.glob(os.path.join(FOLDER, "*.html"))

PROJECTS_MODAL_SCRIPT = """
<script>
function openProjectModal(card) {
    const m = document.getElementById('modal-1');
    if (!m) return;
    
    const title = card.getAttribute('data-title') || 'Project Title';
    const desc = card.getAttribute('data-description') || '';
    const category = card.getAttribute('data-category-label') || '';
    const tech = card.getAttribute('data-tech') || '';
    const github = card.getAttribute('data-github') || '#';
    const live = card.getAttribute('data-live') || '#';

    const titleEl = m.querySelector('h3');
    if (titleEl) titleEl.textContent = title;

    const descEl = m.querySelector('p.text-on-surface-variant');
    if (descEl) descEl.textContent = desc;

    const catEl = m.querySelector('.text-primary.font-label-caps');
    if (catEl) catEl.textContent = category;

    // Build tech tags
    const techArea = m.querySelector('[data-modal-tech]') || m.querySelector('.flex.flex-wrap.gap-2.mt-4');
    if (techArea && tech) {
        techArea.innerHTML = tech.split(',').map(t => 
            `<span class="px-2 py-1 bg-surface-container text-on-surface border border-outline-variant/30 rounded-lg font-code-block text-[12px]">${t.trim()}</span>`
        ).join('');
        techArea.setAttribute('data-modal-tech', ''); // mark it
    }

    // Update buttons
    const links = m.querySelectorAll('a');
    links.forEach(a => {
        if (a.textContent.includes('GitHub')) a.href = github;
        if (a.textContent.includes('Live')) a.href = live;
    });

    m.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
</script>
"""

for file in html_files:
    basename = os.path.basename(file)
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Dark mode button: Add onclick="toggleDarkMode()" to the button with aria-label="Toggle dark mode" or "dark_mode"
    # Or to the button that has a span with data-darkmode-icon inside it.
    # We can match `<button ...>` that contains `<span ... data-darkmode-icon>`
    # But usually it's just `<button ... aria-label="Toggle dark mode"`
    # Let's replace: <button class="..." aria-label="Toggle dark mode"> -> add onclick
    content = re.sub(
        r'<button([^>]*aria-label=["\']Toggle dark mode["\'][^>]*)>',
        lambda m: m.group(0) if 'onclick' in m.group(1) else f'<button onclick="toggleDarkMode()"{m.group(1)}>',
        content
    )
    # Also catch other variations if they exist
    content = re.sub(
        r'<button([^>]*data-darkmode-icon[^>]*)>', # if the attribute is on the button
        lambda m: m.group(0) if 'onclick' in m.group(1) else f'<button onclick="toggleDarkMode()"{m.group(1)}>',
        content
    )
    
    # 2. CODING.HTML fixes
    if basename == 'coding.html':
        # Streak badge: "42 Days"
        content = re.sub(r'(<div[^>]*>)\s*42 Days\s*(</div>)', r'\1<span data-streak>42 Days</span>\2', content)
        # Rank badge: #23,492 or similar
        content = re.sub(r'(<div[^>]*>)\s*#\d+(,\d+)*\s*(</div>)', r'\1<span data-rank>#—</span>\2', content)
        # Solved counts: 250 / 800 etc
        content = re.sub(r'250 / 800', r'<span data-easy-solved>250 / 800</span>', content)
        content = re.sub(r'150 / 1700', r'<span data-med-solved>150 / 1700</span>', content)
        content = re.sub(r'25 / 700', r'<span data-hard-solved>25 / 700</span>', content)
        
        # Language bars container - find the div holding the C++, Python, Java stats.
        # It's usually a flex flex-col gap-5 holding them.
        content = re.sub(r'(<div class="flex flex-col gap-[345]"[^>]*>)\s*(?=<div[^>]*>\s*<div[^>]*>\s*<span[^>]*>C\+\+)', r'\1 data-langs ', content)

    # 3. PROJECTS.HTML fixes
    if basename == 'projects.html':
        # Replace onclick="openModal('modal-1')" with onclick="openProjectModal(this)" and add dummy data
        dummy_data = ' data-title="Project Title" data-description="Project description..." data-category-label="Systems" data-tech="React,Node,Tailwind" data-github="#" data-live="#" '
        content = re.sub(
            r'onclick=["\']openModal\([\'"]modal-1[\'"]\)["\']',
            f'onclick="openProjectModal(this)" {dummy_data}',
            content
        )
        # Inject the modal JS before </body>
        if 'openProjectModal' not in content:
            content = content.replace('</body>', PROJECTS_MODAL_SCRIPT + '\n</body>')

    # 4. RESUME.HTML fixes
    if basename == 'resume.html':
        # "Download PDF" button
        # Just give it a standard href for now
        content = re.sub(r'<button([^>]*>)\s*<span([^>]*>)\s*Download PDF\s*</span>', r'<a href="resume.pdf" download class="inline-flex..." \1<span\2Download PDF</span></a>', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Applied more fixes successfully!")
