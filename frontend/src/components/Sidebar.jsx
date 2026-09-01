import { LayoutDashboard, ClipboardCheck, PlusCircle, Settings, Sparkles, ShieldCheck, ArrowUpRight } from 'lucide-react';
import { NavLink, useNavigate } from 'react-router-dom';
import sentinel from '../assets/sidebar-sentinel.png';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/audits', label: 'Audits', icon: ClipboardCheck },
  { to: '/new-audit', label: 'New Audit', icon: PlusCircle },
  { to: '/settings', label: 'Settings', icon: Settings },
];
export default function Sidebar() {
  const navigate = useNavigate();
  return <aside className="sidebar">
    <button className="brand" onClick={() => navigate('/')} aria-label="Go to landing page"><span className="brand-mark"><ShieldCheck size={22}/></span><span><b>Auditra</b><small>AI Workflow Intelligence</small></span></button>
    <nav>{links.map(({to,label,icon:Icon}) => <NavLink key={to} to={to} className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}><Icon size={19}/><span>{label}</span><span className="nav-glow"/></NavLink>)}</nav>
    <div className="sidebar-visual"><img src={sentinel} alt="Abstract AI audit shield illustration"/><div><span></span><h4>Audit with context, not guesswork.</h4><button onClick={() => navigate('/new-audit')}></button></div></div>
    <div className="sidebar-foot"><span className="status-dot"/><span>Local audit engine</span></div>
  </aside>;
}
