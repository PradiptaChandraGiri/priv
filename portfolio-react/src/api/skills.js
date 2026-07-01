import api from './axios';

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
  try { const r = await api.get('/skills'); return r.data?.data || r.data; }
  catch { return MOCK; }
};
export const createSkill = (data) => api.post('/skills', data);
export const updateSkill = (id, data) => api.put(`/skills/${id}`, data);
export const deleteSkill = (id) => api.delete(`/skills/${id}`);
