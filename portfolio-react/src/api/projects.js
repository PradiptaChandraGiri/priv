import api from './axios';

const MOCK = [
  { id: 1, title: 'CampusBazaar', category: 'web', description: 'Student-exclusive marketplace for VSSUT campus — buy & sell books, electronics, and essentials with 0% commission and direct WhatsApp contact.', tech_stack: ['React', 'Firebase', 'JavaScript', 'Vercel'], github_url: 'https://github.com/PradiptaChandraGiri/campusbazaar', live_url: 'https://vssut-campusbazar.vercel.app', featured: true, status: 'completed', thumbnail: null },
  { id: 2, title: 'DRRMS — Disaster Relief System', category: 'web', description: 'Centralized disaster relief management platform to track victims, volunteers, donations, and resource distribution. Built as a Database Engineering project.', tech_stack: ['React', 'Node.js', 'MySQL', 'Express.js'], github_url: 'https://github.com/PradiptaChandraGiri/DRRMS-Database-Project', live_url: null, featured: false, status: 'completed', thumbnail: null },
  { id: 3, title: 'SkySenseAI', category: 'ml', description: 'AI-powered environmental prediction platform using machine learning models and Flask backend with an interactive web dashboard for intelligent forecasting.', tech_stack: ['Python', 'Flask', 'Scikit-learn', 'JavaScript'], github_url: 'https://github.com/PradiptaChandraGiri', live_url: null, featured: true, status: 'completed', thumbnail: null },
  { id: 4, title: 'DailyAssist AI', category: 'ml', description: 'Desktop productivity assistant built with Python and Tkinter. Manages daily tasks, reminders, smart notifications, and AI-assisted productivity tracking.', tech_stack: ['Python', 'Tkinter', 'Plyer', 'JSON'], github_url: 'https://github.com/PradiptaChandraGiri', live_url: null, featured: false, status: 'completed', thumbnail: null },
  { id: 5, title: 'DCSM — Digital Complaint System', category: 'web', description: 'Digital complaint management system for streamlined grievance submission, tracking, and resolution with role-based access control.', tech_stack: ['React', 'Node.js', 'MySQL'], github_url: 'https://github.com/PradiptaChandraGiri/DCSM-Digital-Complaint-Managment-System', live_url: null, featured: false, status: 'completed', thumbnail: null },
  { id: 6, title: 'GenAI Toolbox', category: 'ml', description: 'A collection of Generative AI tools and utilities built for practical use cases including text generation, summarization, and AI-powered automation.', tech_stack: ['Python', 'GenAI', 'Flask'], github_url: 'https://github.com/PradiptaChandraGiri/genai-toolbox', live_url: null, featured: false, status: 'completed', thumbnail: null }
];

export const getProjects = async (params) => {
  try { const r = await api.get('/projects', { params }); return r.data?.data || r.data; }
  catch { 
    if (params?.featured) return MOCK.filter(p => p.featured);
    if (params?.category && params.category !== 'all') return MOCK.filter(p => p.category === params.category);
    return MOCK;
  }
};
export const createProject = (data) => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, val]) => {
    if (key === 'thumbnail' && val) {
      formData.append('thumbnail', val);
    } else if (val !== undefined && val !== null) {
      formData.append(key, val);
    }
  });
  return api.post('/projects', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const updateProject = (id, data) => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, val]) => {
    if (key === 'thumbnail' && val) {
      formData.append('thumbnail', val);
    } else if (val !== undefined && val !== null) {
      formData.append(key, val);
    }
  });
  return api.put(`/projects/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};
export const deleteProject = (id) => api.delete(`/projects/${id}`);
