import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import AppShell from './components/AppShell';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Audits from './pages/Audits';
import NewAudit from './pages/NewAudit';
import Settings from './pages/Settings';

export default function App(){return <ThemeProvider><BrowserRouter><Routes><Route path="/" element={<Landing/>}/><Route element={<AppShell/>}><Route path="/dashboard" element={<Dashboard/>}/><Route path="/audits" element={<Audits/>}/><Route path="/new-audit" element={<NewAudit/>}/><Route path="/settings" element={<Settings/>}/></Route><Route path="*" element={<Navigate to="/" replace/>}/></Routes></BrowserRouter></ThemeProvider>}
