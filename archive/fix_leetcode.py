import re
with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace View LeetCode Profile href="#"
html = re.sub(
    r'href="#"(\s*>\s*<span>View LeetCode Profile)',
    r'href="https://leetcode.com/Pradipta_Chadnra_Giri" target="_blank" rel="noopener noreferrer"\1',
    html
)

with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'w', encoding='utf-8') as f:
    f.write(html)
