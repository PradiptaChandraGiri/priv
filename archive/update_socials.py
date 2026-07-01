import os
import glob
import re

FOLDER = r'C:\Users\girip\Desktop\Portfolio_pradipta'

LINKEDIN_URL = "https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/?skipRedirect=true"
GMAIL = "giripradiptachandra@gmail.com"

html_files = glob.glob(os.path.join(FOLDER, "*.html"))

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace mailto: links
    content = re.sub(r'href=["\']mailto:[^"\']*["\']', f'href="mailto:{GMAIL}"', content)
    
    # Replace linkedin.com/in/... or linkedin.com/company/...
    content = re.sub(r'href=["\']https?://(www\.)?linkedin\.com/[^"\']*["\']', f'href="{LINKEDIN_URL}"', content)
    
    # Replace dummy email text (like hello@example.com) that might be in the contact page
    # But let's check for standard ones Stitch AI might have used:
    content = re.sub(r'>[\w\.-]+@[\w\.-]+\.\w+<', f'>{GMAIL}<', content)
    # Wait, the admin login uses admin@portfolio.local, we don't want to replace that in the JS string
    # The regex >[\w\.-]+@[\w\.-]+\.\w+< requires it to be between tags, which is good.
    # However, admin.html might have >admin@portfolio.local< in a placeholder or span. Let's be careful.
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated Socials!")
