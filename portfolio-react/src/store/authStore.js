import { create } from 'zustand';
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
