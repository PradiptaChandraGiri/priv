import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'
EMAIL = 'admin@portfolio.local'
PASSWORD = 'Admin@1234'

print("\n1. Logging in to get token...")
login_res = requests.post(f"{BASE_URL}/auth/login", json={
    "email": EMAIL,
    "password": PASSWORD
})
print("Login Response:", login_res.status_code)
if login_res.status_code != 200:
    print("Login failed, aborting.")
    exit(1)

token = login_res.json().get('token')
headers = {'Authorization': f'Bearer ' + token}

print("\n2. Updating Profile...")
profile_res = requests.put(f"{BASE_URL}/profile", headers=headers, json={
  "name": "Pradipta Chandra Giri",
  "title": "AI & Machine Learning Enthusiast | Full-Stack Developer",
  "bio": "Hi, I'm Pradipta Chandra Giri, a Computer Science and Engineering undergraduate at VSSUT Burla with a passion for Artificial Intelligence, Full-Stack Development, and Software Engineering. I enjoy building practical applications that solve real-world problems while continuously learning new technologies and contributing to innovative projects.",
  "university": "Veer Surendra Sai University of Technology (VSSUT), Burla",
  "degree": "Bachelor of Technology (B.Tech) - Computer Science & Engineering",
  "graduation_year": 2027,
  "cgpa": "9.31",
  "github_url": "https://github.com/PradiptaChandraGiri",
  "linkedin_url": "https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/",
  "leetcode_username": "Pradipta_Chadnra_Giri",
  "available_for": ["SDE Internships", "Research Roles", "Open Source", "Freelance"],
  "tagline": "Building scalable solutions, one commit at a time"
})
print("Profile Response:", profile_res.status_code)

print("\n3. Adding Projects...")
projects = [
    {
      "title": "DailyAssist AI",
      "short_description": "A desktop productivity assistant built using Python",
      "full_description": "A desktop productivity assistant built using Python that helps users manage daily tasks, reminders, smart notifications, and AI-assisted productivity through a user-friendly interface.",
      "category": "AI/ML",
      "tech_stack": ["Python", "Tkinter", "Plyer", "JSON", "Git", "GitHub"],
      "github_url": "https://github.com/PradiptaChandraGiri",
      "live_url": "",
      "featured": True,
      "status": "completed",
      "role": "Developer",
      "team_size": 1,
      "highlights": ["Smart notifications", "Task management", "User-friendly interface"]
    },
    {
      "title": "SkySenseAI",
      "short_description": "An AI-powered environmental prediction platform",
      "full_description": "An AI-powered environmental prediction platform that leverages machine learning models and Flask to generate intelligent predictions through an interactive dashboard.",
      "category": "AI/ML",
      "tech_stack": ["Python", "Flask", "Machine Learning", "HTML", "CSS", "JavaScript", "Scikit-learn"],
      "github_url": "https://github.com/PradiptaChandraGiri",
      "live_url": "",
      "featured": True,
      "status": "completed",
      "role": "Developer",
      "team_size": 1,
      "highlights": ["Machine Learning predictions", "Interactive dashboard", "Flask backend"]
    },
    {
      "title": "CampusBazaar",
      "short_description": "A student-exclusive marketplace",
      "full_description": "A student-exclusive marketplace that enables students to buy and sell books, electronics, hostel essentials, bicycles, and other campus items without any commission.",
      "category": "Web Dev",
      "tech_stack": ["React", "JavaScript", "Firebase", "HTML", "CSS", "Vercel"],
      "github_url": "https://github.com/PradiptaChandraGiri",
      "live_url": "",
      "featured": True,
      "status": "completed",
      "role": "Full Stack Developer",
      "team_size": 1,
      "highlights": ["Zero commission marketplace", "Firebase integration", "Real-time updates"]
    },
    {
      "title": "Disaster Relief Resource Management System (DRRMS)",
      "short_description": "A centralized disaster management platform",
      "full_description": "A centralized disaster management platform designed to efficiently manage disaster information, volunteers, victims, donations, inventory, and relief distribution using modern database technologies.",
      "category": "Web Dev",
      "tech_stack": ["React", "Node.js", "Express.js", "MySQL", "Vite"],
      "github_url": "https://github.com/PradiptaChandraGiri/theresoursemanagement",
      "live_url": "",
      "featured": True,
      "status": "completed",
      "role": "Full Stack Developer",
      "team_size": 1,
      "highlights": ["Centralized database", "Resource distribution tracking", "Volunteer management"]
    }
]
for p in projects:
    project_res = requests.post(f"{BASE_URL}/projects", headers=headers, json=p)
    print("Project", p['title'], "Response:", project_res.status_code)

print("\n4. Adding Certificates...")
certificates = [
    {
      "title": "Google Gemini Student Ambassador Program",
      "issuing_org": "Google",
      "issue_date": "2026-01-01",
      "category": "Leadership",
      "skills_gained": ["Leadership", "Community Building", "AI Workshops"],
      "featured": True
    },
    {
      "title": "GirlScript Summer of Code (GSSoC) Participant",
      "issuing_org": "GirlScript Foundation",
      "issue_date": "2026-05-01",
      "category": "Open Source",
      "skills_gained": ["Open Source", "Version Control", "Collaboration"],
      "featured": True
    }
]
for c in certificates:
    cert_res = requests.post(f"{BASE_URL}/certificates", headers=headers, json=c)
    print("Certificate", c['title'], "Response:", cert_res.status_code)

print("\n5. Adding Skills...")
skills = [
    { "name": "Python", "category": "Languages", "proficiency": 90, "display_order": 1 },
    { "name": "C++", "category": "Languages", "proficiency": 85, "display_order": 2 },
    { "name": "JavaScript", "category": "Languages", "proficiency": 85, "display_order": 3 },
    { "name": "SQL", "category": "Languages", "proficiency": 85, "display_order": 4 },
    { "name": "React.js", "category": "Frontend", "proficiency": 88, "display_order": 5 },
    { "name": "Tailwind CSS", "category": "Frontend", "proficiency": 85, "display_order": 6 },
    { "name": "Node.js", "category": "Backend", "proficiency": 80, "display_order": 7 },
    { "name": "Flask", "category": "Backend", "proficiency": 85, "display_order": 8 },
    { "name": "MySQL", "category": "Database", "proficiency": 85, "display_order": 9 },
    { "name": "Machine Learning", "category": "AI/ML", "proficiency": 80, "display_order": 10 },
    { "name": "Scikit-learn", "category": "AI/ML", "proficiency": 80, "display_order": 11 },
    { "name": "Pandas", "category": "AI/ML", "proficiency": 85, "display_order": 12 },
    { "name": "Git & GitHub", "category": "Tools", "proficiency": 90, "display_order": 13 }
]

for skill in skills:
    s_res = requests.post(f"{BASE_URL}/skills", headers=headers, json=skill)
    print("Skill", skill['name'], "Response:", s_res.status_code)

print("\nAll database seeding complete!")
