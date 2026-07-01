# Pradipta Chandra Giri — Full-Stack Developer & AI Enthusiast Portfolio

Welcome to the official repository for my professional portfolio. This monorepo contains a modern, high-fidelity web application displaying my technical projects, research papers, certifications, competitive coding achievements, and professional experiences.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, TanStack Query v5, Tailwind CSS, Framer Motion, Lucide Icons |
| **Backend** | Node.js, Express.js, JWT, Axios, Multer, Helmet |
| **Database** | Neon PostgreSQL (Free Tier) |
| **Storage** | Cloudinary (Files, Certs, Resume, Images) |

---

## 📂 Project Structure

```text
stitch_stitch_student_portfolio_hub/
├── portfolio-backend/          # Node.js Express REST API & Database Models
├── portfolio-react/            # Vite + React Frontend Application
├── archive/                    # Archived legacy scripts & static pages
└── MONOREPO_SETUP_GUIDE.md    # Local setup and deployment instructions
```

---

## 🚀 Quick Start (Local Development)

### 1. Backend Setup
```bash
cd portfolio-backend
npm install
# Rename .env.example to .env and configure DATABASE_URL, JWT_SECRET, and Cloudinary keys
npm run dev
```

### 2. Frontend Setup
```bash
cd portfolio-react
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🌐 Deployment

This project is configured to run inside a unified repository and deploy cleanly:
* **Backend API** is deployed to **Render** (using the `portfolio-backend` subdirectory root).
* **Frontend** is deployed to **Vercel** (using the `portfolio-react` subdirectory root).

For detailed deployment instructions, please check the [MONOREPO_SETUP_GUIDE.md](file:///C:/Users/girip/Desktop/stitch_stitch_student_portfolio_hub/MONOREPO_SETUP_GUIDE.md).

---

## 👨‍💻 Owner Details

**Pradipta Chandra Giri**
* B.Tech Computer Science & Engineering, VSSUT Burla
* CGPA: 9.31
* GitHub: [@PradiptaChandraGiri](https://github.com/PradiptaChandraGiri)
* LinkedIn: [pradipta-chandra-giri-035b88340](https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/)
* LeetCode: [@Pradipta_Chadnra_Giri](https://leetcode.com/Pradipta_Chadnra_Giri)
