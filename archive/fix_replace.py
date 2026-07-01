import os

with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "const LEETCODE_USERNAME = 'Pradipta_Chadnra_Giri'; if (isNaN(target)) return;",
    "const suffix = el.dataset.suffix || '';\n      if (isNaN(target)) return;"
)

text = text.replace(
    "const LEETCODE_USERNAME = 'YOUR_LEETCODE_USERNAME';",
    "const LEETCODE_USERNAME = 'Pradipta_Chadnra_Giri';"
)

with open('C:/Users/girip/Desktop/Portfolio_pradipta/coding.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed mistake and updated username")
