const { Pool, neonConfig } = require('@neondatabase/serverless');
const ws = require('ws');
require('dotenv').config();

neonConfig.webSocketConstructor = ws;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

async function main() {
  const client = await pool.connect();
  try {
    console.log("Starting full database seeding...");

    // 1. Clear existing data to avoid duplicates
    await client.query("DELETE FROM projects");
    await client.query("DELETE FROM certificates");
    await client.query("DELETE FROM skills");
    await client.query("DELETE FROM experience");
    console.log("🧹 Cleared old projects, certificates, skills, and experience.");

    // 2. Insert Projects
    const projects = [
      {
        title: "CampusBazaar",
        description: "Student-exclusive marketplace for VSSUT campus — buy & sell books, electronics, and essentials with 0% commission and direct WhatsApp contact.",
        category: "Web Dev",
        tech_stack: ["React", "Firebase", "JavaScript", "Vercel"],
        github_url: "https://github.com/PradiptaChandraGiri/campusbazaar",
        live_url: "https://vssut-campusbazar.vercel.app",
        featured: true,
        sort_order: 1
      },
      {
        title: "DRRMS — Disaster Relief System",
        description: "Centralized disaster relief management platform to track victims, volunteers, donations, and resource distribution. Built as a Database Engineering project.",
        category: "Full Stack",
        tech_stack: ["React", "Node.js", "MySQL", "Express.js"],
        github_url: "https://github.com/PradiptaChandraGiri/DRRMS-Database-Project",
        live_url: "",
        featured: false,
        sort_order: 2
      },
      {
        title: "SkySenseAI",
        description: "AI-powered environmental prediction platform using machine learning models and Flask backend with an interactive web dashboard for intelligent forecasting.",
        category: "AI / ML",
        tech_stack: ["Python", "Flask", "Scikit-learn", "JavaScript"],
        github_url: "https://github.com/PradiptaChandraGiri",
        live_url: "",
        featured: true,
        sort_order: 3
      },
      {
        title: "DailyAssist AI",
        description: "Desktop productivity assistant built with Python and Tkinter. Manages daily tasks, reminders, smart notifications, and AI-assisted productivity tracking.",
        category: "Python / AI",
        tech_stack: ["Python", "Tkinter", "Plyer", "JSON"],
        github_url: "https://github.com/PradiptaChandraGiri",
        live_url: "",
        featured: false,
        sort_order: 4
      },
      {
        title: "DCSM — Digital Complaint System",
        description: "Digital complaint management system for streamlined grievance submission, tracking, and resolution with role-based access control.",
        category: "Full Stack",
        tech_stack: ["React", "Node.js", "MySQL"],
        github_url: "https://github.com/PradiptaChandraGiri/DCSM-Digital-Complaint-Managment-System",
        live_url: "",
        featured: false,
        sort_order: 5
      },
      {
        title: "GenAI Toolbox",
        description: "A collection of Generative AI tools and utilities built for practical use cases including text generation, summarization, and AI-powered automation.",
        category: "GenAI",
        tech_stack: ["Python", "GenAI", "Flask"],
        github_url: "https://github.com/PradiptaChandraGiri/genai-toolbox",
        live_url: "",
        featured: false,
        sort_order: 6
      }
    ];

    for (const p of projects) {
      await client.query(
        `INSERT INTO projects (title, description, category, tech_stack, github_url, live_url, featured, sort_order)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
        [p.title, p.description, p.category, p.tech_stack, p.github_url, p.live_url, p.featured, p.sort_order]
      );
    }
    console.log("✅ Seeded 6 Projects successfully.");

    // 3. Insert Certificates
    const certs = [
      {
        title: "AI Tutorial for Beginners",
        issuer: "IBM SkillsBuild & Simplilearn",
        category: "Artificial Intelligence",
        issue_date: "2026-05-12",
        credential_url: "URL-FWOZMMIUQHG",
        skills: ["AI Fundamentals", "Machine Learning", "Real-world AI"],
        sort_order: 1
      },
      {
        title: "GSSoC 2026 Participant",
        issuer: "GirlScript Summer of Code",
        category: "Open Source",
        issue_date: "2026-08-01",
        credential_url: "",
        skills: ["Open Source", "Collaboration"],
        sort_order: 2
      },
      {
        title: "Gemini Student Ambassador",
        issuer: "Google Developer Programs",
        category: "AI Advocacy",
        issue_date: "2026-01-01",
        credential_url: "",
        skills: ["AI Advocacy", "Community", "Workshops"],
        sort_order: 3
      }
    ];

    for (const c of certs) {
      await client.query(
        `INSERT INTO certificates (title, issuer, category, issue_date, credential_url, skills, sort_order)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [c.title, c.issuer, c.category, c.issue_date, c.credential_url, c.skills, c.sort_order]
      );
    }
    console.log("✅ Seeded 3 Certificates successfully.");

    // 4. Insert Skills
    const skills = [
      { name: "Python", category: "Languages", proficiency: 90, sort_order: 1 },
      { name: "C++", category: "Languages", proficiency: 82, sort_order: 2 },
      { name: "JavaScript", category: "Languages", proficiency: 80, sort_order: 3 },
      { name: "C", category: "Languages", proficiency: 75, sort_order: 4 },
      { name: "Java", category: "Languages", proficiency: 75, sort_order: 5 },
      { name: "SQL", category: "Languages", proficiency: 75, sort_order: 6 },
      { name: "React.js", category: "Frontend", proficiency: 82, sort_order: 7 },
      { name: "HTML5 / CSS3", category: "Frontend", proficiency: 90, sort_order: 8 },
      { name: "Tailwind CSS", category: "Frontend", proficiency: 85, sort_order: 9 },
      { name: "Node.js / Express", category: "Backend", proficiency: 78, sort_order: 10 },
      { name: "Flask", category: "Backend", proficiency: 82, sort_order: 11 },
      { name: "MySQL", category: "Databases", proficiency: 80, sort_order: 12 },
      { name: "Firebase", category: "Databases", proficiency: 80, sort_order: 13 }
    ];

    for (const s of skills) {
      await client.query(
        `INSERT INTO skills (name, category, proficiency, sort_order)
         VALUES ($1, $2, $3, $4)`,
        [s.name, s.category, s.proficiency, s.sort_order]
      );
    }
    console.log("✅ Seeded 13 Skills successfully.");

    // 5. Insert Experience
    const experiences = [
      {
        company: "Google Developer Programs",
        role: "Google Gemini Student Ambassador",
        start_date: "2026-01-01",
        end_date: "2026-12-31",
        is_current: false,
        description: "Organized AI-focused workshops and promoted Google AI tools among VSSUT students.\nConducted technical demonstrations and presentations on Gemini and Google developer tools.\nEngaged and grew the campus developer community through awareness sessions.",
        tech_used: ["Gemini", "Google Cloud", "AI Integration"],
        sort_order: 1
      },
      {
        company: "Automated Quality Inspection Using Computer Vision",
        role: "Hackathon Team Member",
        start_date: "2025-01-01",
        end_date: "2025-01-02",
        is_current: false,
        description: "Designed an AI-powered inspection workflow using computer vision for quality control.\nCollaborated on ML model selection, implementation, and final presentation.",
        tech_used: ["Computer Vision", "Python", "Machine Learning"],
        sort_order: 2
      }
    ];

    for (const exp of experiences) {
      await client.query(
        `INSERT INTO experience (company, role, start_date, end_date, is_current, description, tech_used, sort_order)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
        [exp.company, exp.role, exp.start_date, exp.end_date, exp.is_current, exp.description, exp.tech_used, exp.sort_order]
      );
    }
    console.log("✅ Seeded 2 Experiences successfully.");

    // 6. Update Owner Details
    await client.query(`
      UPDATE owner 
      SET name = $1, title = $2, university = $3, bio = $4, email = $5, github_url = $6, linkedin_url = $7, twitter_url = $8, leetcode_username = $9, location = $10, cgpa = $11, available_for = $12, degree = $13, graduation_year = $14
      WHERE id = (SELECT id FROM owner LIMIT 1)
    `, [
      "Pradipta Chandra Giri",
      "AI & Full-Stack Developer",
      "Veer Surendra Sai University of Technology (VSSUT), Burla",
      "Hi, I'm Pradipta Chandra Giri, a B.Tech CSE undergraduate at VSSUT Burla with a CGPA of 9.31. I build AI-powered applications, full-stack web platforms, and automation tools that solve real-world problems.",
      "giripradiptachandra@gmail.com",
      "https://github.com/PradiptaChandraGiri",
      "https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/",
      "https://x.com/Pradiptachandr5",
      "Pradipta_Chandra_Giri",
      "Bhubaneswar, Odisha, India",
      "9.31",
      ["SDE Internships", "AI/ML Research", "Open Source", "Full-Stack Projects"],
      "B.Tech in Computer Science & Engineering",
      2027
    ]);
    console.log("✅ Updated Owner table record.");

  } catch (err) {
    console.error("❌ Seeding failed:", err);
  } finally {
    client.release();
    pool.end();
  }
}

main();
