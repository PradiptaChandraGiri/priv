import os
import re
import urllib.request

root = r"c:\Users\girip\Desktop\Portfolio_pradipta"
pages = {
    "certificates.html": ("certificates_page_high_fidelity/code.html", "certificates"),
    "skills.html": ("skills_page_high_fidelity/code.html", "skills"),
    "coding.html": ("coding_page_high_fidelity/code.html", "coding"),
    "research.html": ("research_page_high_fidelity/code.html", "research"),
    "about.html": ("about_page_high_fidelity/code.html", "about"),
    "resume.html": ("resume_page_high_fidelity/code.html", "resume"),
    "contact.html": ("contact_page_high_fidelity/code.html", "contact"),
    "admin.html": ("admin_login_page/code.html", "admin"),
    "dashboard.html": ("admin_dashboard_refined/code.html", "dashboard")
}

nav_links = [
    ("Home", "index.html", "home"),
    ("Projects", "projects.html", "projects"),
    ("Certificates", "certificates.html", "certificates"),
    ("Skills", "skills.html", "skills"),
    ("Coding", "coding.html", "coding"),
    ("Research", "research.html", "research"),
    ("About", "about.html", "about"),
    ("Contact", "contact.html", "contact"),
]

mobile_menu_template = """
<!-- Mobile Menu Overlay -->
<div id="mobile-menu" class="fixed inset-0 z-[60] hidden">
<div class="absolute inset-0 bg-background/90 backdrop-blur-md" onclick="toggleMobileMenu()"></div>
<div class="absolute right-0 top-0 h-full w-72 bg-surface-container border-l border-outline-variant/30 flex flex-col p-6 pt-20" style="background:#1f1f27;">
<button onclick="toggleMobileMenu()" class="absolute top-4 right-4 text-on-surface-variant hover:text-primary"><span class="material-symbols-outlined">close</span></button>
{mobile_links}
<a class="text-on-surface-variant hover:text-primary transition-colors py-3 border-b border-outline-variant/20 font-label-caps text-label-caps" href="resume.html">Resume</a>
<a href="contact.html" class="mt-6 bg-primary text-on-primary px-4 py-3 rounded-lg font-label-caps text-label-caps text-center hover:bg-primary-fixed transition-all">Hire Me</a>
</div>
</div>
"""

shared_js = """
<script>
function toggleMobileMenu(){var m=document.getElementById('mobile-menu');if(m){m.classList.toggle('hidden');document.body.style.overflow=m.classList.contains('hidden')?'':'hidden';}}
function toggleDarkMode(){document.documentElement.classList.toggle('dark');}
</script>
"""

# Let's write the copy mechanism
for target_file, (src_file, active_key) in pages.items():
    src_path = os.path.join(root, src_file.replace("/", "\\"))
    target_path = os.path.join(root, target_file)
    
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Generate nav items
    desktop_nav = []
    mobile_nav = []
    
    for name, href, key in nav_links:
        if key == active_key:
            desktop_nav.append(f'<a class="text-primary font-bold border-b-2 border-primary pb-1 px-3 py-2 font-label-caps text-label-caps" href="{href}">{name}</a>')
            mobile_nav.append(f'<a class="text-primary font-bold py-3 border-b border-outline-variant/20 font-label-caps text-label-caps" href="{href}">{name}</a>')
        else:
            desktop_nav.append(f'<a class="text-on-surface-variant hover:text-primary transition-colors px-3 py-2 rounded-md font-label-caps text-label-caps" href="{href}">{name}</a>')
            mobile_nav.append(f'<a class="text-on-surface-variant hover:text-primary transition-colors py-3 border-b border-outline-variant/20 font-label-caps text-label-caps" href="{href}">{name}</a>')
            
    desktop_nav_html = "\\n".join(desktop_nav)
    mobile_nav_html = "\\n".join(mobile_nav)
    
    # 1. Desktop Nav Replacement
    # Find something like <nav class="hidden md:flex... or <div class="hidden md:flex...
    # that is inside the header.
    # We will match the tag containing `hidden md:flex` and its contents and replace it.
    # This regex looks for `<TAG class="...hidden md:flex..."> ... </TAG>`
    content = re.sub(
        r'(<(nav|div)\b[^>]*class="[^"]*hidden\s+md:flex[^>]*>).*?(</\2>)', 
        rf'\1\n{desktop_nav_html}\n\3', 
        content, 
        flags=re.DOTALL | re.IGNORECASE,
        count=1  # Only replace the first one (the main nav)
    )

    # Make brand logo point to index.html (replace <div class="font-display-lg... BTech Portfolio... </div> with <a>)
    content = re.sub(
        r'<div([^>]*class="[^"]*font-display-lg-mobile[^>]*>[^<]*BTech Portfolio\s*)</div>',
        r'<a href="index.html"\1</a>',
        content,
        flags=re.IGNORECASE
    )

    # 2. Add Mobile Menu Hamburger Button
    # Find the closing tag of the <header> or the end of the top bar and insert it right before.
    # It's usually inside <div class="flex items-center... or right before </header>
    if "toggleMobileMenu" not in content:
        # Just put it right before </header>
        content = re.sub(
            r'(</header>)',
            r'<button onclick="toggleMobileMenu()" class="md:hidden p-2 text-on-surface z-50 relative"><span class="material-symbols-outlined">menu</span></button>\n\1',
            content,
            flags=re.IGNORECASE
        )

    # 3. Add Mobile Menu Container
    # Insert right before <main> or right after <header>
    mobile_menu_full = mobile_menu_template.replace("{mobile_links}", mobile_nav_html)
    
    # Let's insert before <main>
    if "<main" in content:
        content = re.sub(
            r'(<main\b)',
            f'{mobile_menu_full}\n\\1',
            content,
            flags=re.IGNORECASE
        )
    else:
        # If no main, insert after </header>
        content = re.sub(
            r'(</header>)',
            f'\\1\n{mobile_menu_full}\n',
            content,
            flags=re.IGNORECASE
        )

    # 4. Shared JS
    content = re.sub(
        r'(</body>)',
        f'{shared_js}\n\\1',
        content,
        flags=re.IGNORECASE
    )

    # Ensure admin links are correct
    content = content.replace('admin-login.html', 'admin.html')
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed {target_file}")
    
print("All done!")
