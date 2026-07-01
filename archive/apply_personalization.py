# -*- coding: utf-8 -*-
import os
import glob
import re

FOLDER = r'.'
html_files = glob.glob(os.path.join(FOLDER, '*.html'))

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Index page
    content = content.replace('Alex <span class="text-primary">Chen</span>', 'Pradipta <span class="text-primary">Giri</span>')
    content = content.replace('Full Stack Dev', 'AI & Machine Learning Enthusiast | Full-Stack Developer')
    content = content.replace(
        'Computer Science Engineering student specializing in scalable web architectures and machine learning integrations. Turning complex algorithms into elegant, user-centric solutions.',
        "Hi, I'm Pradipta Chandra Giri, a Computer Science and Engineering undergraduate at VSSUT Burla with a passion for Artificial Intelligence, Full-Stack Development, and Software Engineering. I enjoy building practical applications that solve real-world problems while continuously learning new technologies and contributing to innovative projects."
    )
    
    # About page long bio
    old_long_bio = 'I am a senior BTech student specializing in full-stack development and system architecture. My approach marries academic rigor with pragmatic engineering, focusing on scalable, high-performance applications built on robust foundations. I believe elegant code is an artifact of clear thinking.'
    new_long_bio = "Hello! I'm Pradipta Chandra Giri, a Computer Science and Engineering undergraduate at Veer Surendra Sai University of Technology (VSSUT), Burla.<br><br>My interests revolve around Artificial Intelligence, Machine Learning, Full-Stack Development, Software Engineering, Database Systems, and System Design. I enjoy transforming ideas into practical software solutions that improve productivity and solve real-world challenges.<br><br>Throughout my academic journey, I have worked on AI-powered applications, automation tools, database management systems, and modern web applications. Every project I build helps me strengthen my understanding of scalable software architecture, clean code practices, and user-centered design.<br><br>I actively participate in technical programs, hackathons, and developer communities to continuously improve my skills and collaborate with like-minded developers. My goal is to become a Software Engineer capable of building intelligent, scalable, and impactful software products."
    content = content.replace(old_long_bio, new_long_bio)
    
    # Education Details
    content = content.replace('ITER, SOA University', 'Veer Surendra Sai University of Technology (VSSUT), Burla')
    content = content.replace(
        'Focusing on Advanced Data Structures, Cloud Architecture, and Machine Learning. Consistently maintaining a position in the top 5% of the cohort.',
        'Focusing on Artificial Intelligence, Software Engineering, and Machine Learning.'
    )
    content = content.replace('CGPA: 8.5', 'CGPA: 9.31')
    content = content.replace("Dean's List", "2nd Year, 4th Sem")
    
    # Footer and random
    content = content.replace('Computer Science engineering student targeting top-tier tech companies.', 'AI & Machine Learning Enthusiast | Full-Stack Developer')
    content = re.sub(r'Ac 2024 Pradipta Chandra Giri', '&copy; 2026 Pradipta Chandra Giri', content)
    
    # Leetcode link fix (just in case)
    content = content.replace('https://leetcode.com/Pradipta_Chandra_Giri', 'https://leetcode.com/Pradipta_Chadnra_Giri')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in html_files:
    replace_in_file(filepath)

print("Personalization complete!")
