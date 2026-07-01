import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'
EMAIL = 'admin@portfolio.local'
PASSWORD = 'Admin@1234'

print("\n2. Logging in to get token...")
login_res = requests.post(f"{BASE_URL}/auth/login", json={
    "email": EMAIL,
    "password": PASSWORD
})
print("Login Response:", login_res.status_code)
if login_res.status_code != 200:
    print("Login failed, aborting.")
    exit(1)

token = login_res.json().get('token')
headers = {'Authorization': f'Bearer {token}'}

print("\n3. Updating Profile...")
profile_res = requests.put(f"{BASE_URL}/profile", headers=headers, json={
  "name": "Pradipta Chandra Giri",
  "title": "BTech CSE Student | Full Stack Developer",
  "bio": "I'm a passionate CS undergrad from Bhubaneswar, Odisha...",
  "university": "ITER, SOA University",
  "degree": "B.Tech in Computer Science & Engineering",
  "graduation_year": 2026,
  "cgpa": "8.5",
  "github_url": "https://github.com/PradiptaChandraGiri",
  "linkedin_url": "https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/",
  "leetcode_username": "Pradipta_Chandra_Giri",
  "available_for": "SDE Internships, Research Roles, Open Source Contributions",
  "tagline": "Building scalable solutions, one commit at a time"
})
print("Profile Response:", profile_res.status_code)

print("\n4. Adding CampusBazaar Project...")
project_res = requests.post(f"{BASE_URL}/projects", headers=headers, json={
  "title": "CampusBazaar",
  "short_description": "Campus marketplace for Indian university students",
  "full_description": "Full-stack platform enabling students to buy and sell items with real-time chat, AI descriptions, and fraud detection.",
  "category": "Web Dev",
  "tech_stack": ["Next.js 14", "TypeScript", "PostgreSQL", "Prisma", "Cloudinary", "NextAuth", "Socket.io", "Redis"],
  "github_url": "https://github.com/PradiptaChandraGiri/campusbazaar",
  "live_url": "https://campusbazaar.vercel.app",
  "featured": True,
  "status": "completed",
  "role": "Full Stack Developer",
  "team_size": 2,
  "highlights": [
    "Real-time chat with Socket.io and Redis",
    "AI-powered description generation with Claude API",
    "Cloudinary integration for image uploads",
    "Fixed dual-auth conflict between NextAuth and custom JWT",
    "University-specific filtering and verified seller system"
  ]
})
print("Project Response:", project_res.status_code)

print("\n5. Adding Certificate...")
cert_res = requests.post(f"{BASE_URL}/certificates", headers=headers, json={
  "title": "Full Stack Web Development",
  "issuing_org": "Coursera",
  "issue_date": "2024-01-15",
  "category": "Web Dev",
  "skills_gained": ["React", "Node.js", "Express"],
  "featured": True
})
print("Certificate Response:", cert_res.status_code)

print("\n6. Adding Skills...")
skills = [
    { "name": "React.js", "category": "Frontend", "proficiency": 88, "display_order": 1 },
    { "name": "Next.js", "category": "Frontend", "proficiency": 85, "display_order": 2 },
    { "name": "Node.js", "category": "Backend", "proficiency": 82, "display_order": 3 },
    { "name": "PostgreSQL", "category": "Database", "proficiency": 80, "display_order": 4 },
    { "name": "Python", "category": "Languages", "proficiency": 85, "display_order": 5 },
    { "name": "C++", "category": "Languages", "proficiency": 80, "display_order": 6 },
    { "name": "TypeScript", "category": "Languages", "proficiency": 82, "display_order": 7 },
    { "name": "Docker", "category": "DevOps", "proficiency": 70, "display_order": 8 },
    { "name": "Git", "category": "Tools", "proficiency": 90, "display_order": 9 },
    { "name": "Tailwind CSS", "category": "Frontend", "proficiency": 92, "display_order": 10 }
]

for skill in skills:
    s_res = requests.post(f"{BASE_URL}/skills", headers=headers, json=skill)
    print(f"Skill {skill['name']} Response: {s_res.status_code}")

print("\nAll database seeding complete! You can now log into your admin dashboard.")
