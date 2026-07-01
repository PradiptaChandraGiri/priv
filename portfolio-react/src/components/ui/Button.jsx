import { clsx } from 'clsx';
export default function Button({ children, variant='primary', className='', ...props }) {
  const base = 'font-mono text-[11px] uppercase tracking-wider px-6 py-3 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-semibold disabled:opacity-50 disabled:cursor-not-allowed';
  const variants = {
    primary: 'bg-primary text-on-primary hover:bg-primary-light hover:shadow-glow-sm',
    outline: 'glass-panel text-primary hover:bg-primary/10 border border-primary/30',
    ghost: 'text-on-surface-variant hover:text-primary hover:bg-primary/10',
    danger: 'bg-error/20 text-error border border-error/30 hover:bg-error/30',
    pill: 'bg-primary text-on-primary rounded-full hover:bg-primary-light hover:shadow-glow-sm',
  };
  return <button className={clsx(base, variants[variant], className)} {...props}>{children}</button>;
}
