import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShieldCheck, Loader2 } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

import { googleLogin } from '../api/auth';

export default function AdminLoginPage() {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [shake, setShake] = useState(false);
  const [error, setError] = useState('');
  const [isGoogleSubmitting, setIsGoogleSubmitting] = useState(false);

  const handleGoogleLoginSuccess = async (response) => {
    setError('');
    setIsGoogleSubmitting(true);
    try {
      const data = await googleLogin(response.credential);
      login(data.token, data.name || 'Admin');
      navigate('/admin/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Access denied. Unauthorized Gmail.');
      setShake(true);
      setTimeout(() => setShake(false), 600);
    } finally {
      setIsGoogleSubmitting(false);
    }
  };

  useEffect(() => {
    const initGoogle = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID || "1015694200788-3i9cfl7uafc8ldc8c3chq1j3g5v53t2b.apps.googleusercontent.com",
          callback: handleGoogleLoginSuccess
        });
        window.google.accounts.id.renderButton(
          document.getElementById("google-signin-btn"),
          { theme: "outline", size: "large", width: 320, text: "signin_with" }
        );
      }
    };
    
    const timer = setInterval(() => {
      if (window.google) {
        initGoogle();
        clearInterval(timer);
      }
    }, 100);
    
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-5 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl pointer-events-none"/>
      <motion.div
        animate={shake ? { x: [-8, 8, -6, 6, -4, 4, 0] } : {}}
        transition={{ duration: 0.45 }}
        className="w-full max-w-sm">
        <div className="glass-card rounded-xl overflow-hidden border border-white/10 shadow-card">
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"/>
          <div className="p-8">
            <div className="flex flex-col items-center text-center mb-8">
              <div className="w-16 h-16 rounded-full bg-surface-container border border-outline-variant/40 flex items-center justify-center mb-4 shadow-glow">
                <ShieldCheck size={28} className="text-primary"/>
              </div>
              <h1 className="font-display font-bold text-2xl text-on-surface">SYSTEM_ADMIN</h1>
              <p className="font-mono text-xs text-on-surface-variant mt-1">Authorize via Google SSO to access command center.</p>
            </div>
            {error && <motion.div initial={{opacity:0,y:-4}} animate={{opacity:1,y:0}} className="mb-6 p-3 rounded-lg bg-error/10 border border-error/30 text-error font-mono text-xs text-center">{error}</motion.div>}
            
            <div className="flex flex-col items-center gap-4 py-2">
              <div id="google-signin-btn" className="w-full flex justify-center"></div>
              {isGoogleSubmitting && (
                <div className="flex items-center gap-2 font-mono text-[10px] text-primary uppercase tracking-wider animate-pulse">
                  <Loader2 size={12} className="animate-spin"/>
                  Verifying SSO Token...
                </div>
              )}
            </div>

            <div className="mt-8 text-center flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse"/>
              <span className="font-mono text-[10px] text-on-surface-variant/50 uppercase tracking-widest">Secure Connection Verified</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
