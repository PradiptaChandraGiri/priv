/**
 * BTech Portfolio — Complete Backend Server
 * Node.js + Express + Neon PostgreSQL + Cloudinary
 * Deploy to Railway: https://railway.app
 */

'use strict';
const express    = require('express');
const cors       = require('cors');
const helmet     = require('helmet');
const rateLimit  = require('express-rate-limit');
const multer     = require('multer');
const { Pool, neonConfig } = require('@neondatabase/serverless');
const ws         = require('ws');
neonConfig.webSocketConstructor = ws;
const bcrypt     = require('bcryptjs');
const jwt        = require('jsonwebtoken');
const cloudinary = require('cloudinary').v2;
const axios      = require('axios');
const nodemailer = require('nodemailer');
require('dotenv').config();

/* ─────────────────────────────────────────
   APP SETUP
───────────────────────────────────────── */
const app  = express();
const PORT = process.env.PORT || 5000;

app.use(helmet({ crossOriginResourcePolicy: false }));
app.use(cors({ origin: process.env.FRONTEND_URL || '*', credentials: true }));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

/* Rate limiting */
const apiLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 150 });
const contactLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 5,
  message: { success: false, message: 'Too many messages. Please wait an hour.' }
});
app.use('/api/', apiLimiter);

/* ─────────────────────────────────────────
   NEON POSTGRESQL CONNECTION
───────────────────────────────────────── */
const db = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

/* ─────────────────────────────────────────
   CLOUDINARY SETUP
───────────────────────────────────────── */
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key:    process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

/* Multer — memory storage (we stream to Cloudinary) */
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg','image/png','image/webp','image/gif','application/pdf'];
    cb(allowed.includes(file.mimetype) ? null : new Error('File type not allowed'), allowed.includes(file.mimetype));
  }
});

/* Upload helper */
async function uploadToCloudinary(buffer, folder, resourceType = 'auto') {
  return new Promise((resolve, reject) => {
    const stream = cloudinary.uploader.upload_stream(
      { folder: `portfolio/${folder}`, resource_type: resourceType },
      (err, result) => err ? reject(err) : resolve(result)
    );
    stream.end(buffer);
  });
}

/* ─────────────────────────────────────────
   AUTH MIDDLEWARE
───────────────────────────────────────── */
function auth(req, res, next) {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) return res.status(401).json({ success: false, message: 'Unauthorized' });
  try {
    req.admin = jwt.verify(header.slice(7), process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ success: false, message: 'Token invalid or expired' });
  }
}

/* ─────────────────────────────────────────
   DATABASE INIT
───────────────────────────────────────── */
async function initDB() {
  await db.query(`
    CREATE TABLE IF NOT EXISTS owner (
      id                SERIAL PRIMARY KEY,
      name              VARCHAR(200) NOT NULL DEFAULT 'Your Name',
      title             VARCHAR(300) DEFAULT 'BTech Computer Science Student',
      university        VARCHAR(300) DEFAULT '',
      bio               TEXT DEFAULT '',
      email             VARCHAR(200) DEFAULT '',
      phone             VARCHAR(50)  DEFAULT '',
      github_url        VARCHAR(500) DEFAULT '',
      linkedin_url      VARCHAR(500) DEFAULT '',
      twitter_url       VARCHAR(500) DEFAULT '',
      leetcode_username VARCHAR(100) DEFAULT '',
      location          VARCHAR(200) DEFAULT '',
      cgpa              VARCHAR(20)  DEFAULT '',
      available_for     TEXT[]       DEFAULT '{}',
      profile_image_url VARCHAR(1000) DEFAULT '',
      resume_url        VARCHAR(1000) DEFAULT '',
      password_hash     VARCHAR(255) NOT NULL,
      created_at        TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS projects (
      id            SERIAL PRIMARY KEY,
      title         VARCHAR(300) NOT NULL,
      description   TEXT,
      category      VARCHAR(100) DEFAULT 'Web Dev',
      tech_stack    TEXT[]  DEFAULT '{}',
      github_url    VARCHAR(500) DEFAULT '',
      live_url      VARCHAR(500) DEFAULT '',
      thumbnail_url VARCHAR(1000) DEFAULT '',
      featured      BOOLEAN DEFAULT FALSE,
      sort_order    INT     DEFAULT 0,
      created_at    TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS certificates (
      id               SERIAL PRIMARY KEY,
      title            VARCHAR(300) NOT NULL,
      issuer           VARCHAR(300) DEFAULT '',
      category         VARCHAR(100) DEFAULT 'Other',
      issue_date       DATE,
      expiry_date      DATE,
      credential_url   VARCHAR(500) DEFAULT '',
      image_url        VARCHAR(1000) DEFAULT '',
      pdf_url          VARCHAR(1000) DEFAULT '',
      skills           TEXT[]  DEFAULT '{}',
      sort_order       INT     DEFAULT 0,
      created_at       TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS research (
      id           SERIAL PRIMARY KEY,
      title        VARCHAR(500) NOT NULL,
      authors      TEXT[]  DEFAULT '{}',
      journal      VARCHAR(300) DEFAULT '',
      status       VARCHAR(50)  DEFAULT 'Published',
      year         INT,
      abstract     TEXT DEFAULT '',
      keywords     TEXT[]  DEFAULT '{}',
      doi          VARCHAR(300) DEFAULT '',
      arxiv_url    VARCHAR(500) DEFAULT '',
      pdf_url      VARCHAR(1000) DEFAULT '',
      citation_count INT DEFAULT 0,
      sort_order   INT  DEFAULT 0,
      created_at   TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS skills (
      id           SERIAL PRIMARY KEY,
      name         VARCHAR(200) NOT NULL,
      category     VARCHAR(100) DEFAULT 'Other',
      proficiency  INT          DEFAULT 80,
      icon         VARCHAR(100) DEFAULT '',
      sort_order   INT          DEFAULT 0,
      created_at   TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS experience (
      id           SERIAL PRIMARY KEY,
      company      VARCHAR(300) NOT NULL,
      role         VARCHAR(300) DEFAULT '',
      start_date   DATE,
      end_date     DATE,
      is_current   BOOLEAN DEFAULT FALSE,
      description  TEXT DEFAULT '',
      tech_used    TEXT[]  DEFAULT '{}',
      sort_order   INT     DEFAULT 0,
      created_at   TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS achievements (
      id           SERIAL PRIMARY KEY,
      title        VARCHAR(300) NOT NULL,
      description  TEXT DEFAULT '',
      date         DATE,
      sort_order   INT  DEFAULT 0,
      created_at   TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS messages (
      id         SERIAL PRIMARY KEY,
      name       VARCHAR(200) NOT NULL,
      email      VARCHAR(200) NOT NULL,
      subject    VARCHAR(300) DEFAULT '',
      body       TEXT NOT NULL,
      is_read    BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMPTZ DEFAULT NOW()
    );
  `);

  /* Seed default owner if none exists */
  const exists = await db.query('SELECT id FROM owner LIMIT 1');
  if (exists.rowCount === 0) {
    const hash = await bcrypt.hash(process.env.ADMIN_PASSWORD || 'Admin@1234', 12);
    await db.query(
      `INSERT INTO owner (name, email, password_hash) VALUES ($1, $2, $3)`,
      ['Portfolio Owner', process.env.ADMIN_EMAIL || 'admin@portfolio.local', hash]
    );
    console.log('✅ Default admin created. Change password via /api/auth/change-password');
  }

  console.log('✅ Database initialised');
}

/* ─────────────────────────────────────────
   ROUTES
───────────────────────────────────────── */

/* ── HEALTH ── */
app.get('/api/health', (_, res) => res.json({ status: 'ok', ts: new Date().toISOString() }));

/* ── AUTH ── */
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ success: false, message: 'Email and password required' });
    const row = await db.query('SELECT * FROM owner WHERE email = $1', [email.toLowerCase()]);
    if (!row.rowCount) return res.status(401).json({ success: false, message: 'Invalid credentials' });
    const owner = row.rows[0];
    const ok = await bcrypt.compare(password, owner.password_hash);
    if (!ok) return res.status(401).json({ success: false, message: 'Invalid credentials' });
    const token = jwt.sign({ id: owner.id, email: owner.email }, process.env.JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, token, name: owner.name });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/auth/google-login', async (req, res) => {
  try {
    const { idToken } = req.body;
    if (!idToken) return res.status(400).json({ success: false, message: 'Google ID Token required' });
    
    // Call Google Tokeninfo API
    const response = await axios.get(`https://oauth2.googleapis.com/tokeninfo?id_token=${idToken}`);
    const { email, email_verified, name } = response.data;
    
    if (!email_verified) return res.status(401).json({ success: false, message: 'Google account email not verified' });
    
    const allowedEmail = 'giripradiptachandra@gmail.com';
    if (email.toLowerCase() !== allowedEmail.toLowerCase()) {
      return res.status(403).json({ success: false, message: `Access denied. Only ${allowedEmail} is authorized.` });
    }
    
    // Find or create owner record
    const row = await db.query('SELECT * FROM owner WHERE LOWER(email) = $1 LIMIT 1', [email.toLowerCase()]);
    let owner;
    if (row.rowCount === 0) {
      const anyOwner = await db.query('SELECT * FROM owner LIMIT 1');
      if (anyOwner.rowCount > 0) {
        const updateRes = await db.query(
          `UPDATE owner SET email = $1, name = $2 WHERE id = $3 RETURNING *`,
          [email.toLowerCase(), name || anyOwner.rows[0].name, anyOwner.rows[0].id]
        );
        owner = updateRes.rows[0];
      } else {
        const mockHash = await bcrypt.hash(Math.random().toString(36), 12);
        const insertRes = await db.query(
          `INSERT INTO owner (name, email, password_hash) VALUES ($1, $2, $3) RETURNING *`,
          [name || 'Admin', email.toLowerCase(), mockHash]
        );
        owner = insertRes.rows[0];
      }
    } else {
      owner = row.rows[0];
    }
    
    const token = jwt.sign({ id: owner.id, email: owner.email }, process.env.JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, token, name: owner.name });
  } catch (e) {
    res.status(500).json({ success: false, message: e.response?.data?.error_description || e.message });
  }
});

app.post('/api/auth/change-password', auth, async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    const row = await db.query('SELECT password_hash FROM owner WHERE id = $1', [req.admin.id]);
    if (!row.rowCount) return res.status(404).json({ success: false });
    const ok = await bcrypt.compare(currentPassword, row.rows[0].password_hash);
    if (!ok) return res.status(401).json({ success: false, message: 'Current password incorrect' });
    if (newPassword.length < 8) return res.status(400).json({ success: false, message: 'Password must be at least 8 characters' });
    const hash = await bcrypt.hash(newPassword, 12);
    await db.query('UPDATE owner SET password_hash = $1 WHERE id = $2', [hash, req.admin.id]);
    res.json({ success: true, message: 'Password updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── PROFILE (PUBLIC) ── */
app.get('/api/profile', async (_, res) => {
  try {
    const r = await db.query(
      `SELECT name,title,university,bio,email,phone,github_url,linkedin_url,
              twitter_url,leetcode_username,location,cgpa,available_for,
              profile_image_url,resume_url,degree,graduation_year FROM owner LIMIT 1`
    );
    res.json({ success: true, data: r.rows[0] || {} });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/profile', auth, async (req, res) => {
  try {
    const allowed = ['name','title','university','bio','email','phone',
      'github_url','linkedin_url','twitter_url','leetcode_username',
      'location','cgpa','available_for','degree','graduation_year'];
    const fields = Object.keys(req.body).filter(k => allowed.includes(k));
    if (!fields.length) return res.status(400).json({ success: false, message: 'No valid fields' });
    const sets  = fields.map((f, i) => `${f} = $${i + 1}`);
    const vals  = fields.map(f => req.body[f]);
    await db.query(`UPDATE owner SET ${sets.join(', ')} WHERE id = $${fields.length + 1}`, [...vals, req.admin.id]);
    res.json({ success: true, message: 'Profile updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* Upload profile photo */
app.post('/api/profile/photo', auth, upload.single('photo'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: 'No file uploaded' });
    const result = await uploadToCloudinary(req.file.buffer, 'profile', 'image');
    await db.query('UPDATE owner SET profile_image_url = $1 WHERE id = $2', [result.secure_url, req.admin.id]);
    res.json({ success: true, url: result.secure_url });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* Upload resume PDF */
app.post('/api/profile/resume', auth, upload.single('resume'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: 'No file uploaded' });
    const result = await uploadToCloudinary(req.file.buffer, 'resume', 'raw');
    await db.query('UPDATE owner SET resume_url = $1 WHERE id = $2', [result.secure_url, req.admin.id]);
    res.json({ success: true, url: result.secure_url });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── PROJECTS ── */
app.get('/api/projects', async (req, res) => {
  try {
    const { category, featured } = req.query;
    let q = 'SELECT * FROM projects WHERE TRUE';
    const vals = [];
    if (category) { vals.push(category); q += ` AND category = $${vals.length}`; }
    if (featured === 'true') { q += ' AND featured = TRUE'; }
    q += ' ORDER BY sort_order ASC, created_at DESC';
    const r = await db.query(q, vals);
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/projects', auth, upload.single('thumbnail'), async (req, res) => {
  try {
    const { title, description, category, tech_stack, github_url, live_url, featured, sort_order } = req.body;
    if (!title) return res.status(400).json({ success: false, message: 'Title required' });
    let thumbnail_url = '';
    if (req.file) {
      const r = await uploadToCloudinary(req.file.buffer, 'projects', 'image');
      thumbnail_url = r.secure_url;
    }
    const tech = Array.isArray(tech_stack) ? tech_stack : (tech_stack || '').split(',').map(s => s.trim()).filter(Boolean);
    const result = await db.query(
      `INSERT INTO projects (title,description,category,tech_stack,github_url,live_url,thumbnail_url,featured,sort_order)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING *`,
      [title, description || '', category || 'Web Dev', tech, github_url || '', live_url || '', thumbnail_url,
       featured === 'true', parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: result.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/projects/:id', auth, upload.single('thumbnail'), async (req, res) => {
  try {
    const { title, description, category, tech_stack, github_url, live_url, featured, sort_order } = req.body;
    const existing = await db.query('SELECT * FROM projects WHERE id = $1', [req.params.id]);
    if (!existing.rowCount) return res.status(404).json({ success: false, message: 'Project not found' });
    let thumbnail_url = existing.rows[0].thumbnail_url;
    if (req.file) {
      const r = await uploadToCloudinary(req.file.buffer, 'projects', 'image');
      thumbnail_url = r.secure_url;
    }
    const tech = Array.isArray(tech_stack) ? tech_stack : (tech_stack || '').split(',').map(s => s.trim()).filter(Boolean);
    await db.query(
      `UPDATE projects SET title=$1,description=$2,category=$3,tech_stack=$4,github_url=$5,
       live_url=$6,thumbnail_url=$7,featured=$8,sort_order=$9 WHERE id=$10`,
      [title, description || '', category || 'Web Dev', tech, github_url || '', live_url || '',
       thumbnail_url, featured === 'true', parseInt(sort_order) || 0, req.params.id]
    );
    res.json({ success: true, message: 'Project updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/projects/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM projects WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Project deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/certificates/:id', auth, upload.fields([{ name: 'image', maxCount: 1 }, { name: 'pdf', maxCount: 1 }]), async (req, res) => {
  try {
    const { title, issuer, category, issue_date, expiry_date, credential_url, skills, sort_order } = req.body;
    const existing = await db.query('SELECT * FROM certificates WHERE id = $1', [req.params.id]);
    if (!existing.rowCount) return res.status(404).json({ success: false, message: 'Certificate not found' });
    
    let image_url = existing.rows[0].image_url;
    let pdf_url = existing.rows[0].pdf_url;
    
    if (req.files?.image?.[0]) {
      const r = await uploadToCloudinary(req.files.image[0].buffer, 'certificates', 'image');
      image_url = r.secure_url;
    }
    if (req.files?.pdf?.[0]) {
      const r = await uploadToCloudinary(req.files.pdf[0].buffer, 'certificates', 'raw');
      pdf_url = r.secure_url;
    }
    
    const skillArr = Array.isArray(skills) ? skills : (skills || '').split(',').map(s => s.trim()).filter(Boolean);
    await db.query(
      `UPDATE certificates 
       SET title=$1, issuer=$2, category=$3, issue_date=$4, expiry_date=$5, credential_url=$6, image_url=$7, pdf_url=$8, skills=$9, sort_order=$10
       WHERE id=$11`,
      [title, issuer || '', category || 'Other', issue_date || null, expiry_date || null,
       credential_url || '', image_url, pdf_url, skillArr, parseInt(sort_order) || 0, req.params.id]
    );
    res.json({ success: true, message: 'Certificate updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/research/:id', auth, upload.single('pdf'), async (req, res) => {
  try {
    const { title, authors, journal, status, year, abstract, keywords, doi, arxiv_url, citation_count, sort_order } = req.body;
    const existing = await db.query('SELECT * FROM research WHERE id = $1', [req.params.id]);
    if (!existing.rowCount) return res.status(404).json({ success: false, message: 'Research paper not found' });
    
    let pdf_url = existing.rows[0].pdf_url;
    if (req.file) {
      const r = await uploadToCloudinary(req.file.buffer, 'research', 'raw');
      pdf_url = r.secure_url;
    }
    
    const authArr = Array.isArray(authors) ? authors : (authors || '').split(',').map(s => s.trim()).filter(Boolean);
    const kwArr   = Array.isArray(keywords) ? keywords : (keywords || '').split(',').map(s => s.trim()).filter(Boolean);
    
    await db.query(
      `UPDATE research 
       SET title=$1, authors=$2, journal=$3, status=$4, year=$5, abstract=$6, keywords=$7, doi=$8, arxiv_url=$9, pdf_url=$10, citation_count=$11, sort_order=$12
       WHERE id=$13`,
      [title, authArr, journal || '', status || 'Published', parseInt(year) || null,
       abstract || '', kwArr, doi || '', arxiv_url || '', pdf_url,
       parseInt(citation_count) || 0, parseInt(sort_order) || 0, req.params.id]
    );
    res.json({ success: true, message: 'Research updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/skills/:id', auth, async (req, res) => {
  try {
    const { name, category, proficiency, icon, sort_order } = req.body;
    const existing = await db.query('SELECT * FROM skills WHERE id = $1', [req.params.id]);
    if (!existing.rowCount) return res.status(404).json({ success: false, message: 'Skill not found' });
    
    await db.query(
      `UPDATE skills SET name=$1, category=$2, proficiency=$3, icon=$4, sort_order=$5 WHERE id=$6`,
      [name, category || 'Other', Math.min(100, Math.max(0, parseInt(proficiency) || 80)),
       icon || '', parseInt(sort_order) || 0, req.params.id]
    );
    res.json({ success: true, message: 'Skill updated' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── CERTIFICATES ── */
app.get('/api/certificates', async (req, res) => {
  try {
    const { category } = req.query;
    let q = 'SELECT * FROM certificates WHERE TRUE';
    const vals = [];
    if (category) { vals.push(category); q += ` AND category = $${vals.length}`; }
    q += ' ORDER BY sort_order ASC, issue_date DESC';
    const r = await db.query(q, vals);
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/certificates', auth, upload.fields([{ name: 'image', maxCount: 1 }, { name: 'pdf', maxCount: 1 }]), async (req, res) => {
  try {
    const { title, issuer, category, issue_date, expiry_date, credential_url, skills, sort_order } = req.body;
    if (!title) return res.status(400).json({ success: false, message: 'Title required' });
    let image_url = '', pdf_url = '';
    if (req.files?.image?.[0]) {
      const r = await uploadToCloudinary(req.files.image[0].buffer, 'certificates', 'image');
      image_url = r.secure_url;
    }
    if (req.files?.pdf?.[0]) {
      const r = await uploadToCloudinary(req.files.pdf[0].buffer, 'certificates', 'raw');
      pdf_url = r.secure_url;
    }
    const skillArr = Array.isArray(skills) ? skills : (skills || '').split(',').map(s => s.trim()).filter(Boolean);
    const result = await db.query(
      `INSERT INTO certificates (title,issuer,category,issue_date,expiry_date,credential_url,image_url,pdf_url,skills,sort_order)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING *`,
      [title, issuer || '', category || 'Other', issue_date || null, expiry_date || null,
       credential_url || '', image_url, pdf_url, skillArr, parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: result.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/certificates/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM certificates WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Certificate deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── RESEARCH ── */
app.get('/api/research', async (_, res) => {
  try {
    const r = await db.query('SELECT * FROM research ORDER BY sort_order ASC, year DESC');
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/research', auth, upload.single('pdf'), async (req, res) => {
  try {
    const { title, authors, journal, status, year, abstract, keywords, doi, arxiv_url, citation_count, sort_order } = req.body;
    if (!title) return res.status(400).json({ success: false, message: 'Title required' });
    let pdf_url = '';
    if (req.file) {
      const r = await uploadToCloudinary(req.file.buffer, 'research', 'raw');
      pdf_url = r.secure_url;
    }
    const authArr = Array.isArray(authors) ? authors : (authors || '').split(',').map(s => s.trim()).filter(Boolean);
    const kwArr   = Array.isArray(keywords) ? keywords : (keywords || '').split(',').map(s => s.trim()).filter(Boolean);
    const result = await db.query(
      `INSERT INTO research (title,authors,journal,status,year,abstract,keywords,doi,arxiv_url,pdf_url,citation_count,sort_order)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12) RETURNING *`,
      [title, authArr, journal || '', status || 'Published', parseInt(year) || null,
       abstract || '', kwArr, doi || '', arxiv_url || '', pdf_url,
       parseInt(citation_count) || 0, parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: result.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/research/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM research WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Paper deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── SKILLS ── */
app.get('/api/skills', async (_, res) => {
  try {
    const r = await db.query('SELECT * FROM skills ORDER BY category ASC, sort_order ASC, proficiency DESC');
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/skills', auth, async (req, res) => {
  try {
    const { name, category, proficiency, icon, sort_order } = req.body;
    if (!name) return res.status(400).json({ success: false, message: 'Name required' });
    const r = await db.query(
      `INSERT INTO skills (name,category,proficiency,icon,sort_order) VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [name, category || 'Other', Math.min(100, Math.max(0, parseInt(proficiency) || 80)),
       icon || '', parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: r.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/skills/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM skills WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Skill deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── EXPERIENCE ── */
app.get('/api/experience', async (_, res) => {
  try {
    const r = await db.query('SELECT * FROM experience ORDER BY sort_order ASC, start_date DESC');
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/experience', auth, async (req, res) => {
  try {
    const { company, role, start_date, end_date, is_current, description, tech_used, sort_order } = req.body;
    if (!company) return res.status(400).json({ success: false, message: 'Company required' });
    const tech = Array.isArray(tech_used) ? tech_used : (tech_used || '').split(',').map(s => s.trim()).filter(Boolean);
    const r = await db.query(
      `INSERT INTO experience (company,role,start_date,end_date,is_current,description,tech_used,sort_order)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *`,
      [company, role || '', start_date || null, end_date || null, is_current === 'true',
       description || '', tech, parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: r.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/experience/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM experience WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/experience/:id', auth, async (req, res) => {
  try {
    const { company, role, start_date, end_date, is_current, description, tech_used, sort_order } = req.body;
    const tech = Array.isArray(tech_used) ? tech_used : (tech_used || '').split(',').map(s => s.trim()).filter(Boolean);
    const r = await db.query(
      `UPDATE experience SET company=$1,role=$2,start_date=$3,end_date=$4,is_current=$5,
       description=$6,tech_used=$7,sort_order=$8 WHERE id=$9 RETURNING *`,
      [company, role || '', start_date || null, end_date || null, is_current === 'true' || is_current === true,
       description || '', tech, parseInt(sort_order) || 0, req.params.id]
    );
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, data: r.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── ACHIEVEMENTS ── */
app.get('/api/achievements', async (_, res) => {
  try {
    const r = await db.query('SELECT * FROM achievements ORDER BY sort_order ASC, date DESC');
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.post('/api/achievements', auth, async (req, res) => {
  try {
    const { title, description, date, sort_order } = req.body;
    if (!title) return res.status(400).json({ success: false, message: 'Title required' });
    const r = await db.query(
      `INSERT INTO achievements (title,description,date,sort_order) VALUES ($1,$2,$3,$4) RETURNING *`,
      [title, description || '', date || null, parseInt(sort_order) || 0]
    );
    res.status(201).json({ success: true, data: r.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.put('/api/achievements/:id', auth, async (req, res) => {
  try {
    const { title, description, date, sort_order } = req.body;
    const r = await db.query(
      `UPDATE achievements SET title=$1,description=$2,date=$3,sort_order=$4 WHERE id=$5 RETURNING *`,
      [title, description || '', date || null, parseInt(sort_order) || 0, req.params.id]
    );
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, data: r.rows[0] });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/achievements/:id', auth, async (req, res) => {
  try {
    const r = await db.query('DELETE FROM achievements WHERE id = $1 RETURNING id', [req.params.id]);
    if (!r.rowCount) return res.status(404).json({ success: false, message: 'Not found' });
    res.json({ success: true, message: 'Deleted' });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── CONTACT ── */
app.post('/api/contact', contactLimiter, async (req, res) => {
  try {
    const { name, email, subject, message } = req.body;
    if (!name || !email || !message) return res.status(400).json({ success: false, message: 'Name, email, and message are required' });
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ success: false, message: 'Invalid email' });

    /* Save to DB */
    await db.query(
      `INSERT INTO messages (name,email,subject,body) VALUES ($1,$2,$3,$4)`,
      [name.slice(0, 200), email.slice(0, 200), (subject || '').slice(0, 300), message.slice(0, 5000)]
    );

    /* Send email notification (optional — set SMTP vars in .env) */
    if (process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS) {
      try {
        const transporter = nodemailer.createTransport({
          host: process.env.SMTP_HOST,
          port: parseInt(process.env.SMTP_PORT) || 587,
          secure: false,
          auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS }
        });
        await transporter.sendMail({
          from: `"Portfolio Contact" <${process.env.SMTP_USER}>`,
          to:   process.env.NOTIFY_EMAIL || process.env.SMTP_USER,
          replyTo: email,
          subject: `[Portfolio] ${subject || 'New message'} — from ${name}`,
          html: `<h2>New message from ${name}</h2>
                 <p><b>Email:</b> ${email}</p>
                 <p><b>Subject:</b> ${subject || '—'}</p>
                 <p><b>Message:</b></p>
                 <p>${message.replace(/\n/g, '<br>')}</p>`
        });
      } catch (mailErr) {
        console.warn('Email send failed (message saved to DB):', mailErr.message);
      }
    }

    res.json({ success: true, message: "Message received! I'll reply within 24 hours." });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── MESSAGES (Admin) ── */
app.get('/api/messages', auth, async (req, res) => {
  try {
    const r = await db.query('SELECT * FROM messages ORDER BY created_at DESC');
    res.json({ success: true, data: r.rows });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.patch('/api/messages/:id/read', auth, async (req, res) => {
  try {
    await db.query('UPDATE messages SET is_read = TRUE WHERE id = $1', [req.params.id]);
    res.json({ success: true });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

app.delete('/api/messages/:id', auth, async (req, res) => {
  try {
    await db.query('DELETE FROM messages WHERE id = $1', [req.params.id]);
    res.json({ success: true });
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── STATS (Admin overview) ── */
app.get('/api/stats', auth, async (_, res) => {
  try {
    const [projects, certs, research, skills, messages, unread] = await Promise.all([
      db.query('SELECT COUNT(*) FROM projects'),
      db.query('SELECT COUNT(*) FROM certificates'),
      db.query('SELECT COUNT(*) FROM research'),
      db.query('SELECT COUNT(*) FROM skills'),
      db.query('SELECT COUNT(*) FROM messages'),
      db.query('SELECT COUNT(*) FROM messages WHERE is_read = FALSE'),
    ]);
    res.json({ success: true, data: {
      projects:  parseInt(projects.rows[0].count),
      certificates: parseInt(certs.rows[0].count),
      research:  parseInt(research.rows[0].count),
      skills:    parseInt(skills.rows[0].count),
      messages:  parseInt(messages.rows[0].count),
      unread:    parseInt(unread.rows[0].count),
    }});
  } catch (e) { res.status(500).json({ success: false, message: e.message }); }
});

/* ── LEETCODE PROXY (no CORS issues server-side) ── */
app.post('/api/leetcode-proxy', async (req, res) => {
  try {
    const response = await axios.post(
      'https://leetcode.com/graphql',
      req.body,
      { headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com',
                   'User-Agent': 'Mozilla/5.0' }, timeout: 10000 }
    );
    res.json(response.data);
  } catch (e) {
    res.status(502).json({ success: false, message: 'LeetCode API unavailable', error: e.message });
  }
});

/* ─────────────────────────────────────────
   GLOBAL ERROR HANDLER
───────────────────────────────────────── */
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ success: false, message: `Upload error: ${err.message}` });
  }
  console.error('Unhandled error:', err);
  res.status(err.status || 500).json({ success: false, message: err.message || 'Internal Server Error' });
});

/* ─────────────────────────────────────────
   START
───────────────────────────────────────── */
initDB()
  .then(() => {
    app.listen(PORT, () => console.log(`🚀 Portfolio API running on port ${PORT}`));
  })
  .catch(err => {
    console.error('❌ Failed to initialise database:', err);
    process.exit(1);
  });

module.exports = app;
