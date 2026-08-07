const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function checkAccount(payload) {
  const res = await fetch(`${API_BASE}/api/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Something went wrong' }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

export async function fetchHistory(limit = 20) {
  const res = await fetch(`${API_BASE}/api/history?limit=${limit}`)
  if (!res.ok) throw new Error('Could not load history')
  return res.json()
}

export async function clearHistory() {
  const res = await fetch(`${API_BASE}/api/history`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Could not clear history')
  return res.json()
}
