import { Outlet, useLocation } from 'react-router-dom';
import { Bell, Search, Command } from 'lucide-react';
import Sidebar from './Sidebar';

const titles = {
  '/dashboard': ['Command Center', 'Portfolio-level health across every workflow audit.'],
  '/audits': ['Audit Workspace', 'Inspect evidence, findings, and recommendations in one place.'],
  '/new-audit': ['Launch Audit', 'Create a project, attach n8n workflows, and run the audit engine.'],
  '/settings': ['Preferences', 'Tune your appearance and local workspace behavior.'],
};
export default function AppShell() {
  const location = useLocation();
  const [title, subtitle] = titles[location.pathname] || titles['/dashboard'];
  return <div className="app-shell"><Sidebar/><main className="app-main"><header className="topbar"><div><p className="eyebrow">AI WORKFLOW AUDIT</p><h1>{title}</h1><p>{subtitle}</p></div><div className="top-actions"><button className="icon-btn" title="Search" onClick={() => window.dispatchEvent(new CustomEvent('focus-audit-search'))}><Search size={18}/></button><button className="icon-btn" title="Keyboard hint" onClick={() => alert('Tip: use the sidebar to move between workspaces.')}><Command size={18}/></button><button className="icon-btn" title="Notifications" onClick={() => alert('No new audit notifications.')}><Bell size={18}/></button></div></header><Outlet/></main></div>;
}
