import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, AlertTriangle, ArrowUpRight, CircleCheck, FileJson2, ShieldAlert, Sparkles, Wifi, WifiOff } from 'lucide-react';
import { api } from '../lib/api';
import ScoreOrb from '../components/ScoreOrb';
import RiskRibbon from '../components/RiskRibbon';
import TrendStream from '../components/TrendStream';

export default function Dashboard(){
  const navigate=useNavigate(); const [audits,setAudits]=useState([]); const [health,setHealth]=useState(null); const [loading,setLoading]=useState(true); const [error,setError]=useState('');
  useEffect(()=>{Promise.all([api.listAudits(),api.health().catch(()=>null)]).then(([a,h])=>{setAudits(a);setHealth(h)}).catch(e=>setError(e.message)).finally(()=>setLoading(false))},[]);
  const completed=audits.filter(a=>a.status==='completed'); const avg=Math.round(completed.reduce((s,a)=>s+(a.overall_score||0),0)/Math.max(1,completed.length));
  const totals=useMemo(()=>audits.reduce((o,a)=>{a.findings.forEach(f=>{const k=(f.severity||'low').toLowerCase();o[k]=(o[k]||0)+1});return o},{critical:0,high:0,medium:0,low:0}),[audits]);
  const riskData=['critical','high','medium','low'].map(k=>({label:k[0].toUpperCase()+k.slice(1),value:totals[k]}));
  const trend=[...completed].reverse().map(a=>a.overall_score||0).slice(-10);
  if(loading)return <div className="page-state">Loading audit intelligence…</div>;
  return <div className="page-grid dashboard-page">{error&&<div className="inline-error">{error}</div>}
    <section className="metric-grid"><article className="metric-card featured"><span className="metric-icon"><Sparkles/></span><div><small>Average audit score</small><strong>{avg || '—'}</strong><p>{completed.length} completed audits</p></div><div className="mini-ring" style={{'--p':`${(avg||0)*3.6}deg`}}/></article><article className="metric-card"><span className="metric-icon"><FileJson2/></span><div><small>Total audits</small><strong>{audits.length}</strong><p>{audits.filter(a=>a.status!=='completed').length} in progress / pending</p></div></article><article className="metric-card"><span className="metric-icon"><ShieldAlert/></span><div><small>High-priority risks</small><strong>{totals.critical+totals.high}</strong><p>{totals.critical} critical · {totals.high} high</p></div></article><article className="metric-card"><span className="metric-icon">{health?<Wifi/>:<WifiOff/>}</span><div><small>Audit engine</small><strong className="status-word">{health?'Online':'Offline'}</strong><p>{health?'FastAPI health check passed':'Check backend connection'}</p></div></article></section>
    <section className="panel span-8"><div className="panel-head"><div><p className="eyebrow">READINESS TRAJECTORY</p><h2>Audit score stream</h2></div><button className="text-btn" onClick={()=>navigate('/audits')}>View portfolio <ArrowUpRight size={16}/></button></div><TrendStream values={trend}/></section>
    <section className="panel span-4 score-panel"><p className="eyebrow">CURRENT POSTURE</p><ScoreOrb score={avg}/><p className="muted center">Portfolio average based on completed audits.</p></section>
    <section className="panel span-5"><div className="panel-head"><div><p className="eyebrow">RISK COMPOSITION</p><h2>Finding severity ribbon</h2></div></div><RiskRibbon data={riskData}/><div className="risk-insight"><AlertTriangle size={18}/><p>{totals.critical+totals.high ? 'Prioritize critical and high findings before production release.' : 'No critical/high findings are currently stored.'}</p></div></section>
    <section className="panel span-7"><div className="panel-head"><div><p className="eyebrow">RECENT ACTIVITY</p><h2>Latest audits</h2></div><button className="primary-btn small" onClick={()=>navigate('/new-audit')}>New audit</button></div><div className="audit-list compact-list">{audits.slice(0,5).map(a=><button key={a.id} onClick={()=>navigate(`/audits?id=${a.id}`)} className="audit-row"><span className="audit-row-icon"><Activity size={18}/></span><span className="grow"><b>{a.project_name}</b><small>{new Date(a.created_at).toLocaleString()}</small></span><span className={`status-chip ${a.status}`}>{a.status.replace('_',' ')}</span>{a.overall_score!=null&&<strong>{a.overall_score}</strong>}<ArrowUpRight size={16}/></button>)}{!audits.length&&<div className="empty-mini"><CircleCheck/><p>No audits yet. Launch your first review.</p></div>}</div></section>
  </div>;
}
