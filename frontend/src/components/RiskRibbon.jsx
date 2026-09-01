export default function RiskRibbon({ data }) {
  const total = Math.max(1, data.reduce((s, d) => s + d.value, 0));
  return <div className="risk-ribbon-wrap"><div className="risk-ribbon">{data.map((d) => <div key={d.label} className={`risk-seg ${d.label.toLowerCase()}`} style={{width: `${(d.value/total)*100}%`}} title={`${d.label}: ${d.value}`} />)}</div><div className="risk-legend">{data.map(d => <span key={d.label}><i className={d.label.toLowerCase()}/>{d.label}<b>{d.value}</b></span>)}</div></div>;
}
