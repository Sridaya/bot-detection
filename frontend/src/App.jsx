import { useEffect, useState } from 'react'
import StatsForm from './components/StatsForm.jsx'
import ResultPanel from './components/ResultPanel.jsx'
import HistoryList from './components/HistoryList.jsx'
import { checkAccount, fetchHistory, clearHistory } from './api.js'
import './App.css'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])

  const loadHistory = async () => {
    try {
      const data = await fetchHistory()
      setHistory(data)
    } catch {
      // Non-fatal — history is a nice-to-have
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const handleSubmit = async (payload) => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await checkAccount(payload)
      setResult(data)
      loadHistory()
    } catch (err) {
      setError(err.message || 'Could not reach the detection service')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    await clearHistory()
    setHistory([])
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="wordmark">
          <span className="wordmark-icon">◎</span>
          <span>SIGNAL</span>
        </div>
        <p className="tagline">
          Bot-likelihood detection from public account signals — followers, activity,
          and profile patterns — trained on ~2,800 labeled accounts.
        </p>
      </header>

      <main className="app-grid">
        <section className="panel">
          <h2 className="panel-title">Account stats</h2>
          <StatsForm onSubmit={handleSubmit} loading={loading} />
        </section>

        <section className="panel">
          <h2 className="panel-title">Detection result</h2>
          <ResultPanel result={result} loading={loading} error={error} />
        </section>
      </main>

      <section className="panel history-section">
        <HistoryList history={history} onClear={handleClear} />
      </section>

      <footer className="app-footer">
        Built by Dayasri K · Random Forest classifier, scikit-learn · Not affiliated with X/Twitter
      </footer>
    </div>
  )
}
