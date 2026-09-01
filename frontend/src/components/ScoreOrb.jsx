export default function ScoreOrb({ score = 0, label = 'Audit score' }) {
  const safe = Math.max(0, Math.min(100, Number(score) || 0));
  return <div className="score-orb" style={{'--score': `${safe * 3.6}deg`}}><div><strong>{safe}</strong><span>/ 100</span><small>{label}</small></div></div>;
}
