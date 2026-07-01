import { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import Button from '../ui/Button';
import FileUpload from '../ui/FileUpload';
import { uploadProfilePhoto, uploadProfileResume } from '../../api/profile';

export default function ProfileForm({ onSubmit, defaultValues }) {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      ...defaultValues,
      // Map arrays to comma-separated strings for easy editing
      title: Array.isArray(defaultValues?.title) ? defaultValues.title.join(', ') : (defaultValues?.title || ''),
      available_for: Array.isArray(defaultValues?.available_for) ? defaultValues.available_for.join(', ') : (defaultValues?.available_for || '')
    }
  });

  const [photoFile, setPhotoFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [uploadingResume, setUploadingResume] = useState(false);

  const handleFormSubmit = async (data) => {
    // Convert comma-separated strings back to arrays
    const formattedData = {
      ...data,
      title: data.title.split(',').map(s => s.trim()).filter(Boolean),
      available_for: data.available_for.split(',').map(s => s.trim()).filter(Boolean)
    };
    onSubmit(formattedData);
  };

  const handlePhotoUpload = async () => {
    if (!photoFile) return toast.error('Select a photo first');
    setUploadingPhoto(true);
    try {
      const res = await uploadProfilePhoto(photoFile);
      toast.success('Profile photo updated successfully!');
      setPhotoFile(null);
    } catch (err) {
      toast.error(err.response?.data?.message || 'Photo upload failed');
    } finally {
      setUploadingPhoto(false);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) return toast.error('Select a PDF file first');
    setUploadingResume(true);
    try {
      const res = await uploadProfileResume(resumeFile);
      toast.success('Resume PDF updated successfully!');
      setResumeFile(null);
    } catch (err) {
      toast.error(err.response?.data?.message || 'Resume upload failed');
    } finally {
      setUploadingResume(false);
    }
  };

  return (
    <div className="space-y-8 max-w-2xl">
      {/* Bio / Meta Section */}
      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 glass-card p-6 rounded-xl border border-white/5">
        <h3 className="font-display font-semibold text-lg text-on-surface mb-2 border-b border-outline-variant/10 pb-2">Profile Details</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Full Name</label>
            <input type="text" {...register('name')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">CGPA</label>
            <input type="text" {...register('cgpa')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Titles (comma-separated roles)</label>
          <input type="text" {...register('title')} placeholder="Full-Stack Developer, AI Enthusiast, B.Tech CSE Student" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
        </div>

        <div>
          <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Bio / Summary</label>
          <textarea {...register('bio')} rows={3} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50 resize-y"/>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">University Name</label>
            <input type="text" {...register('university')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Location</label>
            <input type="text" {...register('location')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Degree Name</label>
            <input type="text" {...register('degree')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Graduation Year</label>
            <input type="number" {...register('graduation_year')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Contact Email</label>
            <input type="email" {...register('email')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Available For (comma-separated)</label>
            <input type="text" {...register('available_for')} placeholder="Internships, SDE Projects, Open Source" className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <h4 className="font-display font-medium text-sm text-on-surface mt-4 border-b border-outline-variant/5 pb-1">Social Links</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">GitHub URL</label>
            <input type="url" {...register('github')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">LinkedIn URL</label>
            <input type="url" {...register('linkedin')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">Twitter URL</label>
            <input type="url" {...register('twitter')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
          <div>
            <label className="font-mono text-[10px] uppercase tracking-wider text-on-surface-variant mb-1 block">LeetCode Username</label>
            <input type="text" {...register('leetcode_username')} className="w-full bg-surface-container border border-outline-variant/40 rounded-lg px-4 py-2 text-on-surface font-body text-sm focus:outline-none focus:border-primary/50"/>
          </div>
        </div>

        <div className="pt-2">
          <Button type="submit" variant="primary" className="w-full">Save Profile Information</Button>
        </div>
      </form>

      {/* Media Uploads Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Profile Photo Upload */}
        <div className="glass-card p-6 rounded-xl border border-white/5 flex flex-col justify-between">
          <div>
            <h3 className="font-display font-semibold text-lg text-on-surface border-b border-outline-variant/10 pb-2 mb-4">Profile Photo</h3>
            {defaultValues?.profile_image_url && !photoFile && (
              <div className="flex flex-col items-center mb-4">
                <p className="font-mono text-[9px] uppercase text-primary mb-2">Current Photo</p>
                <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-primary/30 shadow-glow">
                  <img src={defaultValues.profile_image_url} alt="Current profile" className="w-full h-full object-cover" />
                </div>
              </div>
            )}
            <FileUpload onFile={setPhotoFile} file={photoFile} accept={{'image/*':[]}} label="Drop profile image here"/>
          </div>
          <div className="mt-4">
            <Button onClick={handlePhotoUpload} variant="primary" disabled={uploadingPhoto || !photoFile} className="w-full justify-center">
              {uploadingPhoto ? 'Uploading to Cloudinary...' : 'Upload Photo'}
            </Button>
          </div>
        </div>

        {/* Resume PDF Upload */}
        <div className="glass-card p-6 rounded-xl border border-white/5 flex flex-col justify-between">
          <div>
            <h3 className="font-display font-semibold text-lg text-on-surface border-b border-outline-variant/10 pb-2 mb-4">Resume PDF</h3>
            {defaultValues?.resume_url && !resumeFile && (
              <div className="flex flex-col items-center mb-4">
                <p className="font-mono text-[9px] uppercase text-primary mb-2">Current Resume</p>
                <a href={defaultValues.resume_url} target="_blank" rel="noopener noreferrer" className="btn-outline py-1 px-4 text-xs flex items-center gap-1.5 hover:text-primary transition-colors">
                  <span>📄</span> View Uploaded PDF
                </a>
              </div>
            )}
            <div className="bg-surface-container border border-dashed border-outline-variant/40 rounded-lg p-6 flex flex-col items-center justify-center text-center cursor-pointer hover:border-primary/40 transition-colors">
              <input type="file" id="resume-file-input" accept=".pdf" className="hidden" onChange={e => setResumeFile(e.target.files[0])}/>
              <label htmlFor="resume-file-input" className="cursor-pointer w-full h-full flex flex-col items-center justify-center">
                <span className="text-3xl mb-2">📄</span>
                {resumeFile ? (
                  <span className="font-body text-sm text-primary font-medium">{resumeFile.name}</span>
                ) : (
                  <>
                    <span className="font-body text-sm text-on-surface font-medium">Click to select resume PDF</span>
                    <span className="font-mono text-[9px] text-on-surface-variant/60 mt-1 uppercase">PDF Files Only</span>
                  </>
                )}
              </label>
            </div>
          </div>
          <div className="mt-4">
            <Button onClick={handleResumeUpload} variant="primary" disabled={uploadingResume || !resumeFile} className="w-full justify-center">
              {uploadingResume ? 'Uploading to Cloudinary...' : 'Upload Resume PDF'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
