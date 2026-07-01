import api from './axios';

export const loginAdmin = async (credentials) => {
  const { data } = await api.post('/auth/login', credentials);
  return data;
};

export const googleLogin = async (idToken) => {
  const { data } = await api.post('/auth/google-login', { idToken });
  return data;
};
