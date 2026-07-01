import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
import FileUpload from '../ui/FileUpload';
import { useState } from 'react';

export default function ProjectForm({ onSubmit, defaultValues }) {
  const formattedDefaultValues = defaultValues ? {
    ...defaultValues,
    tech_stack: Array.isArray(defaultValues.tech_stack)
      ? defaultValues.tech_stack.join(', ')
      : defaultValues.tech_stack
  } : undefined;

  const { register, handleSubmit } = useForm({ defaultValues: formattedDefaultValues });
  const [file, setFile] = useState(null);

  return (
    <form onSubmit={handleSubmit(d => onSubmit({...d, thumbnail: file}))} className="space-y-4 max-h-[80vh] overflow-y-auto px-1">
      {[['title','Title','text'],['description','Description (short)','text'],['tech_stack','Technologies (comma-separated)','text'],['github_url','GitHub URL','url'],['live_url','Live URL (optional)','url'],['sort_order','Sort Order','number']].map(([name,label,type])=>(
        <div key={name}>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">{label}</label>
          <input type={type} {...register(name)} placeholder={label} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 transition-colors"/>
        </div>
      ))}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
          <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
            {['web','ml','systems','mobile','other'].map(c=><option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Status</label>
          <select {...register('status')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
            {['completed','ongoing','archived'].map(s=><option key={s} value={s}>{s}</option>)}
          </select>
        </div>
      </div>
      <div className="flex items-center gap-2 py-2">
        <input 
          type="checkbox" 
          id="featured-checkbox" 
          {...register('featured')} 
          className="w-4 h-4 rounded bg-surface-container border border-outline-variant/40 text-primary focus:ring-primary focus:ring-offset-background"
        />
        <label htmlFor="featured-checkbox" className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant cursor-pointer select-none">
          Featured Project (Show on Home Page)
        </label>
      </div>
      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Thumbnail Image</label>
        {defaultValues?.thumbnail_url && !file && (
          <div className="mb-3">
            <p className="font-mono text-[9px] uppercase text-primary mb-1">Current Thumbnail</p>
            <img src={defaultValues.thumbnail_url} alt="Current thumbnail" className="w-40 h-24 object-cover rounded-lg border border-outline-variant/30" />
          </div>
        )}
        <FileUpload onFile={setFile} file={file} accept={{'image/*':[]}} label="Drop project image here"/>
      </div>
      <Button type="submit" variant="primary" className="w-full">Save Project</Button>
    </form>
  );
}
