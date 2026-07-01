import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
export default function SkillForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Skill Name</label><input {...register('name')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
        <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['Frontend','Backend','Database','DevOps','AI/ML','Tools'].map(c=><option key={c}>{c}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Proficiency (0-100)</label><input type="number" min={0} max={100} {...register('proficiency',{valueAsNumber:true})} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Icon (emoji)</label><input {...register('icon')} placeholder="⚛️" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Skill</Button>
    </form>
  );
}
