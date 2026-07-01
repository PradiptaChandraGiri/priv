import { useForm } from 'react-hook-form';
import Button from '../ui/Button';

export default function AchievementForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {[['title','Title','text'],['description','Description','text'],['date','Date (e.g. 2026)','text']].map(([name,label,type])=>(
        <div key={name}>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">{label}</label>
          <input type={type} {...register(name)} placeholder={label} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
        </div>
      ))}
      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Sort Order</label>
        <input type="number" {...register('sort_order')} placeholder="0" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
      </div>
      <Button type="submit" variant="primary" className="w-full">Save Achievement</Button>
    </form>
  );
}
