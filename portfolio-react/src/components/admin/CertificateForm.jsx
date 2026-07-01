import { useForm } from 'react-hook-form';
import Button from '../ui/Button';
import FileUpload from '../ui/FileUpload';
import { useState } from 'react';
export default function CertificateForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({ defaultValues });
  const [file, setFile] = useState(null);
  return (
    <form onSubmit={handleSubmit(d => onSubmit({...d, thumbnail: file}))} className="space-y-4">
      {[['title','Certificate Title'],['issuing_org','Issuing Organization'],['credential_url','Credential URL (optional)']].map(([name,label])=>(
        <div key={name}><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">{label}</label>
        <input {...register(name)} placeholder={label} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      ))}
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Category</label>
        <select {...register('category')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50">
          {['AI/ML','Cloud','Web Dev','DSA','Core CS','Other'].map(c=><option key={c}>{c}</option>)}
        </select></div>
      <div><label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Issue Date</label><input type="date" {...register('issue_date')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2.5 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/></div>
      <div>
        <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Certificate Image / PDF</label>
        {defaultValues?.image_url && !file && (
          <div className="mb-3">
            <p className="font-mono text-[9px] uppercase text-primary mb-1">Current Certificate Image</p>
            <img src={defaultValues.image_url} alt="Current certificate" className="w-40 h-24 object-cover rounded-lg border border-outline-variant/30" />
          </div>
        )}
        <FileUpload onFile={setFile} file={file} label="Drop certificate image or PDF"/>
      </div>
      <Button type="submit" variant="primary" className="w-full">Save Certificate</Button>
    </form>
  );
}
