export default function SectionHeader({ title, subtitle, viewAll, viewAllLink }) {
  return (
    <div className="text-center mb-12">
      <h2 className="font-display font-bold text-3xl md:text-4xl bg-gradient-to-r from-primary via-secondary to-tertiary bg-clip-text text-transparent mb-3">{title}</h2>
      {subtitle && <p className="font-body text-on-surface-variant max-w-2xl mx-auto">{subtitle}</p>}
      {viewAll && <a href={viewAllLink || '#'} className="inline-flex items-center gap-1 font-mono text-[11px] uppercase tracking-wider text-primary hover:text-primary-light mt-2 transition-colors">{viewAll} →</a>}
    </div>
  );
}
