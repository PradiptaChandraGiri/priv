import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';
import { Mail, Phone, MapPin, Code2, CheckCircle, Send, Loader2 } from 'lucide-react';
import { Github, Linkedin, Twitter } from '../components/icons/BrandIcons';
import { submitContact } from '../api/contact';
import { useProfile } from '../hooks/useProfile';
import Badge from '../components/ui/Badge';

const schema = z.object({
  firstName: z.string().min(2, 'Min 2 characters'),
  lastName: z.string().min(2, 'Min 2 characters'),
  email: z.string().email('Invalid email'),
  subject: z.string(),
  message: z.string().min(10, 'Min 10 characters'),
});

export default function ContactPage() {
  const { data: profile } = useProfile();
  const [success, setSuccess] = useState(false);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = async (data) => {
    try {
      await submitContact(data);
      setSuccess(true);
    } catch {
      toast.error('Failed to send. Please try again.');
    }
  };

  const inputClass = "w-full bg-background border border-outline-variant/40 rounded-lg px-4 py-3 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 transition-all placeholder:text-on-surface-variant/40";
  const errClass = "text-error font-mono text-[10px] mt-1";

  const contacts = [
    { icon: Mail, label: profile?.email || 'giripradiptachandra@gmail.com', href: `mailto:${profile?.email||'giripradiptachandra@gmail.com'}` },
    { icon: MapPin, label: 'VSSUT Burla, Sambalpur, Odisha, India', href: 'https://maps.google.com/?q=Veer+Surendra+Sai+University+of+Technology,+Burla,+Sambalpur,+Odisha', isExternal: true },
    { icon: Github, label: 'GitHub', href: profile?.github_url || 'https://github.com/PradiptaChandraGiri', isExternal: true },
    { icon: Linkedin, label: 'LinkedIn', href: profile?.linkedin_url || 'https://www.linkedin.com/in/pradipta-chandra-giri-035b88340/', isExternal: true },
  ];

  return (
    <div className="min-h-screen py-20 px-5 md:px-16">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
          {/* Left */}
          <div>
            <h1 className="font-display font-bold text-4xl md:text-5xl text-on-surface mb-3">Let's <span className="gradient-text">Connect</span></h1>
            <p className="font-body text-on-surface-variant mb-8">Open to internship opportunities, research collaborations, and open source contributions.</p>
            <div className="space-y-4 mb-8">
              {contacts.map(c => (
                <a
                  key={c.label}
                  href={c.href}
                  target={c.isExternal ? '_blank' : undefined}
                  rel={c.isExternal ? 'noopener noreferrer' : undefined}
                  className="w-full flex items-center gap-4 glass-card rounded-xl p-4 hover:border-primary/30 hover:shadow-glow-sm transition-all group text-left"
                >
                  <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                    <c.icon size={18} className="text-primary" />
                  </div>
                  <span className="font-body text-sm text-on-surface-variant group-hover:text-on-surface transition-colors">
                    {c.label}
                  </span>
                </a>
              ))}
            </div>
            <motion.div whileInView={{opacity:1,y:0}} initial={{opacity:0,y:10}} viewport={{once:true}} className="glass-card rounded-xl p-6 border border-success/20">
              <div className="flex items-center gap-3 mb-2"><span className="w-2.5 h-2.5 rounded-full bg-success animate-pulse"/><span className="font-mono text-[11px] uppercase tracking-wider text-success">Available for Hire</span></div>
              <p className="font-mono text-xs text-on-surface-variant">
                {Array.isArray(profile?.available_for) 
                  ? profile.available_for.join(', ') 
                  : (profile?.available_for || 'SDE Internships, AI/ML Research, Open Source, Full-Stack Projects')}
              </p>
            </motion.div>
            
            {/* Inline Map Embed */}
            <motion.div 
              whileInView={{ opacity: 1, y: 0 }} 
              initial={{ opacity: 0, y: 10 }} 
              viewport={{ once: true }} 
              className="glass-card rounded-xl p-3 border border-outline-variant/20 h-64 mt-4 overflow-hidden"
            >
              <iframe
                title="VSSUT Burla Map"
                src="https://maps.google.com/maps?q=Veer%20Surendra%20Sai%20University%20of%20Technology,%20Burla,%20Sambalpur,%20Odisha&t=&z=14&ie=UTF8&iwloc=&output=embed"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen=""
                loading="lazy"
                className="rounded-lg"
              />
            </motion.div>
          </div>

          {/* Right - Form */}
          <div className="glass-card rounded-xl p-6 md:p-8 sticky top-24">
            <AnimatePresence mode="wait">
              {success ? (
                <motion.div key="success" initial={{opacity:0,scale:0.9}} animate={{opacity:1,scale:1}} exit={{opacity:0}} className="flex flex-col items-center text-center py-10 gap-4">
                  <motion.div initial={{scale:0}} animate={{scale:1}} transition={{type:'spring',delay:0.1}}><CheckCircle size={64} className="text-success"/></motion.div>
                  <h3 className="font-display font-bold text-xl text-on-surface">Message Sent!</h3>
                  <p className="font-mono text-xs text-on-surface-variant">I'll reply within 24 hours.</p>
                  <button onClick={() => { setSuccess(false); reset(); }} className="btn-outline py-2 px-6 mt-2">Send Another</button>
                </motion.div>
              ) : (
                <motion.form key="form" onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                  <h2 className="font-display font-semibold text-xl text-on-surface mb-4">Send a Message</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div><input {...register('firstName')} placeholder="First Name" className={inputClass}/>{errors.firstName && <p className={errClass}>{errors.firstName.message}</p>}</div>
                    <div><input {...register('lastName')} placeholder="Last Name" className={inputClass}/>{errors.lastName && <p className={errClass}>{errors.lastName.message}</p>}</div>
                  </div>
                  <div><input {...register('email')} type="email" placeholder="Email" className={inputClass}/>{errors.email && <p className={errClass}>{errors.email.message}</p>}</div>
                  <select {...register('subject')} className={inputClass}>
                    {['Job Opportunity','Collaboration','General Inquiry','Other'].map(o=><option key={o} value={o}>{o}</option>)}
                  </select>
                  <div><textarea {...register('message')} placeholder="Your message..." rows={5} className={`${inputClass} resize-none`}/>{errors.message && <p className={errClass}>{errors.message.message}</p>}</div>
                  <button type="submit" disabled={isSubmitting} className="btn-primary w-full justify-center shadow-glow-sm">
                    {isSubmitting ? <><Loader2 size={16} className="animate-spin"/>Sending...</> : <><Send size={16}/>Send Message</>}
                  </button>
                </motion.form>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
