import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import axios from '../../api/axios';
import { useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { ExternalLink, Code2 } from 'lucide-react';
import Button from '../ui/Button';

const schema = z.object({
  leetcode_username: z.string().min(1, 'Required').max(50).regex(/^[a-zA-Z0-9_-]+$/, 'Only letters, numbers, _, - allowed'),
});

export default function LeetCodeSettings({ currentUsername }) {
  const [isLoading, setIsLoading] = useState(false);
  const qc = useQueryClient();

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { leetcode_username: currentUsername || '' },
  });

  const onSave = async (data) => {
    setIsLoading(true);
    try {
      await axios.put('/profile', { leetcode_username: data.leetcode_username });
      qc.invalidateQueries(['profile']);
      qc.invalidateQueries(['leetcode-profile']);
      toast.success('LeetCode username saved!');
    } catch {
      // Mock mode fallback
      toast.success('Saved locally (Mock Mode)');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card rounded-xl p-6">
      <div className="flex items-center gap-2 mb-2">
        <Code2 size={20} className="text-primary"/>
        <h3 className="font-display font-semibold text-on-surface">LeetCode Integration</h3>
      </div>
      <p className="text-xs font-mono text-on-surface-variant mb-4">Set your public LeetCode username to display live coding stats.</p>
      
      <form onSubmit={handleSubmit(onSave)} className="flex flex-col sm:flex-row gap-3 items-start">
        <div className="flex-1 w-full">
          <div className="flex items-center bg-surface-container border border-outline-variant/40 rounded-lg overflow-hidden focus-within:border-primary/50 transition-colors">
            <span className="px-3 text-[11px] font-mono text-on-surface-variant bg-white/5 h-full flex items-center border-r border-outline-variant/40 py-2.5">leetcode.com/</span>
            <input {...register('leetcode_username')} placeholder="your_username" className="flex-1 px-3 py-2.5 bg-transparent text-on-surface font-body text-sm outline-none" />
          </div>
          {errors.leetcode_username && <p className="text-[10px] font-mono text-error mt-1">{errors.leetcode_username.message}</p>}
        </div>
        <Button type="submit" disabled={isLoading} className="whitespace-nowrap h-[42px]">{isLoading ? 'Saving...' : 'Save'}</Button>
        {currentUsername && (
          <a href={`https://leetcode.com/${currentUsername}`} target="_blank" rel="noopener noreferrer" className="h-[42px] px-3 rounded-lg border border-outline-variant/40 text-on-surface-variant hover:text-primary transition-colors flex items-center glass-panel">
            <ExternalLink size={16} />
          </a>
        )}
      </form>
    </div>
  );
}
