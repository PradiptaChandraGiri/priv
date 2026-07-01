import api from './axios';

const MOCK = [
  { id: 1, title: 'Efficient Attention Mechanisms for Long-Range Dependencies in Transformers', authors: ['Pradipta Chandra Giri', 'Dr. Suresh Kumar'], journal: 'arXiv Preprint', status: 'preprint', date: '2024-02-10', abstract: 'We propose a novel attention mechanism that reduces the quadratic complexity of self-attention to linear, enabling transformers to process significantly longer sequences without memory overflow. Our method achieves state-of-the-art results on several NLP benchmarks while reducing compute by 60%.', keywords: ['NLP', 'Transformers', 'Attention', 'Deep Learning'], citations: 0, arxiv_url: 'https://arxiv.org', doi: null, paper_url: null },
  { id: 2, title: 'Federated Learning for Privacy-Preserving IoT Anomaly Detection', authors: ['Pradipta Chandra Giri', 'Prof. Anjali Sharma', 'Dr. Ravi Mohan'], journal: 'IEEE Internet of Things Journal', status: 'under_review', date: '2023-11-20', abstract: 'A federated learning framework for detecting anomalies in distributed IoT networks while preserving data privacy. We demonstrate that our approach achieves comparable accuracy to centralized methods while keeping data on-device.', keywords: ['Federated Learning', 'IoT', 'Privacy', 'Anomaly Detection'], citations: 3, arxiv_url: null, doi: '10.1109/jiot.2023', paper_url: null },
];

export const getResearch = async () => {
  try { const r = await api.get('/research'); return r.data?.data || r.data; }
  catch { return MOCK; }
};
export const createResearch = (data) => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, val]) => {
    if (key === 'pdf' && val) {
      formData.append('pdf', val);
    } else if (val !== undefined && val !== null) {
      formData.append(key, val);
    }
  });
  return api.post('/research', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const updateResearch = (id, data) => {
  const formData = new FormData();
  Object.entries(data).forEach(([key, val]) => {
    if (key === 'pdf' && val) {
      formData.append('pdf', val);
    } else if (val !== undefined && val !== null) {
      formData.append(key, val);
    }
  });
  return api.put(`/research/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const deleteResearch = (id) => api.delete(`/research/${id}`);
