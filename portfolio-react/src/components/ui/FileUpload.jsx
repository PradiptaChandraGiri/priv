import { useDropzone } from 'react-dropzone';
import { UploadCloud, X, FileText } from 'lucide-react';
export default function FileUpload({ onFile, accept, file, label='Drop files here or click to browse' }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (f) => f[0] && onFile(f[0]),
    accept: accept || { 'image/*': [], 'application/pdf': [] },
    maxFiles: 1,
  });
  return (
    <div>
      <div {...getRootProps()} className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${isDragActive ? 'border-primary bg-primary/10' : 'border-outline-variant/40 hover:border-primary/50 hover:bg-primary/5'}`}>
        <input {...getInputProps()} />
        <UploadCloud className="mx-auto mb-3 text-on-surface-variant" size={32}/>
        <p className="font-mono text-[11px] uppercase tracking-wider text-on-surface-variant">{isDragActive ? 'Drop it!' : label}</p>
      </div>
      {file && (
        <div className="mt-3 flex items-center gap-3 glass-panel rounded-lg p-3">
          {file.type?.startsWith('image/') ? <img src={URL.createObjectURL(file)} className="w-10 h-10 rounded object-cover" alt="preview"/> : <FileText size={20} className="text-primary"/>}
          <span className="font-mono text-xs text-on-surface-variant flex-1 truncate">{file.name}</span>
          <button onClick={() => onFile(null)} className="text-on-surface-variant hover:text-error transition-colors"><X size={16}/></button>
        </div>
      )}
    </div>
  );
}
