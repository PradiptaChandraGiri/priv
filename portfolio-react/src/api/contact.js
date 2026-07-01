import api from './axios';
export const submitContact = (data) => api.post('/contact', data);
export const getMessages = async () => {
  try { const r = await api.get('/messages'); return r.data?.data || r.data; } catch { return [
    { id:1, name:'Jane Doe', email:'jane@company.com', subject:'Job Opportunity', message:'Hi, we have an exciting SDE role at our startup...', read:false, date:'2024-06-20' },
    { id:2, name:'Prof. Smith', email:'smith@university.edu', subject:'Collaboration', message:'I came across your ML research and would like to collaborate...', read:true, date:'2024-06-18' },
  ]; }
};
export const markRead = (id) => api.patch(`/messages/${id}/read`);
