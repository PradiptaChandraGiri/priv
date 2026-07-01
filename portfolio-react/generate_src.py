"""
Full React portfolio project generator.
Run from: c:/Users/girip/Desktop/portfolio-react
"""
import os

ROOT = r"c:\Users\girip\Desktop\portfolio-react\src"

files = {}

# ─── .env ───────────────────────────────────────────────────────────────────
files["../.env"] = """VITE_API_URL=http://localhost:3001/api
"""

# ─── main.jsx ────────────────────────────────────────────────────────────────
files["main.jsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode><App /></React.StrictMode>
);
"""

# ─── App.jsx ─────────────────────────────────────────────────────────────────
files["App.jsx"] = """import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useThemeStore } from './store/themeStore';
import { useAuthStore } from './store/authStore';
import PageLayout from './components/layout/PageLayout';
import HomePage from './pages/HomePage';
import ProjectsPage from './pages/ProjectsPage';
import CertificatesPage from './pages/CertificatesPage';
import ResearchPage from './pages/ResearchPage';
import SkillsPage from './pages/SkillsPage';
import AboutPage from './pages/AboutPage';
import ResumePage from './pages/ResumePage';
import ContactPage from './pages/ContactPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 5 * 60 * 1000, retry: 1 } },
});

function ProtectedRoute({ children }) {
  const { isAdmin } = useAuthStore();
  return isAdmin ? children : <Navigate to="/admin" replace />;
}

export default function App() {
  const { isDark } = useThemeStore();

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<PageLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/certificates" element={<CertificatesPage />} />
            <Route path="/research" element={<ResearchPage />} />
            <Route path="/skills" element={<SkillsPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/resume" element={<ResumePage />} />
            <Route path="/contact" element={<ContactPage />} />
          </Route>
          <Route path="/admin" element={<AdminLoginPage />} />
          <Route path="/admin/dashboard" element={
            <ProtectedRoute><AdminDashboardPage /></ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
      <Toaster position="bottom-right" toastOptions={{
        style: { background: '#1a202c', color: '#e4e1ed', border: '1px solid rgba(192,193,255,0.2)' }
      }} />
    </QueryClientProvider>
  );
}
"""

# ─── api/axios.js ─────────────────────────────────────────────────────────────
files["api/axios.js"] = """import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token');
      window.location.href = '/admin';
    }
    return Promise.reject(err);
  }
);

export default api;
"""

# ─── Mock data helper ─────────────────────────────────────────────────────────
MOCK_PROFILE = """{
  name: 'Pradipta Chandra Giri',
  title: ['Full Stack Developer', 'ML Enthusiast', 'System Architect', 'Open Source Contributor'],
  tagline: 'Building scalable solutions, one commit at a time',
  bio: "I'm a passionate CS undergrad specializing in full-stack development and system architecture. My approach marries academic rigor with pragmatic engineering, focusing on scalable, high-performance applications built on robust foundations.",
  university: 'Institute of Technology & Engineering',
  degree: 'B.Tech in Computer Science & Engineering',
  graduation_year: 2026,
  cgpa: '8.9',
  available_for: 'SDE Internships, Research Roles, Open Source',
  email: 'pradipta@example.com',
  github: 'https://github.com',
  linkedin: 'https://linkedin.com',
  twitter: 'https://twitter.com',
  leetcode: 'https://leetcode.com',
  profile_image_url: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBz0BGDMuQHjqWjgKuEKMBm-r1VhMpTj_1PoIHgO2okPP8V8q57vUDKOSdicuF_5dZs2fJFgQMUxM-WAkN2cbDv2PPdQ2gbxBL6PQeyeT8_IiN5b0JpVKjfSz-723F3KhgVLexVSQgxMuXm2h0IMkUNdyCG7Nj5JBS7-E0UKCTb1B14Pm1Z4T9ShpGLJzzjwt7w-PGR1H0ljrbpyg2YFBwvk2yT3cqESuPdaZBk0YivyZgDKH8RTjeDbVib0EmKEoDT7PfIdq4fcnU',
  resume_url: '#',
  location: 'Bhubaneswar, Odisha, India',
}"""

# api files
files["api/profile.js"] = f"""import api from './axios';

const MOCK = {MOCK_PROFILE};

export const getProfile = async () => {{
  try {{ const r = await api.get('/profile'); return r.data; }}
  catch {{ return MOCK; }}
}};

export const updateProfile = (data) => api.put('/profile', data);
"""

files["api/projects.js"] = """import api from './axios';

const MOCK = [
  { id: 1, title: 'Distributed Task Scheduler', category: 'systems', description: 'A highly concurrent, fault-tolerant distributed task scheduling system written in Go. Utilizes Raft consensus for high availability.', tech_stack: ['Golang', 'gRPC', 'Docker', 'Raft'], github_url: 'https://github.com', live_url: null, featured: true, status: 'completed', thumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuArGDbFRTLxxWjUCpkccRv_TDFw0ZqIol8ojOQ_ppqag6imfsNTNOjv-mmQm_biYg5SiUqxoi2FQYRezJx10BD_sfp3CRNKGCWnpDvVYtDgV9jNX1zutIprnnTzngalK7Sk3Drjoqi56TR5vXgx7Uw4fVaPRbLhLssglZYqbbTNBucGWft8of5fuhXioPCVk7LIktvI93W4uC_j_oOvwK-N5nN65ewLrOqe0VCoZQb4soVxK3UAIPFKo4U3rQIRUoboOJCyEqiA2AE' },
  { id: 2, title: 'OmniCommerce Platform', category: 'web', description: 'A full-stack e-commerce solution with real-time inventory tracking, secure Stripe integration, and a custom headless CMS backend.', tech_stack: ['React', 'Node.js', 'PostgreSQL', 'Stripe'], github_url: 'https://github.com', live_url: 'https://example.com', featured: true, status: 'completed', thumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDxFG3p6Jsv43N2OZc4MHDAeQamE-zg2FFw4zGy7F8mFUMCBOJOvOhQyRqgDuViE9RO0yMwimlahgFvU3mfcbLeIDidvv7nU0ZtJjzOABM6jZjOQ54GFMi7_MNGqaJOhghqpNYrOM2PAJ0gvhxHSA49oQLNGH4ShprGl_e19AjEsB5hWpOmWIRiVeJpE7oEiTRzzgvQIPpyXqTOYJx6KW_ckmLfspvtCrE_yzJyi3aqdLZozXwet3dElsSvKH9D-CUcV0aCCnxMplQ' },
  { id: 3, title: 'Predictive Maintenance AI', category: 'ml', description: 'Time-series forecasting model using LSTM networks to predict equipment failure in industrial IoT sensors. Achieved 94% accuracy.', tech_stack: ['Python', 'TensorFlow', 'Pandas', 'FastAPI'], github_url: 'https://github.com', live_url: null, featured: true, status: 'completed', thumbnail: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDmEBJEoLfzG-83ctyTbGFwBHYcfxaWXJcpWQw5Y0HxzAqOS1NjkC2-yoxl-RKYOXkc2DocJdKUJpIYZ12P_f3jkQhHRbbekMD_QDJEu8vVUlB5rjqBTKpQtK0sXz-0nnGUcCUb1xOj-_wXQ2DYj-Va6z94-4ccWFFprDaOkp6TA5ffd0l3rqPxQuRsDnTA6jlfewSs5ckx0cfW8fo3FGsEXZ-BpV-MZ0M9Ixx64arc7mT6fcx0hQ3apDhOXqOO5X-RkM8DzLrNym8' },
  { id: 4, title: 'SmartAttend', category: 'ml', description: 'Face recognition attendance system using OpenCV and deep learning. Deployed in campus labs.', tech_stack: ['Python', 'OpenCV', 'Flask', 'React'], github_url: 'https://github.com', live_url: null, featured: false, status: 'completed', thumbnail: null },
  { id: 5, title: 'DevConnect', category: 'web', description: 'Real-time developer collaboration platform with code sharing, video calls, and project management.', tech_stack: ['Next.js', 'WebRTC', 'Socket.io', 'MongoDB'], github_url: 'https://github.com', live_url: 'https://example.com', featured: false, status: 'ongoing', thumbnail: null },
];

export const getProjects = async (params) => {
  try { const r = await api.get('/projects', { params }); return r.data; }
  catch { 
    if (params?.featured) return MOCK.filter(p => p.featured);
    if (params?.category && params.category !== 'all') return MOCK.filter(p => p.category === params.category);
    return MOCK;
  }
};
export const createProject = (data) => api.post('/projects', data);
export const updateProject = (id, data) => api.put(`/projects/${id}`, data);
export const deleteProject = (id) => api.delete(`/projects/${id}`);
"""

files["api/certificates.js"] = """import api from './axios';

const MOCK = [
  { id: 1, title: 'Machine Learning Specialization', issuing_org: 'Coursera / DeepLearning.AI', category: 'AI/ML', issue_date: '2024-01-15', skills_gained: ['Supervised Learning', 'Neural Networks', 'TensorFlow'], credential_url: 'https://coursera.org', featured: true, thumbnail: null },
  { id: 2, title: 'AWS Solutions Architect Associate', issuing_org: 'Amazon Web Services', category: 'Cloud', issue_date: '2023-08-20', skills_gained: ['EC2', 'S3', 'Lambda', 'CloudFormation'], credential_url: 'https://aws.amazon.com', featured: true, thumbnail: null },
  { id: 3, title: 'Full Stack Web Development', issuing_org: 'The Odin Project', category: 'Web Dev', issue_date: '2023-03-10', skills_gained: ['React', 'Node.js', 'PostgreSQL'], credential_url: null, featured: false, thumbnail: null },
  { id: 4, title: 'Data Structures & Algorithms', issuing_org: 'Coursera / Stanford', category: 'DSA', issue_date: '2022-12-05', skills_gained: ['Algorithms', 'Graphs', 'Dynamic Programming'], credential_url: 'https://coursera.org', featured: false, thumbnail: null },
];

export const getCertificates = async (params) => {
  try { const r = await api.get('/certificates', { params }); return r.data; }
  catch {
    if (params?.category && params.category !== 'All') return MOCK.filter(c => c.category === params.category);
    return MOCK;
  }
};
export const createCertificate = (data) => api.post('/certificates', data);
export const deleteCertificate = (id) => api.delete(`/certificates/${id}`);
"""

files["api/research.js"] = """import api from './axios';

const MOCK = [
  { id: 1, title: 'Efficient Attention Mechanisms for Long-Range Dependencies in Transformers', authors: ['Pradipta Chandra Giri', 'Dr. Suresh Kumar'], journal: 'arXiv Preprint', status: 'preprint', date: '2024-02-10', abstract: 'We propose a novel attention mechanism that reduces the quadratic complexity of self-attention to linear, enabling transformers to process significantly longer sequences without memory overflow. Our method achieves state-of-the-art results on several NLP benchmarks while reducing compute by 60%.', keywords: ['NLP', 'Transformers', 'Attention', 'Deep Learning'], citations: 0, arxiv_url: 'https://arxiv.org', doi: null, paper_url: null },
  { id: 2, title: 'Federated Learning for Privacy-Preserving IoT Anomaly Detection', authors: ['Pradipta Chandra Giri', 'Prof. Anjali Sharma', 'Dr. Ravi Mohan'], journal: 'IEEE Internet of Things Journal', status: 'under_review', date: '2023-11-20', abstract: 'A federated learning framework for detecting anomalies in distributed IoT networks while preserving data privacy. We demonstrate that our approach achieves comparable accuracy to centralized methods while keeping data on-device.', keywords: ['Federated Learning', 'IoT', 'Privacy', 'Anomaly Detection'], citations: 3, arxiv_url: null, doi: '10.1109/jiot.2023', paper_url: null },
];

export const getResearch = async () => {
  try { const r = await api.get('/research'); return r.data; }
  catch { return MOCK; }
};
export const createResearch = (data) => api.post('/research', data);
export const deleteResearch = (id) => api.delete(`/research/${id}`);
"""

files["api/skills.js"] = """import api from './axios';

const MOCK = [
  { id:1, name:'React', category:'Frontend', proficiency:90, icon:'⚛️' },
  { id:2, name:'TypeScript', category:'Frontend', proficiency:85, icon:'📘' },
  { id:3, name:'Next.js', category:'Frontend', proficiency:80, icon:'▲' },
  { id:4, name:'Tailwind CSS', category:'Frontend', proficiency:95, icon:'🎨' },
  { id:5, name:'Node.js', category:'Backend', proficiency:88, icon:'🟢' },
  { id:6, name:'Python', category:'Backend', proficiency:92, icon:'🐍' },
  { id:7, name:'FastAPI', category:'Backend', proficiency:80, icon:'⚡' },
  { id:8, name:'Go', category:'Backend', proficiency:70, icon:'🔵' },
  { id:9, name:'PostgreSQL', category:'Database', proficiency:85, icon:'🐘' },
  { id:10, name:'MongoDB', category:'Database', proficiency:78, icon:'🍃' },
  { id:11, name:'Redis', category:'Database', proficiency:72, icon:'🔴' },
  { id:12, name:'Docker', category:'DevOps', proficiency:82, icon:'🐳' },
  { id:13, name:'AWS', category:'DevOps', proficiency:75, icon:'☁️' },
  { id:14, name:'TensorFlow', category:'AI/ML', proficiency:80, icon:'🧠' },
  { id:15, name:'PyTorch', category:'AI/ML', proficiency:75, icon:'🔥' },
  { id:16, name:'Git', category:'Tools', proficiency:95, icon:'📦' },
];

export const getSkills = async () => {
  try { const r = await api.get('/skills'); return r.data; }
  catch { return MOCK; }
};
export const createSkill = (data) => api.post('/skills', data);
export const deleteSkill = (id) => api.delete(`/skills/${id}`);
"""

files["api/achievements.js"] = """import api from './axios';
const MOCK = [
  { id:1, title:'LeetCode 1800+ Rating', description:'Top 5% globally in competitive programming', date:'2024', icon:'🏆' },
  { id:2, title:'Smart India Hackathon Finalist', description:'National-level hackathon, Top 20 teams', date:'2023', icon:'🥇' },
  { id:3, title:'Google Summer of Code', description:'Selected contributor to an open-source org', date:'2024', icon:'🌟' },
];
export const getAchievements = async () => {
  try { return (await api.get('/achievements')).data; } catch { return MOCK; }
};
export const createAchievement = (data) => api.post('/achievements', data);
export const deleteAchievement = (id) => api.delete(`/achievements/${id}`);
"""

files["api/experience.js"] = """import api from './axios';
const MOCK = [
  { id:1, company:'TechNova Solutions', role:'Software Engineering Intern', start_date:'2024-05', end_date:null, current:true, description:['Engineered scalable microservices using Node.js and Docker, reducing API latency by 30%','Implemented CI/CD pipelines via GitHub Actions'] },
  { id:2, company:'Open Source (CNCF)', role:'GSoC Contributor', start_date:'2024-06', end_date:'2024-09', current:false, description:['Contributed to a CNCF project, merged 12 PRs','Implemented distributed tracing module'] },
];
export const getExperience = async () => {
  try { return (await api.get('/experience')).data; } catch { return MOCK; }
};
export const createExperience = (data) => api.post('/experience', data);
export const deleteExperience = (id) => api.delete(`/experience/${id}`);
"""

files["api/contact.js"] = """import api from './axios';
export const submitContact = (data) => api.post('/contact', data);
export const getMessages = async () => {
  try { return (await api.get('/messages')).data; } catch { return [
    { id:1, name:'Jane Doe', email:'jane@company.com', subject:'Job Opportunity', message:'Hi, we have an exciting SDE role at our startup...', read:false, date:'2024-06-20' },
    { id:2, name:'Prof. Smith', email:'smith@university.edu', subject:'Collaboration', message:'I came across your ML research and would like to collaborate...', read:true, date:'2024-06-18' },
  ]; }
};
export const markRead = (id) => api.patch(`/messages/${id}/read`);
"""

# ─── store ────────────────────────────────────────────────────────────────────
files["store/authStore.js"] = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      isAdmin: false,
      adminName: 'Admin',
      login: (token, name = 'Admin') => {
        localStorage.setItem('admin_token', token);
        set({ token, isAdmin: true, adminName: name });
      },
      logout: () => {
        localStorage.removeItem('admin_token');
        set({ token: null, isAdmin: false });
      },
    }),
    { name: 'auth-storage' }
  )
);
"""

files["store/themeStore.js"] = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useThemeStore = create(
  persist(
    (set, get) => ({
      isDark: true,
      toggle: () => set({ isDark: !get().isDark }),
    }),
    { name: 'theme-storage' }
  )
);
"""

# ─── hooks ────────────────────────────────────────────────────────────────────
files["hooks/useProfile.js"] = """import { useQuery } from '@tanstack/react-query';
import { getProfile } from '../api/profile';
export const useProfile = () => useQuery({ queryKey: ['profile'], queryFn: getProfile });
"""

files["hooks/useProjects.js"] = """import { useQuery } from '@tanstack/react-query';
import { getProjects } from '../api/projects';
export const useProjects = (params) => useQuery({ queryKey: ['projects', params], queryFn: () => getProjects(params) });
"""

files["hooks/useCertificates.js"] = """import { useQuery } from '@tanstack/react-query';
import { getCertificates } from '../api/certificates';
export const useCertificates = (params) => useQuery({ queryKey: ['certificates', params], queryFn: () => getCertificates(params) });
"""

files["hooks/useResearch.js"] = """import { useQuery } from '@tanstack/react-query';
import { getResearch } from '../api/research';
export const useResearch = () => useQuery({ queryKey: ['research'], queryFn: getResearch });
"""

files["hooks/useSkills.js"] = """import { useQuery } from '@tanstack/react-query';
import { getSkills } from '../api/skills';
export const useSkills = () => useQuery({ queryKey: ['skills'], queryFn: getSkills });
"""

# ─── components/layout ────────────────────────────────────────────────────────
files["components/layout/Navbar.jsx"] = """import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Menu, X, FileText } from 'lucide-react';
import { useThemeStore } from '../../store/themeStore';

const links = [
  { to: '/', label: 'Home' },
  { to: '/projects', label: 'Projects' },
  { to: '/certificates', label: 'Certificates' },
  { to: '/research', label: 'Research' },
  { to: '/skills', label: 'Skills' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
];

export default function Navbar() {
  const { isDark, toggle } = useThemeStore();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const loc = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => { setMenuOpen(false); }, [loc.pathname]);

  const isActive = (to) => to === '/' ? loc.pathname === '/' : loc.pathname.startsWith(to);

  return (
    <>
      <header className={`fixed top-0 w-full z-50 transition-all duration-300 border-b border-white/10 bg-surface/60 backdrop-blur-xl ${scrolled ? 'shadow-[0_4px_24px_rgba(0,0,0,0.4)]' : ''}`}>
        <div className="flex justify-between items-center h-16 px-5 md:px-16 max-w-7xl mx-auto">
          <Link to="/" className="font-display font-bold text-2xl bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent">BTech Portfolio</Link>
          <nav className="hidden md:flex items-center gap-6">
            {links.map(l => (
              <Link key={l.to} to={l.to} className={`font-mono text-[11px] uppercase tracking-wider transition-colors duration-300 px-2 py-1 ${isActive(l.to) ? 'text-primary font-semibold border-b-2 border-primary pb-0' : 'text-on-surface-variant hover:text-primary'}`}>{l.label}</Link>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <button onClick={toggle} className="p-2 rounded-full text-on-surface-variant hover:text-primary transition-all duration-300 hover:rotate-180">
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            <Link to="/resume" className="hidden md:flex p-2 rounded-full text-on-surface-variant hover:text-primary transition-all"><FileText size={18} /></Link>
            <Link to="/contact" className="hidden md:block bg-primary text-on-primary font-mono text-[11px] uppercase tracking-wider px-5 py-2 rounded-full hover:bg-primary-light transition-all hover:shadow-glow-sm font-semibold">Hire Me</Link>
            <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2 text-on-surface-variant hover:text-primary transition-colors">
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {menuOpen && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-40 md:hidden">
            <div className="absolute inset-0 bg-background/90 backdrop-blur-md" onClick={() => setMenuOpen(false)} />
            <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }} transition={{ type: 'tween', duration: 0.3 }}
              className="absolute right-0 top-0 h-full w-72 bg-surface-container border-l border-outline-variant/30 flex flex-col p-6 pt-20">
              {links.map(l => (
                <Link key={l.to} to={l.to} className={`py-3 border-b border-outline-variant/20 font-mono text-[11px] uppercase tracking-wider transition-colors ${isActive(l.to) ? 'text-primary font-bold' : 'text-on-surface-variant hover:text-primary'}`}>{l.label}</Link>
              ))}
              <Link to="/resume" className="py-3 border-b border-outline-variant/20 font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors">Resume</Link>
              <Link to="/contact" className="mt-6 bg-primary text-on-primary px-4 py-3 rounded-lg font-mono text-[11px] uppercase tracking-wider text-center hover:bg-primary-light transition-all font-semibold">Hire Me</Link>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
"""

files["components/layout/Footer.jsx"] = """import { Link } from 'react-router-dom';
import { Github, Linkedin, Twitter, Code2 } from 'lucide-react';

const quickLinks = [
  { to: '/projects', label: 'Projects' },
  { to: '/certificates', label: 'Certificates' },
  { to: '/research', label: 'Research' },
  { to: '/contact', label: 'Contact' },
];

const socials = [
  { href: 'https://github.com', icon: Github, label: 'GitHub' },
  { href: 'https://linkedin.com', icon: Linkedin, label: 'LinkedIn' },
  { href: 'https://twitter.com', icon: Twitter, label: 'Twitter' },
  { href: 'https://leetcode.com', icon: Code2, label: 'LeetCode' },
];

export default function Footer() {
  return (
    <footer className="bg-background border-t border-white/10 w-full py-12">
      <div className="max-w-7xl mx-auto px-5 md:px-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div className="flex flex-col gap-3">
            <Link to="/" className="font-display font-bold text-2xl bg-gradient-to-r from-primary to-tertiary bg-clip-text text-transparent w-fit">BTech Portfolio</Link>
            <p className="font-body text-sm text-on-surface-variant opacity-60 max-w-xs">CS engineering student targeting top-tier tech companies, research institutes, and competitive internship programs.</p>
          </div>
          <div className="flex flex-col gap-2">
            <span className="font-mono text-[11px] uppercase tracking-wider text-primary mb-1">Quick Links</span>
            {quickLinks.map(l => (
              <Link key={l.to} to={l.to} className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-colors opacity-80 hover:opacity-100 hover:-translate-y-0.5 transform transition-transform w-fit">{l.label}</Link>
            ))}
          </div>
          <div className="flex flex-col gap-2">
            <span className="font-mono text-[11px] uppercase tracking-wider text-primary mb-1">Connect</span>
            {socials.map(s => (
              <a key={s.label} href={s.href} target="_blank" rel="noopener noreferrer"
                className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant hover:text-primary transition-all opacity-80 hover:opacity-100 hover:-translate-y-0.5 flex items-center gap-2 w-fit">
                <s.icon size={14} />{s.label}
              </a>
            ))}
          </div>
        </div>
        <div className="border-t border-white/10 pt-6 flex flex-col md:flex-row items-center justify-between gap-2">
          <p className="font-mono text-[10px] text-on-surface-variant opacity-40">© 2024 Engineering Portfolio. Built with ❤️ and React.</p>
          <div className="flex gap-4">
            <a href="#" className="font-mono text-[10px] text-on-surface-variant hover:text-primary transition-colors opacity-40 hover:opacity-100">Privacy</a>
            <a href="#" className="font-mono text-[10px] text-on-surface-variant hover:text-primary transition-colors opacity-40 hover:opacity-100">Terms</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
"""

files["components/layout/PageLayout.jsx"] = """import { Outlet, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from './Navbar';
import Footer from './Footer';

export default function PageLayout() {
  const loc = useLocation();
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <AnimatePresence mode="wait">
        <motion.main key={loc.pathname} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.3 }} className="flex-grow pt-16">
          <Outlet />
        </motion.main>
      </AnimatePresence>
      <Footer />
    </div>
  );
}
"""

# ─── UI components ─────────────────────────────────────────────────────────────
files["components/ui/Button.jsx"] = """import { clsx } from 'clsx';
export default function Button({ children, variant='primary', className='', ...props }) {
  const base = 'font-mono text-[11px] uppercase tracking-wider px-6 py-3 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-semibold disabled:opacity-50 disabled:cursor-not-allowed';
  const variants = {
    primary: 'bg-primary text-on-primary hover:bg-primary-light hover:shadow-glow-sm',
    outline: 'glass-panel text-primary hover:bg-primary/10 border border-primary/30',
    ghost: 'text-on-surface-variant hover:text-primary hover:bg-primary/10',
    danger: 'bg-error/20 text-error border border-error/30 hover:bg-error/30',
    pill: 'bg-primary text-on-primary rounded-full hover:bg-primary-light hover:shadow-glow-sm',
  };
  return <button className={clsx(base, variants[variant], className)} {...props}>{children}</button>;
}
"""

files["components/ui/Badge.jsx"] = """import { clsx } from 'clsx';
export default function Badge({ children, variant='primary', size='md', className='' }) {
  const base = 'rounded-full font-mono uppercase tracking-wider inline-flex items-center';
  const sizes = { sm: 'text-[9px] px-2 py-0.5', md: 'text-[10px] px-3 py-1', lg: 'text-xs px-4 py-1.5' };
  const variants = {
    primary: 'bg-primary/15 text-primary border border-primary/30',
    secondary: 'bg-secondary/15 text-secondary border border-secondary/30',
    success: 'bg-success/15 text-success border border-success/30',
    warning: 'bg-warning/15 text-warning border border-warning/30',
    error: 'bg-error/15 text-error border border-error/30',
    neutral: 'bg-white/5 text-on-surface-variant border border-outline-variant/30',
    tertiary: 'bg-tertiary/15 text-tertiary border border-tertiary/30',
  };
  return <span className={clsx(base, sizes[size], variants[variant], className)}>{children}</span>;
}
"""

files["components/ui/GlassCard.jsx"] = """import { clsx } from 'clsx';
export default function GlassCard({ children, className='', hover=true }) {
  return (
    <div className={clsx(
      'glass-card backdrop-blur-xl rounded-lg border border-white/10 bg-surface-container/50',
      hover && 'hover:-translate-y-1 hover:shadow-card transition-all duration-300',
      className
    )}>{children}</div>
  );
}
"""

files["components/ui/Card.jsx"] = """import { motion } from 'framer-motion';
import { clsx } from 'clsx';
export default function Card({ children, className='', delay=0 }) {
  return (
    <motion.div initial={{ opacity:0, y:20 }} whileInView={{ opacity:1, y:0 }} viewport={{ once:true }} transition={{ duration:0.5, delay }} whileHover={{ y:-4, scale:1.01 }}
      className={clsx('glass-card rounded-lg border border-white/10 bg-surface-container/50 transition-shadow hover:shadow-card', className)}>
      {children}
    </motion.div>
  );
}
"""

files["components/ui/SkeletonCard.jsx"] = """export default function SkeletonCard({ height='h-64' }) {
  return (
    <div className={`rounded-lg border border-white/10 overflow-hidden ${height}`}>
      <div className="skeleton-shimmer h-1/2 rounded-none" />
      <div className="p-4 space-y-3">
        <div className="skeleton-shimmer h-3 w-2/3 rounded" />
        <div className="skeleton-shimmer h-3 w-full rounded" />
        <div className="skeleton-shimmer h-3 w-4/5 rounded" />
        <div className="flex gap-2 mt-4">
          {[1,2,3].map(i => <div key={i} className="skeleton-shimmer h-5 w-12 rounded-full" />)}
        </div>
      </div>
    </div>
  );
}
"""

files["components/ui/SectionHeader.jsx"] = """export default function SectionHeader({ title, subtitle, viewAll, viewAllLink }) {
  return (
    <div className="text-center mb-12">
      <h2 className="font-display font-bold text-3xl md:text-4xl bg-gradient-to-r from-primary via-secondary to-tertiary bg-clip-text text-transparent mb-3">{title}</h2>
      {subtitle && <p className="font-body text-on-surface-variant max-w-2xl mx-auto">{subtitle}</p>}
      {viewAll && <a href={viewAllLink || '#'} className="inline-flex items-center gap-1 font-mono text-[11px] uppercase tracking-wider text-primary hover:text-primary-light mt-2 transition-colors">{viewAll} →</a>}
    </div>
  );
}
"""

files["components/ui/Modal.jsx"] = """import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
export default function Modal({ open, onClose, children, title }) {
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => { window.removeEventListener('keydown', onKey); document.body.style.overflow = ''; };
  }, [open, onClose]);
  return (
    <AnimatePresence>
      {open && (
        <motion.div initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-background/80 backdrop-blur-md" onClick={onClose} />
          <motion.div initial={{scale:0.95,opacity:0}} animate={{scale:1,opacity:1}} exit={{scale:0.95,opacity:0}}
            className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto glass-card rounded-xl border border-white/10 shadow-card">
            <div className="flex items-center justify-between p-4 border-b border-white/10">
              {title && <h3 className="font-display font-semibold text-on-surface">{title}</h3>}
              <button onClick={onClose} className="ml-auto p-1.5 rounded-lg text-on-surface-variant hover:text-primary hover:bg-primary/10 transition-all"><X size={18}/></button>
            </div>
            <div className="p-6">{children}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
"""

files["components/ui/FileUpload.jsx"] = """import { useDropzone } from 'react-dropzone';
import { UploadCloud, X, FileText } from 'lucide-react';
export default function FileUpload({ onFile, accept, file, label='Drop files here or click to browse' }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (f) => f[0] && onFile(f[0]),
    accept: accept || { 'image/*': [], 'application/pdf': [] },
    maxFiles: 1,
  });
  return (
    <div>
      <div {...getRootProps()} className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${isDragActive ? 'border-primary bg-primary/10' : 'border-outline-variant/40 hover:border-primary/50 hover:bg-primary/5'}`}>
        <input {...getInputProps()} />
        <UploadCloud className="mx-auto mb-3 text-on-surface-variant" size={32}/>
        <p className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant">{isDragActive ? 'Drop it!' : label}</p>
      </div>
      {file && (
        <div className="mt-3 flex items-center gap-3 glass-panel rounded-lg p-3">
          {file.type?.startsWith('image/') ? <img src={URL.createObjectURL(file)} className="w-10 h-10 rounded object-cover" alt="preview"/> : <FileText size={20} className="text-primary"/>}
          <span className="font-mono text-xs text-on-surface-variant flex-1 truncate">{file.name}</span>
          <button onClick={() => onFile(null)} className="text-on-surface-variant hover:text-error transition-colors"><X size={16}/></button>
        </div>
      )}
    </div>
  );
}
"""

# ─── home components ─────────────────────────────────────────────────────────
files["components/home/HeroSection.jsx"] = """import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Download, Github, Linkedin, Twitter, Code2, ChevronDown } from 'lucide-react';

const roles = ['Full Stack Developer', 'ML Enthusiast', 'System Architect', 'Open Source Contributor'];

export default function HeroSection({ profile }) {
  const [roleIdx, setRoleIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);
  const [displayText, setDisplayText] = useState('');

  useEffect(() => {
    const curr = roles[roleIdx];
    const speed = deleting ? 40 : 80;
    const timer = setTimeout(() => {
      if (!deleting) {
        setDisplayText(curr.slice(0, charIdx + 1));
        if (charIdx + 1 === curr.length) setTimeout(() => setDeleting(true), 2000);
        else setCharIdx(c => c + 1);
      } else {
        setDisplayText(curr.slice(0, charIdx - 1));
        if (charIdx - 1 === 0) { setDeleting(false); setRoleIdx(i => (i + 1) % roles.length); setTimeout(() => setCharIdx(0), 400); }
        else setCharIdx(c => c - 1);
      }
    }, speed);
    return () => clearTimeout(timer);
  }, [charIdx, deleting, roleIdx]);

  const socials = [
    { href: profile?.github || '#', icon: Github, label: 'GitHub' },
    { href: profile?.linkedin || '#', icon: Linkedin, label: 'LinkedIn' },
    { href: profile?.twitter || '#', icon: Twitter, label: 'Twitter' },
    { href: profile?.leetcode || '#', icon: Code2, label: 'LeetCode' },
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center pt-16 pb-12 px-5 md:px-16 overflow-hidden">
      {/* Animated orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-float-slow pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-secondary/10 rounded-full blur-3xl animate-float-med pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 w-72 h-72 bg-accent/8 rounded-full blur-3xl animate-float-fast pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center w-full">
        {/* Text */}
        <motion.div className="flex flex-col gap-6 order-2 md:order-1 text-center md:text-left" initial={{ opacity: 0, x: -40 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/20 w-fit mx-auto md:mx-0 font-mono text-xs">
            <span>⚡</span> Hello, I'm
          </motion.div>
          <div>
            <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="font-display font-bold text-4xl md:text-6xl text-on-surface mb-2">
              {profile?.name?.split(' ')[0] || 'Pradipta'} <span className="gradient-text">{profile?.name?.split(' ').slice(1).join(' ') || 'Chandra'}</span>
            </motion.h1>
            <motion.h2 initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="font-display text-xl md:text-2xl text-on-surface-variant h-8 flex items-center justify-center md:justify-start gap-1">
              {displayText}<span className="animate-blink text-primary">|</span>
            </motion.h2>
          </div>
          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} className="font-body text-on-surface-variant max-w-xl leading-relaxed">
            {profile?.bio?.slice(0, 160) || 'CS Engineering student specializing in scalable architectures and ML integrations.'}...
          </motion.p>
          {/* Stats */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="flex gap-6 justify-center md:justify-start glass-panel rounded-xl p-4 w-fit mx-auto md:mx-0">
            <div className="text-center px-4 border-r border-outline-variant/30"><div className="font-display font-bold text-2xl text-primary">12+</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">Projects</div></div>
            <div className="text-center px-4 border-r border-outline-variant/30"><div className="font-display font-bold text-2xl text-tertiary">8+</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">Certs</div></div>
            <div className="text-center px-4"><div className="font-display font-bold text-2xl text-secondary">{profile?.cgpa || '8.9'}</div><div className="font-mono text-[10px] text-on-surface-variant uppercase">CGPA</div></div>
          </motion.div>
          {/* CTAs */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.7 }} className="flex flex-wrap gap-4 justify-center md:justify-start">
            <Link to="/projects" className="btn-primary shadow-glow-sm"><span>View My Work</span><ArrowRight size={16}/></Link>
            <a href={profile?.resume_url || '#'} className="btn-outline"><Download size={16}/><span>Download Resume</span></a>
          </motion.div>
          {/* Social icons */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }} className="flex gap-3 justify-center md:justify-start">
            {socials.map(s => (
              <a key={s.label} href={s.href} target="_blank" rel="noopener noreferrer" title={s.label}
                className="w-11 h-11 glass-panel rounded-full flex items-center justify-center text-on-surface-variant hover:text-primary hover:border-primary/40 hover:-translate-y-1 hover:shadow-glow-sm transition-all">
                <s.icon size={18}/>
              </a>
            ))}
          </motion.div>
        </motion.div>
        {/* Profile Photo */}
        <motion.div className="order-1 md:order-2 flex justify-center" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.7 }}>
          <div className="w-64 h-64 md:w-80 md:h-80 rounded-full p-2 bg-gradient-to-tr from-primary to-secondary animate-pulse-ring">
            <img src={profile?.profile_image_url} alt={profile?.name} loading="lazy" className="w-full h-full rounded-full object-cover border-4 border-surface" onError={e => { e.target.style.display='none'; }} />
          </div>
        </motion.div>
      </div>
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-50">
        <span className="font-mono text-[9px] uppercase tracking-widest text-on-surface-variant">Scroll</span>
        <ChevronDown size={20} className="text-on-surface-variant animate-bounce" />
      </div>
    </section>
  );
}
"""

files["components/home/StatsSection.jsx"] = """import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { FolderCode, Award, BookOpen, Layers } from 'lucide-react';

const stats = [
  { label: 'Projects Built', value: 12, suffix: '+', icon: FolderCode, color: 'text-primary', bg: 'bg-primary/10', border: 'border-primary/20' },
  { label: 'Certificates Earned', value: 8, suffix: '+', icon: Award, color: 'text-tertiary', bg: 'bg-tertiary/10', border: 'border-tertiary/20' },
  { label: 'Research Papers', value: 2, suffix: '', icon: BookOpen, color: 'text-secondary', bg: 'bg-secondary/10', border: 'border-secondary/20' },
  { label: 'Tech Skills', value: 20, suffix: '+', icon: Layers, color: 'text-primary', bg: 'bg-primary/10', border: 'border-primary/20' },
];

function AnimatedNumber({ target, suffix }) {
  const [val, setVal] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        let start = 0;
        const step = () => { start += Math.ceil(target / 40); if (start >= target) { setVal(target); } else { setVal(start); requestAnimationFrame(step); } };
        requestAnimationFrame(step);
        obs.disconnect();
      }
    }, { threshold: 0.5 });
    if (ref.current) obs.observe(ref.current);
    return () => obs.disconnect();
  }, [target]);
  return <span ref={ref}>{val}{suffix}</span>;
}

export default function StatsSection() {
  return (
    <section className="py-20 px-5 md:px-16 border-y border-outline-variant/10 bg-background">
      <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity:0, y:20 }} whileInView={{ opacity:1, y:0 }} viewport={{ once:true }} transition={{ delay: i * 0.1 }} whileHover={{ y: -4 }}
            className="glass-card rounded-xl p-6 flex flex-col items-center text-center gap-3">
            <div className={`w-12 h-12 rounded-full ${s.bg} flex items-center justify-center border ${s.border}`}>
              <s.icon size={22} className={s.color}/>
            </div>
            <div className={`font-display font-bold text-3xl ${s.color}`}>
              <AnimatedNumber target={s.value} suffix={s.suffix} />
            </div>
            <div className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">{s.label}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
"""

files["components/home/FeaturedProjects.jsx"] = """import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Github, ExternalLink, ArrowRight } from 'lucide-react';
import { useProjects } from '../../hooks/useProjects';
import SkeletonCard from '../ui/SkeletonCard';
import Badge from '../ui/Badge';
import SectionHeader from '../ui/SectionHeader';

const catColor = { web:'primary', ml:'secondary', systems:'tertiary', mobile:'accent' };

export default function FeaturedProjects() {
  const { data: projects, isLoading } = useProjects({ featured: true });
  return (
    <section className="py-20 px-5 md:px-16 bg-surface/30">
      <div className="max-w-7xl mx-auto">
        <SectionHeader title="Featured Projects" subtitle="A selection of my most impactful technical work" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {isLoading ? [1,2,3].map(i => <SkeletonCard key={i}/>) : projects?.slice(0,3).map((p, i) => (
            <motion.div key={p.id} initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.1}} whileHover={{y:-6, scale:1.01}}
              className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300 border-t-4"
              style={{borderTopColor: p.category==='ml'?'#d0bcff':p.category==='systems'?'#ffb783':'#c0c1ff'}}>
              {p.thumbnail && <img src={p.thumbnail} alt={p.title} loading="lazy" className="h-40 w-full object-cover opacity-80"/>}
              {!p.thumbnail && <div className="h-40 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center"><span className="font-display font-bold text-5xl text-primary/40">{p.title[0]}</span></div>}
              <div className="p-5 flex flex-col flex-1">
                <Badge variant={catColor[p.category]||'primary'} className="mb-2 w-fit">{p.category}</Badge>
                <h3 className="font-display font-semibold text-on-surface mb-2">{p.title}</h3>
                <p className="font-body text-sm text-on-surface-variant mb-4 flex-1 line-clamp-2">{p.description}</p>
                <div className="flex flex-wrap gap-1.5 mb-4">{p.tech_stack?.slice(0,3).map(t => <span key={t} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full uppercase">{t}</span>)}</div>
                <div className="flex items-center gap-3 border-t border-white/10 pt-3 mt-auto">
                  {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><Github size={16}/></a>}
                  {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><ExternalLink size={16}/></a>}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        <div className="text-center"><Link to="/projects" className="btn-outline mx-auto w-fit">View All Projects <ArrowRight size={14}/></Link></div>
      </div>
    </section>
  );
}
"""

files["components/home/SkillsPreview.jsx"] = """import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useSkills } from '../../hooks/useSkills';
import SectionHeader from '../ui/SectionHeader';

export default function SkillsPreview() {
  const { data: skills } = useSkills();
  const top = skills?.slice(0, 12) || [];
  return (
    <section className="py-20 px-5 md:px-16 border-y border-outline-variant/10">
      <div className="max-w-7xl mx-auto">
        <SectionHeader title="My Tech Stack" subtitle="Technologies I work with daily" viewAll="View All Skills" viewAllLink="/skills" />
        <div className="flex flex-wrap justify-center gap-3">
          {top.map((s, i) => (
            <motion.div key={s.id} initial={{opacity:0,y:10}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.05}} whileHover={{y:-4,scale:1.05}}
              className="glass-panel px-4 py-2.5 rounded-full flex items-center gap-2 cursor-pointer hover:border-primary/40 hover:shadow-glow-sm transition-all">
              <span className="text-lg">{s.icon}</span>
              <span className="font-mono text-xs text-primary">{s.name}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
"""

files["components/home/CTASection.jsx"] = """import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, FileText } from 'lucide-react';
export default function CTASection({ profile }) {
  return (
    <section className="py-20 px-5 md:px-16" style={{background:'linear-gradient(135deg,rgba(192,193,255,0.08),rgba(208,188,255,0.08))'}}>
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} className="flex flex-col md:flex-row items-center justify-between gap-8 text-center md:text-left">
          <div>
            <h2 className="font-display font-bold text-3xl md:text-4xl text-on-surface mb-3">Open to <span className="gradient-text">Opportunities</span></h2>
            <p className="font-body text-on-surface-variant max-w-lg">{profile?.available_for || 'SDE Internships, Research Roles, Open Source Contributions'}</p>
          </div>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link to="/contact" className="btn-primary shadow-glow-sm"><Mail size={16}/><span>Get In Touch</span></Link>
            <Link to="/resume" className="btn-outline"><FileText size={16}/><span>View Resume</span></Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
"""

# ─── project components ──────────────────────────────────────────────────────
files["components/projects/ProjectCard.jsx"] = """import { useState } from 'react';
import { motion } from 'framer-motion';
import { Github, ExternalLink, Info } from 'lucide-react';
import Badge from '../ui/Badge';
import Modal from '../ui/Modal';

const catColor = { web:'primary', ml:'secondary', systems:'tertiary', mobile:'accent' };
const statusColor = { completed:'success', ongoing:'warning', archived:'neutral' };

export default function ProjectCard({ project: p, delay=0 }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}} whileHover={{y:-6,scale:1.01}}
        className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300 cursor-pointer group" onClick={() => setOpen(true)}>
        <div className="relative h-44 overflow-hidden">
          {p.thumbnail ? <img src={p.thumbnail} alt={p.title} loading="lazy" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"/>
            : <div className="h-full bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center"><span className="font-display font-bold text-6xl text-primary/30">{p.title[0]}</span></div>}
          <div className="absolute inset-0 bg-gradient-to-t from-surface-container/90 to-transparent"/>
          <div className="absolute top-3 left-3"><Badge variant={catColor[p.category]||'primary'}>{p.category}</Badge></div>
          {p.featured && <div className="absolute top-3 right-3"><Badge variant="warning">⭐ Featured</Badge></div>}
        </div>
        <div className="p-5 flex flex-col flex-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-display font-semibold text-on-surface">{p.title}</h3>
            <Badge variant={statusColor[p.status]||'neutral'} size="sm">{p.status}</Badge>
          </div>
          <p className="font-body text-sm text-on-surface-variant mb-4 flex-1 line-clamp-2">{p.description}</p>
          <div className="flex flex-wrap gap-1.5 mb-4">{p.tech_stack?.slice(0,4).map(t => <span key={t} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full">{t}</span>)}</div>
          <div className="flex items-center gap-3 border-t border-white/10 pt-3 mt-auto" onClick={e => e.stopPropagation()}>
            {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><Github size={16}/></a>}
            {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="text-on-surface-variant hover:text-primary transition-colors"><ExternalLink size={16}/></a>}
            <button className="ml-auto font-mono text-[10px] uppercase tracking-wider text-primary flex items-center gap-1 hover:text-primary-light transition-colors"><Info size={14}/> Details</button>
          </div>
        </div>
      </motion.div>

      <Modal open={open} onClose={() => setOpen(false)} title={p.title}>
        <div className="space-y-4">
          {p.thumbnail && <img src={p.thumbnail} alt={p.title} className="w-full h-48 object-cover rounded-lg mb-4"/>}
          <div className="flex gap-2 flex-wrap"><Badge variant={catColor[p.category]||'primary'}>{p.category}</Badge><Badge variant={statusColor[p.status]||'neutral'}>{p.status}</Badge></div>
          <p className="font-body text-on-surface-variant">{p.description}</p>
          <div><p className="font-mono text-[10px] uppercase tracking-wider text-primary mb-2">Tech Stack</p><div className="flex flex-wrap gap-2">{p.tech_stack?.map(t => <span key={t} className="font-mono text-xs px-3 py-1 bg-primary/10 text-primary border border-primary/20 rounded-full">{t}</span>)}</div></div>
          <div className="flex gap-3 pt-2">
            {p.github_url && <a href={p.github_url} target="_blank" rel="noopener noreferrer" className="btn-outline flex items-center gap-2 text-sm"><Github size={16}/> View Source</a>}
            {p.live_url && <a href={p.live_url} target="_blank" rel="noopener noreferrer" className="btn-primary flex items-center gap-2 text-sm"><ExternalLink size={16}/> Live Demo</a>}
          </div>
        </div>
      </Modal>
    </>
  );
}
"""

files["components/projects/ProjectFilter.jsx"] = """const filters = ['All', 'Web Dev', 'ML/AI', 'Systems', 'Mobile', 'Other'];
const map = { 'All':'all', 'Web Dev':'web', 'ML/AI':'ml', 'Systems':'systems', 'Mobile':'mobile', 'Other':'other' };

export default function ProjectFilter({ active, onChange }) {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2 mb-8">
      {filters.map(f => (
        <button key={f} onClick={() => onChange(map[f])}
          className={`whitespace-nowrap px-5 py-2 rounded-full font-mono text-[10px] uppercase tracking-wider border transition-all ${active===map[f] ? 'bg-primary/20 text-primary border-primary/40 shadow-glow-sm' : 'bg-white/5 text-on-surface-variant border-white/10 hover:bg-white/10'}`}>
          {f}
        </button>
      ))}
    </div>
  );
}
"""

files["components/certificates/CertificateCard.jsx"] = """import { useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, Download } from 'lucide-react';
import Badge from '../ui/Badge';
import Modal from '../ui/Modal';

const catColor = { 'AI/ML':'secondary', 'Cloud':'primary', 'Web Dev':'tertiary', 'DSA':'warning', 'Core CS':'neutral' };

export default function CertificateCard({ cert: c, delay=0 }) {
  const [open, setOpen] = useState(false);
  const date = c.issue_date ? new Date(c.issue_date).toLocaleDateString('en-US',{month:'short',year:'numeric'}) : '';
  return (
    <>
      <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}} whileHover={{y:-4}}
        className="glass-card rounded-xl overflow-hidden flex flex-col hover:shadow-card transition-all duration-300">
        <div className={`h-1.5 w-full bg-gradient-to-r from-primary to-secondary`}/>
        <div className="p-5 flex flex-col flex-1">
          <div className="flex items-start gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center flex-shrink-0 font-display font-bold text-primary text-sm">{c.issuing_org?.[0]}</div>
            <div className="flex-1 min-w-0">
              <h3 className="font-display font-semibold text-on-surface text-sm leading-tight line-clamp-2">{c.title}</h3>
              <p className="font-mono text-[10px] text-on-surface-variant mt-0.5">{c.issuing_org}</p>
            </div>
            {c.featured && <Badge variant="warning" size="sm">⭐</Badge>}
          </div>
          <div className="flex items-center justify-between mb-3">
            <Badge variant={catColor[c.category]||'primary'} size="sm">{c.category}</Badge>
            {date && <span className="font-mono text-[10px] text-on-surface-variant">{date}</span>}
          </div>
          {c.skills_gained?.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-4">
              {c.skills_gained.slice(0,3).map(s => <span key={s} className="font-mono text-[9px] px-2 py-0.5 bg-secondary/10 text-secondary border border-secondary/20 rounded-full">{s}</span>)}
              {c.skills_gained.length > 3 && <span className="font-mono text-[9px] text-on-surface-variant">+{c.skills_gained.length-3}</span>}
            </div>
          )}
          <div className="flex items-center gap-2 mt-auto border-t border-white/10 pt-3">
            <button onClick={() => setOpen(true)} className="btn-outline py-1.5 px-3 text-[10px] flex-1">View Certificate</button>
            {c.credential_url && <a href={c.credential_url} target="_blank" rel="noopener noreferrer" className="p-2 text-on-surface-variant hover:text-primary transition-colors" title="Verify"><ExternalLink size={14}/></a>}
          </div>
        </div>
      </motion.div>

      <Modal open={open} onClose={() => setOpen(false)} title={c.title}>
        <div className="space-y-4 text-center">
          <div className="w-16 h-16 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto font-display font-bold text-primary text-2xl">{c.issuing_org?.[0]}</div>
          <div><h3 className="font-display font-semibold text-xl text-on-surface">{c.title}</h3><p className="text-on-surface-variant font-mono text-xs mt-1">{c.issuing_org}</p></div>
          <div className="flex justify-center gap-2"><Badge variant={catColor[c.category]||'primary'}>{c.category}</Badge>{date && <Badge variant="neutral">{date}</Badge>}</div>
          {c.skills_gained?.length > 0 && <div className="flex flex-wrap gap-2 justify-center">{c.skills_gained.map(s=><span key={s} className="font-mono text-xs px-3 py-1 bg-secondary/10 text-secondary border border-secondary/20 rounded-full">{s}</span>)}</div>}
          {c.credential_url && <a href={c.credential_url} target="_blank" rel="noopener noreferrer" className="btn-primary mx-auto w-fit"><ExternalLink size={16}/> Verify Certificate</a>}
        </div>
      </Modal>
    </>
  );
}
"""

files["components/research/ResearchCard.jsx"] = """import { useState } from 'react';
import { motion } from 'framer-motion';
import { ExternalLink, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import Badge from '../ui/Badge';

const statusColor = { published:'success', under_review:'warning', preprint:'primary' };
const statusLabel = { published:'Published', under_review:'Under Review', preprint:'Preprint' };

export default function ResearchCard({ paper: p, delay=0 }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay}}
      className="glass-card rounded-xl overflow-hidden flex hover:shadow-card transition-all duration-300">
      <div className="w-1.5 flex-shrink-0 bg-gradient-to-b from-primary to-secondary rounded-l-xl"/>
      <div className="p-6 flex-1">
        <div className="flex flex-wrap items-center gap-3 mb-3">
          <Badge variant={statusColor[p.status]||'neutral'}>{statusLabel[p.status]||p.status}</Badge>
          {p.citations > 0 && <span className="font-mono text-[10px] text-on-surface-variant">{p.citations} citations</span>}
        </div>
        <h3 className="font-display font-semibold text-lg text-on-surface mb-2">{p.title}</h3>
        <p className="font-body text-sm text-on-surface-variant mb-1">{p.authors?.join(', ')}</p>
        <p className="font-mono text-xs text-primary italic mb-3">{p.journal} · {p.date ? new Date(p.date).getFullYear() : ''}</p>
        <div className={`font-body text-sm text-on-surface-variant mb-3 ${!expanded ? 'line-clamp-3' : ''}`}>{p.abstract}</div>
        <button onClick={() => setExpanded(!expanded)} className="font-mono text-[10px] uppercase tracking-wider text-primary flex items-center gap-1 hover:text-primary-light transition-colors mb-3">
          {expanded ? <><ChevronUp size={12}/> Show Less</> : <><ChevronDown size={12}/> Read More</>}
        </button>
        {p.keywords?.length > 0 && <div className="flex flex-wrap gap-1.5 mb-4">{p.keywords.map(k=><span key={k} className="font-mono text-[9px] px-2 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded-full">{k}</span>)}</div>}
        <div className="flex gap-3 flex-wrap border-t border-white/10 pt-3">
          {p.paper_url && <a href={p.paper_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><BookOpen size={14}/> Read Paper</a>}
          {p.arxiv_url && <a href={p.arxiv_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><ExternalLink size={14}/> arXiv</a>}
          {p.doi && <a href={`https://doi.org/${p.doi}`} target="_blank" rel="noopener noreferrer" className="btn-outline py-1.5 px-4 text-[10px]"><ExternalLink size={14}/> DOI</a>}
        </div>
      </div>
    </motion.div>
  );
}
"""

# ─── admin components ─────────────────────────────────────────────────────────
files["components/admin/AdminSidebar.jsx"] = """import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FolderCode, Award, BookOpen, Cpu, Trophy, Briefcase, User, FileText, MessageSquare, LogOut } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const items = [
  { label:'Overview', icon:LayoutDashboard, id:'overview' },
  { label:'Projects', icon:FolderCode, id:'projects' },
  { label:'Certificates', icon:Award, id:'certificates' },
  { label:'Research', icon:BookOpen, id:'research' },
  { label:'Skills', icon:Cpu, id:'skills' },
  { label:'Achievements', icon:Trophy, id:'achievements' },
  { label:'Experience', icon:Briefcase, id:'experience' },
  { label:'Profile', icon:User, id:'profile' },
  { label:'Resume', icon:FileText, id:'resume' },
  { label:'Messages', icon:MessageSquare, id:'messages' },
];

export default function AdminSidebar({ active, setActive, unreadCount=0 }) {
  const { logout, adminName } = useAuthStore();
  return (
    <aside className="w-64 flex-shrink-0 glass-card border-r border-outline-variant/20 flex flex-col h-full">
      <div className="p-6 border-b border-white/10">
        <div className="font-display font-bold text-lg gradient-text">Admin Panel</div>
        <div className="font-mono text-[10px] text-on-surface-variant mt-1">Welcome, {adminName}</div>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        {items.map(item => (
          <button key={item.id} onClick={() => setActive(item.id)}
            className={`w-full flex items-center gap-3 px-6 py-3 text-left transition-all duration-200 font-mono text-[11px] uppercase tracking-wider ${active===item.id ? 'bg-primary/15 text-primary border-r-2 border-primary' : 'text-on-surface-variant hover:bg-white/5 hover:text-primary'}`}>
            <item.icon size={16}/>
            <span>{item.label}</span>
            {item.id==='messages' && unreadCount>0 && <span className="ml-auto bg-primary text-on-primary text-[9px] font-bold px-1.5 py-0.5 rounded-full">{unreadCount}</span>}
          </button>
        ))}
      </nav>
      <button onClick={logout} className="flex items-center gap-3 px-6 py-4 text-on-surface-variant hover:text-error transition-colors border-t border-white/10 font-mono text-[11px] uppercase tracking-wider">
        <LogOut size={16}/> Logout
      </button>
    </aside>
  );
}
"""

def form_template(title, fields_jsx):
    return f"""import {{ useForm }} from 'react-hook-form';
import {{ zodResolver }} from '@hookform/resolvers/zod';
import {{ z }} from 'zod';
import Button from '../ui/Button';

export default function {title}({{ onSubmit, defaultValues }}) {{
  const {{ register, handleSubmit, formState:{{ errors }} }} = useForm({{ defaultValues }});
  const submit = (data) => {{ onSubmit && onSubmit(data); }};
  return (
    <form onSubmit={{handleSubmit(submit)}} className="space-y-4">
{fields_jsx}
      <Button type="submit" variant="primary" className="w-full">Save</Button>
    </form>
  );
}}
"""

files["components/admin/ProjectForm.jsx"] = """import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
import FileUpload from '../ui/FileUpload';
import { useState } from 'react';

export default function ProjectForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  const [file, setFile] = useState(null);
  return (
    <form onSubmit={handleSubmit(d => onSubmit({...d, thumbnail: file}))} className="space-y-4">
      {[['title','Title','text'],['description','Description (short)','text'],['github_url','GitHub URL','url'],['live_url','Live URL (optional)','url']].map(([name,label,type])=>(
        <div key={name}><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">{label}</label>
        <input type={type} {...register(name)} placeholder={label} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/></div>
      ))}
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
        <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['web','ml','systems','mobile','other'].map(c=><option key={c} value={c}>{c}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Status</label>
        <select {...register('status')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['completed','ongoing','archived'].map(s=><option key={s} value={s}>{s}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Thumbnail Image</label><FileUpload onFile={setFile} file={file} accept={{'image/*':[]}} label="Drop project image here"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Project</Button>
    </form>
  );
}
"""

files["components/admin/CertificateForm.jsx"] = """import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
import FileUpload from '../ui/FileUpload';
import { useState } from 'react';
export default function CertificateForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  const [file, setFile] = useState(null);
  return (
    <form onSubmit={handleSubmit(d => onSubmit({...d, thumbnail: file}))} className="space-y-4">
      {[['title','Certificate Title'],['issuing_org','Issuing Organization'],['credential_url','Credential URL (optional)']].map(([name,label])=>(
        <div key={name}><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">{label}</label>
        <input {...register(name)} placeholder={label} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      ))}
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
        <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['AI/ML','Cloud','Web Dev','DSA','Core CS','Other'].map(c=><option key={c}>{c}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Issue Date</label><input type="date" {...register('issue_date')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Certificate Image / PDF</label><FileUpload onFile={setFile} file={file} label="Drop certificate image or PDF"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Certificate</Button>
    </form>
  );
}
"""

files["components/admin/ResearchForm.jsx"] = """import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
export default function ResearchForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Title</label><input {...register('title')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Journal / Conference</label><input {...register('journal')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Abstract</label><textarea {...register('abstract')} rows={4} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 resize-none"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Status</label>
        <select {...register('status')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['preprint','under_review','published'].map(s=><option key={s} value={s}>{s}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">arXiv URL</label><input {...register('arxiv_url')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Research</Button>
    </form>
  );
}
"""

files["components/admin/SkillForm.jsx"] = """import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
export default function SkillForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Skill Name</label><input {...register('name')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
        <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['Frontend','Backend','Database','DevOps','AI/ML','Tools'].map(c=><option key={c}>{c}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Proficiency (0-100)</label><input type="number" min={0} max={100} {...register('proficiency',{valueAsNumber:true})} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Icon (emoji)</label><input {...register('icon')} placeholder="⚛️" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Skill</Button>
    </form>
  );
}
"""

files["components/admin/MessageList.jsx"] = """import { useState } from 'react';
import { ChevronDown, ChevronUp, Check } from 'lucide-react';
import Badge from '../ui/Badge';
export default function MessageList({ messages=[], onMarkRead }) {
  const [expanded, setExpanded] = useState(null);
  return (
    <div className="space-y-3">
      {messages.length === 0 && <div className="text-center py-12 text-on-surface-variant font-mono text-xs">No messages yet.</div>}
      {messages.map(m => (
        <div key={m.id} className={`glass-card rounded-xl overflow-hidden border ${!m.read ? 'border-primary/30' : 'border-white/10'}`}>
          <div className="flex items-center gap-4 p-4 cursor-pointer hover:bg-white/5 transition-colors" onClick={() => setExpanded(expanded===m.id?null:m.id)}>
            {!m.read && <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0"/>}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3"><span className="font-body font-semibold text-on-surface text-sm">{m.name}</span><Badge variant="neutral" size="sm">{m.subject}</Badge></div>
              <span className="font-mono text-[10px] text-on-surface-variant">{m.email} · {m.date}</span>
            </div>
            {expanded===m.id ? <ChevronUp size={16} className="text-on-surface-variant"/> : <ChevronDown size={16} className="text-on-surface-variant"/>}
          </div>
          {expanded===m.id && (
            <div className="px-4 pb-4 border-t border-white/10">
              <p className="font-body text-sm text-on-surface-variant my-3">{m.message}</p>
              {!m.read && <button onClick={() => onMarkRead(m.id)} className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-success hover:text-success/80 transition-colors"><Check size={14}/> Mark as Read</button>}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
"""

# ─── PAGES ────────────────────────────────────────────────────────────────────
files["pages/HomePage.jsx"] = """import { Suspense } from 'react';
import { useProfile } from '../hooks/useProfile';
import HeroSection from '../components/home/HeroSection';
import StatsSection from '../components/home/StatsSection';
import FeaturedProjects from '../components/home/FeaturedProjects';
import SkillsPreview from '../components/home/SkillsPreview';
import CTASection from '../components/home/CTASection';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function HomePage() {
  const { data: profile } = useProfile();
  return (
    <div>
      <HeroSection profile={profile} />
      <StatsSection />
      <FeaturedProjects />
      <SkillsPreview />
      <CTASection profile={profile} />
    </div>
  );
}
"""

files["pages/ProjectsPage.jsx"] = """import { useState } from 'react';
import { motion } from 'framer-motion';
import { Home, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useProjects } from '../hooks/useProjects';
import ProjectCard from '../components/projects/ProjectCard';
import ProjectFilter from '../components/projects/ProjectFilter';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function ProjectsPage() {
  const [cat, setCat] = useState('all');
  const { data: projects, isLoading } = useProjects(cat !== 'all' ? { category: cat } : {});
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="glass-card rounded-xl p-8 mb-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-grid-pattern bg-grid-sm opacity-30"/>
          <div className="relative z-10">
            <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3">
              <Link to="/" className="hover:text-primary transition-colors flex items-center gap-1"><Home size={12}/>Home</Link>
              <ChevronRight size={12}/><span className="text-primary">Projects</span>
            </nav>
            <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">My Projects</h1>
            <p className="font-body text-on-surface-variant">Engineering projects from systems design to ML models.</p>
          </div>
        </div>
        <ProjectFilter active={cat} onChange={setCat} />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? [1,2,3,4,5,6].map(i=><SkeletonCard key={i}/>) : projects?.map((p,i)=><ProjectCard key={p.id} project={p} delay={i*0.05}/>)}
        </div>
        {!isLoading && projects?.length===0 && <div className="text-center py-20 text-on-surface-variant font-mono text-xs">No projects in this category.</div>}
      </div>
    </div>
  );
}
"""

files["pages/CertificatesPage.jsx"] = """import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Home, ChevronRight } from 'lucide-react';
import { useCertificates } from '../hooks/useCertificates';
import CertificateCard from '../components/certificates/CertificateCard';
import SkeletonCard from '../components/ui/SkeletonCard';

const cats = ['All', 'Cloud', 'AI/ML', 'Web Dev', 'DSA', 'Core CS', 'Other'];

export default function CertificatesPage() {
  const [cat, setCat] = useState('All');
  const { data: certs, isLoading } = useCertificates(cat !== 'All' ? { category: cat } : {});
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12">
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Certificates</span></nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Certifications & Credentials</h1>
          <p className="font-body text-on-surface-variant">Verified achievements from world-class platforms.</p>
        </div>
        {/* Filter */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 mb-8">
          {cats.map(c=><button key={c} onClick={()=>setCat(c)} className={`whitespace-nowrap px-5 py-2 rounded-full font-mono text-[10px] uppercase tracking-wider border transition-all ${cat===c?'bg-primary/20 text-primary border-primary/40 shadow-glow-sm':'bg-white/5 text-on-surface-variant border-white/10 hover:bg-white/10'}`}>{c}</button>)}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? [1,2,3,4,5,6].map(i=><SkeletonCard key={i}/>) : certs?.map((c,i)=><CertificateCard key={c.id} cert={c} delay={i*0.05}/>)}
        </div>
      </div>
    </div>
  );
}
"""

files["pages/ResearchPage.jsx"] = """import { Link } from 'react-router-dom';
import { Home, ChevronRight, Rocket } from 'lucide-react';
import { useResearch } from '../hooks/useResearch';
import ResearchCard from '../components/research/ResearchCard';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function ResearchPage() {
  const { data: papers, isLoading } = useResearch();
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-4xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12">
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Research</span></nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Research & Publications</h1>
          <p className="font-body text-on-surface-variant">Academic work, papers, and contributions to the field.</p>
        </div>
        <div className="space-y-6">
          {isLoading ? [1,2].map(i=><SkeletonCard key={i} height="h-48"/>) : papers?.length === 0 ? (
            <div className="text-center py-20"><Rocket size={48} className="mx-auto text-on-surface-variant/30 mb-4"/><p className="font-mono text-xs text-on-surface-variant uppercase tracking-wider">No publications yet. Research coming soon!</p></div>
          ) : papers?.map((p,i)=><ResearchCard key={p.id} paper={p} delay={i*0.1}/>)}
        </div>
      </div>
    </div>
  );
}
"""

files["pages/SkillsPage.jsx"] = """import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion, useInView } from 'framer-motion';
import { Home, ChevronRight } from 'lucide-react';
import { useSkills } from '../hooks/useSkills';
import SkeletonCard from '../components/ui/SkeletonCard';

function SkillBar({ skill }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  return (
    <div ref={ref} className="space-y-1">
      <div className="flex justify-between font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">
        <span>{skill.icon} {skill.name}</span><span className="text-primary">{skill.proficiency}%</span>
      </div>
      <div className="h-2 bg-surface-container rounded-full overflow-hidden">
        <motion.div className="h-full bg-gradient-to-r from-primary to-secondary rounded-full" initial={{width:0}} animate={{width: inView ? `${skill.proficiency}%` : 0}} transition={{duration:1.2, ease:'easeOut'}}/>
      </div>
    </div>
  );
}

export default function SkillsPage() {
  const { data: skills, isLoading } = useSkills();
  const categories = skills ? [...new Set(skills.map(s=>s.category))] : [];
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="glass-card rounded-xl p-8 mb-12">
          <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-3"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">Skills</span></nav>
          <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-2">Skills & Technologies</h1>
          <p className="font-body text-on-surface-variant">Technologies I build with daily.</p>
        </div>
        {isLoading ? <div className="grid grid-cols-2 md:grid-cols-4 gap-6">{[1,2,3,4,5,6,7,8].map(i=><SkeletonCard key={i} height="h-24"/>)}</div> : (
          <>
            {categories.map(cat => (
              <div key={cat} className="mb-12">
                <h2 className="font-display font-bold text-2xl gradient-text mb-6">{cat}</h2>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  {skills.filter(s=>s.category===cat).map((s,i)=>(
                    <motion.div key={s.id} initial={{opacity:0,y:10}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.05}} whileHover={{y:-4,scale:1.05}}
                      className="glass-card rounded-xl p-4 flex flex-col items-center text-center gap-2 cursor-pointer hover:border-primary/30 hover:shadow-glow-sm transition-all">
                      <span className="text-3xl">{s.icon}</span>
                      <span className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">{s.name}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            ))}
            <div className="mt-12">
              <h2 className="font-display font-bold text-2xl gradient-text mb-6">Proficiency Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                {[...skills].sort((a,b)=>b.proficiency-a.proficiency).map(s=><SkillBar key={s.id} skill={s}/>)}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
"""

files["pages/AboutPage.jsx"] = """import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Home, ChevronRight, MapPin, Download, Mail, GraduationCap } from 'lucide-react';
import { useProfile } from '../hooks/useProfile';
import Badge from '../components/ui/Badge';

const interests = [
  { icon:'🌐', title:'Web Development', desc:'Full-stack apps with React & Node.js' },
  { icon:'🧠', title:'Machine Learning', desc:'Deep learning and model deployment' },
  { icon:'⚙️', title:'System Design', desc:'Scalable distributed systems' },
  { icon:'📖', title:'Open Source', desc:'Contributing to OSS projects' },
  { icon:'🏆', title:'Competitive Programming', desc:'LeetCode, Codeforces' },
  { icon:'🔬', title:'Research', desc:'AI & systems research' },
];

export default function AboutPage() {
  const { data: profile } = useProfile();
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        {/* Intro */}
        <div className="glass-card rounded-xl p-8 mb-12 grid grid-cols-1 md:grid-cols-5 gap-8 items-center">
          <div className="md:col-span-2 flex justify-center">
            <div className="w-64 h-64 rounded-xl overflow-hidden border-2 border-primary/30 shadow-glow">
              <img src={profile?.profile_image_url} alt={profile?.name} className="w-full h-full object-cover"/>
            </div>
          </div>
          <div className="md:col-span-3 space-y-4">
            <nav className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-on-surface-variant"><Link to="/" className="hover:text-primary flex items-center gap-1"><Home size={12}/>Home</Link><ChevronRight size={12}/><span className="text-primary">About</span></nav>
            <h1 className="font-display font-bold text-3xl md:text-4xl text-on-surface">{profile?.name || 'Pradipta Chandra Giri'}</h1>
            <p className="font-mono text-sm text-primary">Full Stack Developer | BTech CSE</p>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse"/>
              <Badge variant="success">Open to Work</Badge>
            </div>
            <p className="font-body text-on-surface-variant">{profile?.bio || 'Passionate CS undergrad building scalable systems.'}</p>
            <div className="flex items-center gap-2 font-mono text-xs text-on-surface-variant"><MapPin size={14}/>{profile?.location || 'Bhubaneswar, Odisha, India'}</div>
            <div className="flex gap-3 flex-wrap">
              <a href={profile?.resume_url||'#'} className="btn-primary py-2 px-5"><Download size={14}/>Download Resume</a>
              <Link to="/contact" className="btn-outline py-2 px-5"><Mail size={14}/>Contact Me</Link>
            </div>
          </div>
        </div>

        {/* Education */}
        <div className="mb-12">
          <h2 className="font-display font-bold text-2xl gradient-text mb-6 flex items-center gap-2"><GraduationCap size={24}/>Education</h2>
          <div className="glass-card rounded-xl p-6 border-l-4 border-primary">
            <div className="flex flex-col md:flex-row md:justify-between md:items-start mb-2">
              <h3 className="font-display font-semibold text-lg text-on-surface">{profile?.degree || 'B.Tech Computer Science & Engineering'}</h3>
              <span className="font-mono text-xs text-primary">2021 — {profile?.graduation_year || 2025}</span>
            </div>
            <p className="font-body text-on-surface-variant mb-3">{profile?.university || 'Institute of Technology & Engineering'}</p>
            <Badge variant="success">CGPA: {profile?.cgpa || '8.9'}/10</Badge>
          </div>
        </div>

        {/* Areas of Interest */}
        <div className="mb-12">
          <h2 className="font-display font-bold text-2xl gradient-text mb-6">Areas of Interest</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {interests.map((item,i)=>(
              <motion.div key={item.title} initial={{opacity:0,y:10}} whileInView={{opacity:1,y:0}} viewport={{once:true}} transition={{delay:i*0.05}} whileHover={{y:-4}}
                className="glass-card rounded-xl p-4 text-center hover:border-primary/30 hover:shadow-glow-sm transition-all">
                <div className="text-3xl mb-2">{item.icon}</div>
                <div className="font-display font-semibold text-sm text-on-surface mb-1">{item.title}</div>
                <div className="font-body text-[11px] text-on-surface-variant">{item.desc}</div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Looking For */}
        <motion.div initial={{opacity:0,y:20}} whileInView={{opacity:1,y:0}} viewport={{once:true}} className="glass-card rounded-xl p-8 border border-primary/20">
          <h2 className="font-display font-bold text-2xl gradient-text mb-3">What I'm Looking For</h2>
          <p className="font-body text-on-surface-variant mb-4">Targeting top-tier tech companies and impactful research opportunities.</p>
          <ul className="space-y-2">
            {['🎯 A fast-learning environment with challenging problems','🌍 Real-world impact and production systems','🤝 Collaborative engineering teams','📈 Growth in both technical depth and breadth'].map(b=>(
              <li key={b} className="flex items-center gap-2 font-body text-on-surface-variant text-sm"><span className="text-lg">{b.slice(0,2)}</span>{b.slice(2)}</li>
            ))}
          </ul>
        </motion.div>
      </div>
    </div>
  );
}
"""

files["pages/ResumePage.jsx"] = """import { useProfile } from '../hooks/useProfile';
import { Download, ExternalLink, Printer } from 'lucide-react';
import { useSkills } from '../hooks/useSkills';

export default function ResumePage() {
  const { data: profile } = useProfile();
  const { data: skills } = useSkills();
  const topSkills = skills?.slice(0,10).map(s=>s.name).join(', ') || 'React, Node.js, Python, PostgreSQL, Docker';
  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-4xl mx-auto">
        {/* Action Bar */}
        <div className="glass-card rounded-xl p-4 mb-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center border border-primary/20"><span className="text-primary text-lg">📄</span></div>
            <div><div className="font-mono text-sm text-on-surface font-semibold">Resume.pdf</div><div className="font-mono text-[10px] text-on-surface-variant">Last updated: June 2024</div></div>
          </div>
          <div className="flex gap-3">
            <a href={profile?.resume_url || '#'} download className="btn-primary py-2 px-5"><Download size={16}/>Download PDF</a>
            <a href={profile?.resume_url || '#'} target="_blank" rel="noopener noreferrer" className="btn-outline py-2 px-5"><ExternalLink size={16}/>Open Tab</a>
            <button onClick={() => window.print()} className="btn-outline py-2 px-5"><Printer size={16}/>Print</button>
          </div>
        </div>

        {/* Resume Content */}
        <div id="resume-print" className="glass-card rounded-xl p-8 md:p-12 print:bg-white print:shadow-none print:text-black space-y-8">
          {/* Header */}
          <div className="text-center border-b border-white/10 pb-6 print:border-gray-300">
            <h1 className="font-display font-bold text-3xl text-on-surface print:text-black">{profile?.name || 'Pradipta Chandra Giri'}</h1>
            <p className="font-mono text-sm text-primary print:text-indigo-600 mt-1">{profile?.degree || 'B.Tech CSE'} | {profile?.university || 'ITE'}</p>
            <div className="flex justify-center gap-4 mt-3 flex-wrap">
              {[profile?.email, profile?.github && 'GitHub', profile?.linkedin && 'LinkedIn'].filter(Boolean).map(l=><span key={l} className="font-mono text-xs text-on-surface-variant print:text-gray-600">{l}</span>)}
            </div>
          </div>

          {/* Sections */}
          {[['OBJECTIVE', <p className="font-body text-on-surface-variant print:text-gray-700">{profile?.bio || 'Passionate CS engineer seeking impactful roles.'}</p>],
            ['EDUCATION', <div><div className="flex justify-between"><span className="font-body font-semibold text-on-surface print:text-black">{profile?.degree || 'B.Tech CSE'}</span><span className="font-mono text-xs text-primary print:text-indigo-600">2021—{profile?.graduation_year||2025}</span></div><p className="font-body text-sm text-on-surface-variant print:text-gray-700">{profile?.university} · CGPA {profile?.cgpa}</p></div>],
            ['SKILLS', <p className="font-mono text-sm text-on-surface-variant print:text-gray-700">{topSkills}</p>],
            ['AVAILABLE FOR', <p className="font-body text-on-surface-variant print:text-gray-700">{profile?.available_for || 'SDE Internships, Research Roles, Open Source'}</p>],
          ].map(([title, content]) => (
            <div key={title}>
              <h2 className="font-display font-bold text-sm uppercase tracking-widest text-primary print:text-indigo-600 mb-2 border-b border-primary/20 print:border-indigo-200 pb-1">{title}</h2>
              {content}
            </div>
          ))}
        </div>
      </div>
      <style>{`@media print { body { background: white !important; } .glass-card { background: white !important; box-shadow: none !important; } nav, header, footer { display: none !important; } }`}</style>
    </div>
  );
}
"""

files["pages/ContactPage.jsx"] = """import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';
import { Mail, Phone, MapPin, Github, Linkedin, Twitter, Code2, CheckCircle, Send, Loader2 } from 'lucide-react';
import { submitContact } from '../api/contact';
import { useProfile } from '../hooks/useProfile';
import Badge from '../components/ui/Badge';

const schema = z.object({
  firstName: z.string().min(2, 'Min 2 characters'),
  lastName: z.string().min(2, 'Min 2 characters'),
  email: z.string().email('Invalid email'),
  subject: z.string(),
  message: z.string().min(10, 'Min 10 characters'),
});

export default function ContactPage() {
  const { data: profile } = useProfile();
  const [success, setSuccess] = useState(false);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = async (data) => {
    try {
      await submitContact(data);
      setSuccess(true);
    } catch {
      toast.error('Failed to send. Please try again.');
    }
  };

  const inputClass = "w-full bg-background border border-outline-variant/40 rounded-lg px-4 py-3 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 transition-all placeholder:text-on-surface-variant/40";
  const errClass = "text-error font-mono text-[10px] mt-1";

  const contacts = [
    { icon: Mail, label: profile?.email || 'pradipta@example.com', href: `mailto:${profile?.email||'pradipta@example.com'}` },
    { icon: MapPin, label: profile?.location || 'Bhubaneswar, Odisha', href: '#' },
    { icon: Github, label: 'GitHub', href: profile?.github||'#' },
    { icon: Linkedin, label: 'LinkedIn', href: profile?.linkedin||'#' },
  ];

  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
          {/* Left */}
          <div>
            <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-3">Let's <span className="gradient-text">Connect</span></h1>
            <p className="font-body text-on-surface-variant mb-8">Open to internship opportunities, research collaborations, and open source contributions.</p>
            <div className="space-y-4 mb-8">
              {contacts.map(c => (
                <a key={c.label} href={c.href} target={c.href.startsWith('http')?'_blank':undefined} rel="noopener noreferrer"
                  className="flex items-center gap-4 glass-card rounded-xl p-4 hover:border-primary/30 hover:shadow-glow-sm transition-all group">
                  <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center group-hover:bg-primary/20 transition-colors"><c.icon size={18} className="text-primary"/></div>
                  <span className="font-body text-sm text-on-surface-variant group-hover:text-on-surface transition-colors">{c.label}</span>
                </a>
              ))}
            </div>
            <motion.div whileInView={{opacity:1,y:0}} initial={{opacity:0,y:10}} viewport={{once:true}} className="glass-card rounded-xl p-6 border border-success/20">
              <div className="flex items-center gap-3 mb-2"><span className="w-2.5 h-2.5 rounded-full bg-success animate-pulse"/><span className="font-mono text-[11px] uppercase tracking-wider text-success">Available for Hire</span></div>
              <p className="font-mono text-xs text-on-surface-variant">{profile?.available_for || 'SDE Internships, Research Roles, Open Source'}</p>
            </motion.div>
          </div>

          {/* Right - Form */}
          <div className="glass-card rounded-xl p-6 md:p-8 sticky top-24">
            <AnimatePresence mode="wait">
              {success ? (
                <motion.div key="success" initial={{opacity:0,scale:0.9}} animate={{opacity:1,scale:1}} exit={{opacity:0}} className="flex flex-col items-center text-center py-10 gap-4">
                  <motion.div initial={{scale:0}} animate={{scale:1}} transition={{type:'spring',delay:0.1}}><CheckCircle size={64} className="text-success"/></motion.div>
                  <h3 className="font-display font-bold text-xl text-on-surface">Message Sent!</h3>
                  <p className="font-mono text-xs text-on-surface-variant">I'll reply within 24 hours.</p>
                  <button onClick={() => { setSuccess(false); reset(); }} className="btn-outline py-2 px-6 mt-2">Send Another</button>
                </motion.div>
              ) : (
                <motion.form key="form" onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                  <h2 className="font-display font-semibold text-xl text-on-surface mb-4">Send a Message</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div><input {...register('firstName')} placeholder="First Name" className={inputClass}/>{errors.firstName && <p className={errClass}>{errors.firstName.message}</p>}</div>
                    <div><input {...register('lastName')} placeholder="Last Name" className={inputClass}/>{errors.lastName && <p className={errClass}>{errors.lastName.message}</p>}</div>
                  </div>
                  <div><input {...register('email')} type="email" placeholder="Email" className={inputClass}/>{errors.email && <p className={errClass}>{errors.email.message}</p>}</div>
                  <select {...register('subject')} className={inputClass}>
                    {['Job Opportunity','Collaboration','General Inquiry','Other'].map(o=><option key={o} value={o}>{o}</option>)}
                  </select>
                  <div><textarea {...register('message')} placeholder="Your message..." rows={5} className={`${inputClass} resize-none`}/>{errors.message && <p className={errClass}>{errors.message.message}</p>}</div>
                  <button type="submit" disabled={isSubmitting} className="btn-primary w-full justify-center shadow-glow-sm">
                    {isSubmitting ? <><Loader2 size={16} className="animate-spin"/>Sending...</> : <><Send size={16}/>Send Message</>}
                  </button>
                </motion.form>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
"""

files["pages/AdminLoginPage.jsx"] = """import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Eye, EyeOff, Loader2, Lock } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password required'),
});

const DEMO = { email: 'admin@portfolio.local', password: 'Admin@1234' };

export default function AdminLoginPage() {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [showPass, setShowPass] = useState(false);
  const [shake, setShake] = useState(false);
  const [error, setError] = useState('');
  const { register, handleSubmit, formState: { isSubmitting } } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = async ({ email, password }) => {
    setError('');
    await new Promise(r => setTimeout(r, 900));
    if (email === DEMO.email && password === DEMO.password) {
      login(btoa(email + ':' + Date.now()), 'Admin');
      navigate('/admin/dashboard');
    } else {
      setError('Invalid credentials. Access denied.');
      setShake(true);
      setTimeout(() => setShake(false), 600);
    }
  };

  const inputClass = "w-full bg-surface-container border border-outline-variant/40 rounded-xl px-4 py-3 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 transition-all placeholder:text-on-surface-variant/40";

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-5 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl pointer-events-none"/>
      <motion.div
        animate={shake ? { x: [-8, 8, -6, 6, -4, 4, 0] } : {}}
        transition={{ duration: 0.45 }}
        className="w-full max-w-sm">
        <div className="glass-card rounded-xl overflow-hidden border border-white/10 shadow-card">
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"/>
          <div className="p-8">
            <div className="flex flex-col items-center text-center mb-8">
              <div className="w-16 h-16 rounded-full bg-surface-container border border-outline-variant/40 flex items-center justify-center mb-4 shadow-glow">
                <ShieldCheck size={28} className="text-primary"/>
              </div>
              <h1 className="font-display font-bold text-2xl text-on-surface">SYSTEM_ADMIN</h1>
              <p className="font-mono text-xs text-on-surface-variant mt-1">Authenticate to access command center.</p>
              <p className="font-mono text-[10px] text-primary/60 mt-2">Demo: admin@portfolio.local / Admin@1234</p>
            </div>
            {error && <motion.div initial={{opacity:0,y:-4}} animate={{opacity:1,y:0}} className="mb-4 p-3 rounded-lg bg-error/10 border border-error/30 text-error font-mono text-xs text-center">{error}</motion.div>}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Admin Email</label>
                <input type="email" {...register('email')} placeholder="admin@system.local" className={inputClass}/>
              </div>
              <div>
                <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Passcode</label>
                <div className="relative">
                  <input type={showPass ? 'text' : 'password'} {...register('password')} placeholder="••••••••" className={inputClass}/>
                  <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant hover:text-primary transition-colors">
                    {showPass ? <EyeOff size={16}/> : <Eye size={16}/>}
                  </button>
                </div>
              </div>
              <button type="submit" disabled={isSubmitting} className="btn-primary w-full justify-center mt-2 py-3 shadow-glow-sm">
                {isSubmitting ? <><Loader2 size={16} className="animate-spin"/>Authenticating...</> : <><Lock size={16}/>Initialize Session</>}
              </button>
            </form>
            <div className="mt-6 text-center flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse"/>
              <span className="font-mono text-[10px] text-on-surface-variant/50 uppercase tracking-widest">Secure Connection Verified</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
"""

files["pages/AdminDashboardPage.jsx"] = """import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Plus, Trash2, LayoutDashboard, FolderCode, Award, BookOpen, Cpu, MessageSquare } from 'lucide-react';
import toast from 'react-hot-toast';
import AdminSidebar from '../components/admin/AdminSidebar';
import ProjectForm from '../components/admin/ProjectForm';
import CertificateForm from '../components/admin/CertificateForm';
import ResearchForm from '../components/admin/ResearchForm';
import SkillForm from '../components/admin/SkillForm';
import MessageList from '../components/admin/MessageList';
import Modal from '../components/ui/Modal';
import Badge from '../components/ui/Badge';
import { getProjects, createProject, deleteProject } from '../api/projects';
import { getCertificates, createCertificate, deleteCertificate } from '../api/certificates';
import { getResearch, createResearch, deleteResearch } from '../api/research';
import { getSkills, createSkill, deleteSkill } from '../api/skills';
import { getMessages, markRead } from '../api/contact';

const stats = [
  { label:'Projects', icon:FolderCode, key:'projects', color:'text-primary' },
  { label:'Certificates', icon:Award, key:'certificates', color:'text-tertiary' },
  { label:'Research', icon:BookOpen, key:'research', color:'text-secondary' },
  { label:'Messages', icon:MessageSquare, key:'messages', color:'text-success' },
];

function DataTable({ data=[], columns, onDelete, entityKey }) {
  const qc = useQueryClient();
  const del = useMutation({ mutationFn: onDelete, onSuccess: () => { qc.invalidateQueries([entityKey]); toast.success('Deleted!'); } });
  return (
    <div className="space-y-2 mt-4">
      {data.map(item => (
        <div key={item.id} className="glass-card rounded-xl p-4 flex items-center justify-between hover:border-outline-variant/40 transition-all">
          <div className="flex-1 min-w-0">
            {columns.map(col => (
              <div key={col.key} className={col.primary ? 'font-body font-semibold text-on-surface text-sm' : 'font-mono text-[10px] text-on-surface-variant mt-0.5'}>{item[col.key] ?? ''}</div>
            ))}
          </div>
          <button onClick={() => { if(window.confirm(`Delete "${item[columns[0].key]}"?`)) del.mutate(item.id); }} className="p-2 text-on-surface-variant hover:text-error transition-colors ml-4"><Trash2 size={16}/></button>
        </div>
      ))}
    </div>
  );
}

export default function AdminDashboardPage() {
  const [active, setActive] = useState('overview');
  const [modal, setModal] = useState(false);
  const qc = useQueryClient();

  const projects = useQuery({ queryKey:['projects'], queryFn: getProjects });
  const certificates = useQuery({ queryKey:['certificates'], queryFn: getCertificates });
  const research = useQuery({ queryKey:['research'], queryFn: getResearch });
  const skills = useQuery({ queryKey:['skills'], queryFn: getSkills });
  const messages = useQuery({ queryKey:['messages'], queryFn: getMessages });

  const unread = messages.data?.filter(m=>!m.read).length || 0;
  const counts = { projects: projects.data?.length||0, certificates: certificates.data?.length||0, research: research.data?.length||0, messages: messages.data?.length||0 };

  const addMutation = (fn, key) => useMutation({ mutationFn: fn, onSuccess: () => { qc.invalidateQueries([key]); setModal(false); toast.success('Added!'); } });
  const addProject = addMutation(createProject, 'projects');
  const addCert = addMutation(createCertificate, 'certificates');
  const addResearch = addMutation(createResearch, 'research');
  const addSkill = addMutation(createSkill, 'skills');
  const markReadMut = useMutation({ mutationFn: markRead, onSuccess: () => qc.invalidateQueries(['messages']) });

  const sections = {
    overview: () => (
      <div>
        <h2 className="font-display font-bold text-2xl text-on-surface mb-6">Overview</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map(s=>(
            <motion.div key={s.key} whileHover={{y:-2}} className="glass-card rounded-xl p-5 flex flex-col items-center text-center gap-2">
              <s.icon size={24} className={s.color}/>
              <div className={`font-display font-bold text-3xl ${s.color}`}>{counts[s.key]}</div>
              <div className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    ),
    projects: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Projects</h2>
        <button onClick={() => setModal('project')} className="btn-primary py-2 px-4"><Plus size={16}/>Add Project</button>
      </div>
      <DataTable data={projects.data||[]} columns={[{key:'title',primary:true},{key:'category'},{key:'status'}]} onDelete={deleteProject} entityKey="projects"/>
      <Modal open={modal==='project'} onClose={() => setModal(false)} title="Add Project"><ProjectForm onSubmit={d => addProject.mutate(d)}/></Modal>
    </div>),
    certificates: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Certificates</h2>
        <button onClick={() => setModal('cert')} className="btn-primary py-2 px-4"><Plus size={16}/>Add Certificate</button>
      </div>
      <DataTable data={certificates.data||[]} columns={[{key:'title',primary:true},{key:'issuing_org'},{key:'category'}]} onDelete={deleteCertificate} entityKey="certificates"/>
      <Modal open={modal==='cert'} onClose={() => setModal(false)} title="Add Certificate"><CertificateForm onSubmit={d => addCert.mutate(d)}/></Modal>
    </div>),
    research: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Research Papers</h2>
        <button onClick={() => setModal('research')} className="btn-primary py-2 px-4"><Plus size={16}/>Add Paper</button>
      </div>
      <DataTable data={research.data||[]} columns={[{key:'title',primary:true},{key:'journal'},{key:'status'}]} onDelete={deleteResearch} entityKey="research"/>
      <Modal open={modal==='research'} onClose={() => setModal(false)} title="Add Research Paper"><ResearchForm onSubmit={d => addResearch.mutate(d)}/></Modal>
    </div>),
    skills: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Skills</h2>
        <button onClick={() => setModal('skill')} className="btn-primary py-2 px-4"><Plus size={16}/>Add Skill</button>
      </div>
      <DataTable data={skills.data||[]} columns={[{key:'name',primary:true},{key:'category'},{key:'proficiency'}]} onDelete={deleteSkill} entityKey="skills"/>
      <Modal open={modal==='skill'} onClose={() => setModal(false)} title="Add Skill"><SkillForm onSubmit={d => addSkill.mutate(d)}/></Modal>
    </div>),
    messages: () => (<div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="font-display font-bold text-2xl text-on-surface">Messages</h2>
        {unread > 0 && <Badge variant="primary">{unread} unread</Badge>}
      </div>
      <MessageList messages={messages.data||[]} onMarkRead={id => markReadMut.mutate(id)}/>
    </div>),
  };

  const ActiveSection = sections[active] || sections.overview;

  return (
    <div className="min-h-screen bg-background flex">
      <AdminSidebar active={active} setActive={setActive} unreadCount={unread}/>
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="h-16 border-b border-outline-variant/20 flex items-center px-8 glass-card rounded-none">
          <h1 className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant">Admin Dashboard</h1>
          <div className="ml-auto flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-success animate-pulse"/><span className="font-mono text-[10px] text-on-surface-variant">System Online</span></div>
        </div>
        <div className="flex-1 overflow-y-auto p-8">
          <motion.div key={active} initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} transition={{duration:0.2}}>
            <ActiveSection/>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
"""

# ─── Write all files ───────────────────────────────────────────────────────────
for rel_path, content in files.items():
    abs_path = os.path.normpath(os.path.join(ROOT, rel_path))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  CREATED: {rel_path}")

print(f"\n✅ Generated {len(files)} files successfully!")
