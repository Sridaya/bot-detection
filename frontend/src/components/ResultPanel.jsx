const RADIUS = 70
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

export default function ResultPanel({ result, loading, error }) {
  if (loading) {
    return (
      <div className="result-panel result-panel--empty">
        <div className="sweep" />
        <p className="empty-label">Reading signal…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="result-panel result-panel--empty">
        <p className="empty-label error-label">{error}</p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="result-panel result-panel--empty">
        <svg width="140" height="140" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r={RADIUS} fill="none" stroke="var(--border)" strokeWidth="10" />
        </svg>
        <p className="empty-label">Enter account stats to run a check</p>
      </div>
    )
  }

  const isBot = result.is_bot
  const pct = Math.round(result.confidence * 100)
  const accent = isBot ? 'var(--flag)' : 'var(--signal)'
  const offset = CIRCUMFERENCE - (pct / 100) * CIRCUMFERENCE

  return (
    <div className="result-panel">
      <div className="gauge-wrap">
        <svg width="160" height="160" viewBox="0 0 160 160">
          <circle cx="80" cy="80" r={RADIUS} fill="none" stroke="var(--border)" strokeWidth="10" />
          <circle
            cx="80"
            cy="80"
            r={RADIUS}
            fill="none"
            stroke={accent}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
            transform="rotate(-90 80 80)"
            style={{ transition: 'stroke-dashoffset 0.6s ease' }}
          />
        </svg>
        <div className="gauge-center">
          <span className="gauge-pct" style={{ color: accent }}>
            {pct}%
          </span>
          <span className="gauge-sub">confidence</span>
        </div>
      </div>

      <div className={`label-chip ${isBot ? 'label-chip--bot' : 'label-chip--human'}`}>
        {result.label}
      </div>
      <p className="result-username">@{result.username}</p>

      <ul className="reasons-list">
        {result.top_reasons.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  )
}
