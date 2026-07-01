import api from './axios';
const MOCK = [
  { id:1, company:'TechNova Solutions', role:'Software Engineering Intern', start_date:'2024-05', end_date:null, current:true, description:['Engineered scalable microservices using Node.js and Docker, reducing API latency by 30%','Implemented CI/CD pipelines via GitHub Actions'] },
  { id:2, company:'Open Source (CNCF)', role:'GSoC Contributor', start_date:'2024-06', end_date:'2024-09', current:false, description:['Contributed to a CNCF project, merged 12 PRs','Implemented distributed tracing module'] },
];
export const getExperience = async () => {
  try { return (await api.get('/experience')).data; } catch { return MOCK; }
};
export const createExperience = (data) => api.post('/experience', data);
export const updateExperience = (id, data) => api.put(`/experience/${id}`, data);
export const deleteExperience = (id) => api.delete(`/experience/${id}`);
