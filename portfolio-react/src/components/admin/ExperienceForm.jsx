import { useForm } from 'react-hook-form';
import Button from '../ui/Button';

export default function ExperienceForm({ onSubmit, defaultValues }) {
  // Format description & tech_used arrays to comma-separated strings for editing
  const initialValues = defaultValues ? {
    ...defaultValues,
    description: Array.isArray(defaultValues.description) 
      ? defaultValues.description.join('\n') 
      : defaultValues.description || '',
    tech_used: Array.isArray(defaultValues.tech_used)
      ? defaultValues.tech_used.join(', ')
      : defaultValues.tech_used || ''
  } : undefined;

  const { register, handleSubmit, watch } = useForm({ defaultValues: initialValues });
  const isCurrent = watch('is_current');

  const handleFormSubmit = (data) => {
    const payload = {
      ...data,
      is_current: data.is_current === 'true' || data.is_current === true,
      description: data.description.split('\n').map(s => s.trim()).filter(Boolean),
      tech_used: data.tech_used.split(',').map(s => s.trim()).filter(Boolean)
    };
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Company / Project Name</label>
          <input type="text" {...register('company')} placeholder="e.g. Google" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
        </div>
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Role / Designation</label>
          <input type="text" {...register('role')} placeholder="e.g. SDE Intern" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Start Date</label>
          <input type="date" {...register('start_date')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
        </div>
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">End Date</label>
          <input type="date" {...register('end_date')} disabled={isCurrent} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors disabled:opacity-50"/>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <input type="checkbox" id="is_current" {...register('is_current')} className="rounded border-outline-variant bg-surface-container text-primary focus:ring-primary"/>
        <label htmlFor="is_current" className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant cursor-pointer">I am currently working in this role</label>
      </div>

      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Responsibilities / Highlights (One per line)</label>
        <textarea {...register('description')} rows={3} placeholder="Developed microservices&#10;Decreased build times by 15%" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors resize-y"/>
      </div>

      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Tech Stack Used (comma-separated)</label>
        <input type="text" {...register('tech_used')} placeholder="React, Node.js, AWS" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
      </div>

      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Sort Order</label>
        <input type="number" {...register('sort_order')} placeholder="0" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
      </div>

      <Button type="submit" variant="primary" className="w-full">Save Experience</Button>
    </form>
  );
}
