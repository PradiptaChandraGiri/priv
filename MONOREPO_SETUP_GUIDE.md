# Monorepo Setup and Deployment Guide

This guide provides instructions for configuring, running, and deploying your portfolio monorepo.

## Project Structure
```text
stitch_stitch_student_portfolio_hub/
├── portfolio-backend/          # Node.js + Express + PG Database
└── portfolio-react/            # Vite + React Client
```

---

## 1. Local Development Setup

### Terminal 1: Backend
```bash
cd portfolio-backend
npm install
# Configure your .env file with DATABASE_URL and Cloudinary keys
node server.js
```

### Terminal 2: Frontend
```bash
cd portfolio-react
npm install
npm run dev
```
Navigate to `http://localhost:5173`.

---

## 2. Deploying to Production

### Deploying the Backend on Render
1. Create a **Web Service** on Render.
2. Connect your GitHub repository.
3. Set the **Root Directory** to `portfolio-backend`.
4. Set the build command to `npm install` and start command to `node server.js`.
5. Add the necessary Environment Variables:
   - `DATABASE_URL`
   - `JWT_SECRET`
   - `ADMIN_PASSWORD`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

### Deploying the Frontend on Vercel
1. Create a project on Vercel.
2. Select your repository.
3. Set the **Root Directory** to `portfolio-react`.
4. Set the **Framework Preset** to `Vite`.
5. Add Environment Variables:
   - `VITE_API_URL` (your Render backend API URL ending in `/api`)
   - `VITE_LEETCODE_USERNAME` (`Pradipta_Chadnra_Giri`)
