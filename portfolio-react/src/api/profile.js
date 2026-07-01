import api from './axios';

const MOCK = {
  name: 'Pradipta Chandra Giri',
  title: ['AI & Machine Learning Enthusiast', 'Full-Stack Developer', 'Python Developer', 'B.Tech CSE Student'],
  tagline: 'Building intelligent and scalable solutions to solve real-world problems.',
  bio: "Hello! I'm Pradipta Chandra Giri, a Computer Science and Engineering undergraduate at Veer Surendra Sai University of Technology (VSSUT), Burla. My interests revolve around Artificial Intelligence, Machine Learning, Full-Stack Development, Software Engineering, Database Systems, and System Design.",
  university: 'Veer Surendra Sai University of Technology (VSSUT), Burla',
  degree: 'B.Tech in Computer Science & Engineering',
  graduation_year: 2027,
  cgpa: '9.31',
  available_for: 'Internships, Open Source, Hackathons',
  email: 'giripradiptachandra@gmail.com',
  github: 'https://github.com/PradiptaChandraGiri',
  linkedin: 'https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/',
  twitter: 'https://x.com/Pradiptachandr5',
  leetcode: 'https://leetcode.com/Pradipta_Chandra_Giri/',
  leetcode_username: 'Pradipta_Chandra_Giri',
  profile_image_url: '/profile.jpg',
  resume_url: '#',
  location: 'Burla, Odisha, India',
};

export const getProfile = async () => {
  try {
    const r = await api.get('/profile');
    const data = (r.data?.data && r.data.data.name) ? r.data.data : MOCK;
    return {
      ...data,
      github: data.github_url || data.github || '',
      linkedin: data.linkedin_url || data.linkedin || '',
      twitter: data.twitter_url || data.twitter || '',
      leetcode: data.leetcode_username ? `https://leetcode.com/${data.leetcode_username}/` : (data.leetcode || '')
    };
  }
  catch {
    return MOCK;
  }
};

export const updateProfile = (data) => {
  const payload = {
    ...data,
    github_url: data.github,
    linkedin_url: data.linkedin,
    twitter_url: data.twitter
  };
  return api.put('/profile', payload);
};

export const uploadProfilePhoto = (file) => {
  const formData = new FormData();
  formData.append('photo', file);
  return api.post('/profile/photo', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const uploadProfileResume = (file) => {
  const formData = new FormData();
  formData.append('resume', file);
  return api.post('/profile/resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};
