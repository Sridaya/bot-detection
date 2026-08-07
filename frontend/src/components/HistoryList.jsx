export default function HistoryList({ history, onClear }) {
  if (!history.length) {
    return (
      <div className="history-panel">
        <div className="history-header">
          <h3>History</h3>
        </div>
        <p className="empty-label">No checks yet this session.</p>
      </div>
    )
  }

  return (
    <div className="history-panel">
      <div className="history-header">
        <h3>History</h3>
        <button className="clear-btn" onClick={onClear}>
          Clear
        </button>
      </div>
      <div className="history-list">
        {history.map((h, i) => (
          <div className="history-row" key={i}>
            <span className={`dot ${h.is_bot ? 'dot--bot' : 'dot--human'}`} />
            <span className="history-username">@{h.username}</span>
            <span className="history-label">{h.is_bot ? 'Bot' : 'Human'}</span>
            <span className="history-confidence">
              {Math.round(h.confidence * 100)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
