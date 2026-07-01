import api from './axios';

const MOCK = [
  { id: 1, title: 'AI Tutorial for Beginners', issuing_org: 'IBM SkillsBuild & Simplilearn', category: 'AI/ML', issue_date: '2026-05-12', skills_gained: ['AI Fundamentals', 'Machine Learning', 'Real-world AI'], credential_url: 'URL-FWOZMMIUQHG', featured: true, image_url: 'https://res.cloudinary.com/dezefzxbm/image/upload/v1782890501/portfolio/certificates/w2ae368yrzw9snssyx57.jpg', thumbnail: null },
  { id: 2, title: 'GSSoC 2026 Participant', issuing_org: 'GirlScript Summer of Code', category: 'Open Source', issue_date: '2026-08-01', skills_gained: ['Open Source', 'Collaboration'], credential_url: null, featured: true, image_url: 'https://res.cloudinary.com/dezefzxbm/image/upload/v1782890502/portfolio/certificates/vdjfchagmywvsffbuiu4.jpg', thumbnail: null },
  { id: 3, title: 'Gemini Student Ambassador', issuing_org: 'Google Developer Programs', category: 'AI/ML', issue_date: '2026-01-01', skills_gained: ['AI Advocacy', 'Community', 'Workshops'], credential_url: null, featured: true, image_url: 'https://res.cloudinary.com/dezefzxbm/image/upload/v1782890503/portfolio/certificates/ov44mnekva3dkws3kmus.jpg', thumbnail: null }
];

export const getCertificates = async (params) => {
  try {
    const r = await api.get('/certificates', { params });
    const list = r.data?.data || r.data || [];
    return list.map(c => ({
      ...c,
      issuing_org: c.issuer,
      skills_gained: c.skills
    }));
  }
  catch {
    if (params?.category && params.category !== 'All') return MOCK.filter(c => c.category === params.category);
    return MOCK;
  }
};

export const createCertificate = (data) => {
  const formData = new FormData();
  formData.append('title', data.title || '');
  formData.append('issuer', data.issuing_org || '');
  formData.append('category', data.category || 'Other');
  formData.append('issue_date', data.issue_date || '');
  formData.append('credential_url', data.credential_url || '');
  
  if (data.thumbnail) {
    formData.append('image', data.thumbnail);
  }
  
  return api.post('/certificates', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const updateCertificate = (id, data) => {
  const formData = new FormData();
  formData.append('title', data.title || '');
  formData.append('issuer', data.issuing_org || '');
  formData.append('category', data.category || 'Other');
  formData.append('issue_date', data.issue_date || '');
  formData.append('credential_url', data.credential_url || '');
  
  if (data.thumbnail && typeof data.thumbnail !== 'string') {
    formData.append('image', data.thumbnail);
  }
  
  return api.put(`/certificates/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const deleteCertificate = (id) => api.delete(`/certificates/${id}`);
