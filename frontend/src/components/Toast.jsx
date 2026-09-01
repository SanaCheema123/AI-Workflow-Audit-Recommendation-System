import { CheckCircle2, XCircle, X } from 'lucide-react';
export default function Toast({ toast, onClose }) {
  if (!toast) return null;
  const Icon = toast.type === 'error' ? XCircle : CheckCircle2;
  return <div className={`toast ${toast.type || 'success'}`}><Icon size={18}/><span>{toast.message}</span><button onClick={onClose}><X size={16}/></button></div>;
}
