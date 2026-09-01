function points(values, width=640, height=180) {
  if (!values.length) return '';
  const max = Math.max(...values, 1), min = Math.min(...values, 0), range = Math.max(1, max-min);
  return values.map((v,i)=> `${(i/(Math.max(values.length-1,1)))*width},${height-((v-min)/range)*(height-30)-15}`).join(' ');
}
export default function TrendStream({ values=[] }) {
  const p = points(values);
  const area = p ? `0,180 ${p} 640,180` : '';
  return <div className="trend-stream"><svg viewBox="0 0 640 190" preserveAspectRatio="none"><defs><linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="var(--primary)" stopOpacity=".42"/><stop offset="1" stopColor="var(--primary)" stopOpacity="0"/></linearGradient></defs><g className="grid-lines">{[30,70,110,150].map(y=><line key={y} x1="0" y1={y} x2="640" y2={y}/>)}</g>{p && <><polygon points={area} fill="url(#areaGrad)"/><polyline points={p} fill="none" stroke="var(--primary)" strokeWidth="4" vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round"/></>}</svg><div className="chart-caption"><span>Older audits</span><span>Most recent</span></div></div>;
}
