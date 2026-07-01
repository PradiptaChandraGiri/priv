import os
import re
import glob

# Mapping of HTML file to React component name and output file
MAPPING = {
    'index.html': ('HomePage', 'HomePage.jsx'),
    'about.html': ('AboutPage', 'AboutPage.jsx'),
    'projects.html': ('ProjectsPage', 'ProjectsPage.jsx'),
    'certificates.html': ('CertificatesPage', 'CertificatesPage.jsx'),
    'skills.html': ('SkillsPage', 'SkillsPage.jsx'),
    'research.html': ('ResearchPage', 'ResearchPage.jsx'),
    'contact.html': ('ContactPage', 'ContactPage.jsx'),
    'resume.html': ('ResumePage', 'ResumePage.jsx'),
    'coding.html': ('CodingPage', 'CodingPage.jsx'),
    'admin.html': ('AdminLoginPage', 'AdminLoginPage.jsx'),
    'dashboard.html': ('AdminDashboardPage', 'AdminDashboardPage.jsx'),
}

SRC_DIR = r'C:\Users\girip\Desktop\stitch_stitch_student_portfolio_hub'
DEST_DIR = r'c:\Users\girip\Desktop\Portfolio_pradipta\portfolio-react\src\pages'

def html_to_jsx(html):
    # Basic class -> className conversion
    jsx = re.sub(r'\bclass=', 'className=', html)
    # onclick -> onClick
    jsx = re.sub(r'\bonclick=', 'onClick=', jsx)
    jsx = re.sub(r'\bonsubmit=', 'onSubmit=', jsx)
    # self-closing tags
    for tag in ['img', 'hr', 'br', 'input']:
        # This is a naive regex for self closing, might need careful handling
        jsx = re.sub(r'(<' + tag + r'[^>]*?)(?<!/)>', r'\1 />', jsx, flags=re.IGNORECASE)
    # style="var:..." -> style={{var: "..."}}
    def style_repl(match):
        style_str = match.group(1)
        rules = style_str.split(';')
        obj_props = []
        for rule in rules:
            if ':' not in rule: continue
            k, v = rule.split(':', 1)
            k = k.strip()
            v = v.strip().replace('"', "'")
            # camelCase the key
            k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
            obj_props.append(f'{k}: "{v}"')
        return f"style={{{{{', '.join(obj_props)}}}}}"
    
    jsx = re.sub(r'\bstyle="(.*?)"', style_repl, jsx)
    
    # HTML comments -> JSX comments
    jsx = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', jsx, flags=re.DOTALL)
    
    # SVG fill-rule, clip-rule, stroke-width, stroke-linecap, stroke-linejoin
    jsx = jsx.replace('fill-rule', 'fillRule')
    jsx = jsx.replace('clip-rule', 'clipRule')
    jsx = jsx.replace('stroke-width', 'strokeWidth')
    jsx = jsx.replace('stroke-linecap', 'strokeLinecap')
    jsx = jsx.replace('stroke-linejoin', 'strokeLinejoin')
    jsx = jsx.replace('stroke-dasharray', 'strokeDasharray')
    jsx = jsx.replace('stroke-dashoffset', 'strokeDashoffset')
    jsx = jsx.replace('viewbox', 'viewBox')
    jsx = jsx.replace('xmlns:xlink', 'xmlnsXlink')
    jsx = jsx.replace('tabindex', 'tabIndex')
    
    return jsx

for html_file, (comp_name, jsx_file) in MAPPING.items():
    html_path = os.path.join(SRC_DIR, html_file)
    if not os.path.exists(html_path):
        print(f"Skipping {html_file}, not found.")
        continue
        
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract <main> if it exists
    main_match = re.search(r'(<main[^>]*>.*?</main>)', content, flags=re.IGNORECASE | re.DOTALL)
    
    if main_match and html_file not in ['dashboard.html', 'admin.html']:
        jsx_content = html_to_jsx(main_match.group(1))
    else:
        # Fallback to body content if no main or if it's admin/dashboard
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, flags=re.IGNORECASE | re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
            # Remove scripts and nav/mobile-menu to avoid duplicating layout if it's a normal page
            body_content = re.sub(r'<script.*?>.*?</script>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
            
            # For non-admin/dashboard pages without main, we might need to strip topnav and mobile menu
            if html_file not in ['dashboard.html', 'admin.html']:
                body_content = re.sub(r'<nav.*?</nav>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
                # Instead of matching </div> recursively, just split at <!-- Hero Section --> or similar if present
                # or just remove the known mobile menu structure non-greedily
                body_content = re.sub(r'<div id="mobile-menu".*?<!--', '<!--', body_content, flags=re.IGNORECASE | re.DOTALL)
                
            jsx_content = html_to_jsx(body_content)
        else:
            print(f"Skipping {html_file}, no main or body found.")
            continue
            
    old_jsx_path = os.path.join(DEST_DIR, jsx_file)
    imports = ""
    if os.path.exists(old_jsx_path):
        with open(old_jsx_path, 'r', encoding='utf-8') as old_f:
            old_content = old_f.read()
            import_match = re.search(r'^(import.*?)(?:\n\n|\nexport)', old_content, flags=re.DOTALL | re.MULTILINE)
            if import_match:
                imports = import_match.group(1)
    
    if not imports:
        imports = "import { Link } from 'react-router-dom';\nimport { motion } from 'framer-motion';"
        
    wrapper_start = "<>"
    wrapper_end = "</>"
    if html_file in ['dashboard.html', 'admin.html']:
        wrapper_start = "<div className=\"min-h-screen bg-background text-on-surface flex flex-col\">"
        wrapper_end = "</div>"
        
    final_file_content = f"{imports}\n\nexport default function {comp_name}() {{\n  return (\n    {wrapper_start}\n      {jsx_content}\n    {wrapper_end}\n  );\n}}\n"
    
    with open(old_jsx_path, 'w', encoding='utf-8') as f:
        f.write(final_file_content)
    print(f"Converted {html_file} to {jsx_file}")

print("Done converting HTML to JSX.")
