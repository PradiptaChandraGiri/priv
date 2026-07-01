import { clsx } from 'clsx';
export default function Badge({ children, variant='primary', size='md', className='' }) {
  const base = 'rounded-full font-mono uppercase tracking-wider inline-flex items-center';
  const sizes = { sm: 'text-[9px] px-2 py-0.5', md: 'text-[10px] px-3 py-1', lg: 'text-xs px-4 py-1.5' };
  const variants = {
    primary: 'bg-primary/15 text-primary border border-primary/30',
    secondary: 'bg-secondary/15 text-secondary border border-secondary/30',
    success: 'bg-success/15 text-success border border-success/30',
    warning: 'bg-warning/15 text-warning border border-warning/30',
    error: 'bg-error/15 text-error border border-error/30',
    neutral: 'bg-white/5 text-on-surface-variant border border-outline-variant/30',
    tertiary: 'bg-tertiary/15 text-tertiary border border-tertiary/30',
  };
  return <span className={clsx(base, sizes[size], variants[variant], className)}>{children}</span>;
}
