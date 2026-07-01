import api from './axios';
const MOCK = [
  { id:1, title:'LeetCode 1800+ Rating', description:'Top 5% globally in competitive programming', date:'2024', icon:'🏆' },
  { id:2, title:'Smart India Hackathon Finalist', description:'National-level hackathon, Top 20 teams', date:'2023', icon:'🥇' },
  { id:3, title:'Google Summer of Code', description:'Selected contributor to an open-source org', date:'2024', icon:'🌟' },
];
export const getAchievements = async () => {
  try { return (await api.get('/achievements')).data; } catch { return MOCK; }
};
export const createAchievement = (data) => api.post('/achievements', data);
export const updateAchievement = (id, data) => api.put(`/achievements/${id}`, data);
export const deleteAchievement = (id) => api.delete(`/achievements/${id}`);
