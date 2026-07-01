import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
export default function ResearchForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Title</label><input {...register('title')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Journal / Conference</label><input {...register('journal')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Abstract</label><textarea {...register('abstract')} rows={4} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 resize-none"/></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Status</label>
        <select {...register('status')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['preprint','under_review','published'].map(s=><option key={s} value={s}>{s}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">arXiv URL</label><input {...register('arxiv_url')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <Button type="submit" variant="primary" className="w-full">Save Research</Button>
    </form>
  );
}
