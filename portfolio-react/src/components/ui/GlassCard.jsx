import { clsx } from 'clsx';
export default function GlassCard({ children, className='', hover=true }) {
  return (
    <div className={clsx(
      'glass-card backdrop-blur-xl rounded-lg border border-white/10 bg-surface-container/50',
      hover && 'hover:-translate-y-1 hover:shadow-card transition-all duration-300',
      className
    )}>{children}</div>
  );
}
