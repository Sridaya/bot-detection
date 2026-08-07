import { useState } from 'react'

const initialState = {
  username: '',
  followers_count: '',
  friends_count: '',
  listed_count: '',
  favourites_count: '',
  statuses_count: '',
  account_age_days: '',
  verified: false,
  default_profile: false,
  default_profile_image: false,
  bio: '',
}

const FIELDS = [
  { key: 'followers_count', label: 'Followers', hint: 'Follower count' },
  { key: 'friends_count', label: 'Following', hint: 'Accounts they follow' },
  { key: 'statuses_count', label: 'Tweets/Posts', hint: 'Total post count' },
  { key: 'favourites_count', label: 'Likes', hint: 'Total likes given' },
  { key: 'listed_count', label: 'Listed count', hint: 'Times added to a list' },
  { key: 'account_age_days', label: 'Account age (days)', hint: 'Roughly, since join date' },
]

export default function StatsForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialState)
  const [error, setError] = useState('')

  const update = (key, value) => setForm((f) => ({ ...f, [key]: value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.username.trim()) {
      setError('Enter a username to label this check.')
      return
    }
    setError('')
    const payload = {
      ...form,
      followers_count: Number(form.followers_count) || 0,
      friends_count: Number(form.friends_count) || 0,
      listed_count: Number(form.listed_count) || 0,
      favourites_count: Number(form.favourites_count) || 0,
      statuses_count: Number(form.statuses_count) || 0,
      account_age_days: Number(form.account_age_days) || 1,
    }
    onSubmit(payload)
  }

  return (
    <form className="stats-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          id="username"
          type="text"
          placeholder="e.g. some_handle"
          value={form.username}
          onChange={(e) => update('username', e.target.value)}
        />
      </div>

      <div className="form-grid">
        {FIELDS.map(({ key, label, hint }) => (
          <div className="form-group" key={key}>
            <label htmlFor={key}>{label}</label>
            <input
              id={key}
              type="number"
              min="0"
              inputMode="numeric"
              placeholder="0"
              value={form[key]}
              onChange={(e) => update(key, e.target.value)}
            />
            <span className="field-hint">{hint}</span>
          </div>
        ))}
      </div>

      <div className="form-group">
        <label htmlFor="bio">Bio / description</label>
        <textarea
          id="bio"
          rows={2}
          placeholder="Paste their bio text (optional)"
          value={form.bio}
          onChange={(e) => update('bio', e.target.value)}
        />
      </div>

      <div className="checkbox-row">
        <label className="checkbox">
          <input
            type="checkbox"
            checked={form.verified}
            onChange={(e) => update('verified', e.target.checked)}
          />
          Verified
        </label>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={form.default_profile_image}
            onChange={(e) => update('default_profile_image', e.target.checked)}
          />
          Default profile photo
        </label>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={form.default_profile}
            onChange={(e) => update('default_profile', e.target.checked)}
          />
          Default theme/profile
        </label>
      </div>

      {error && <p className="form-error">{error}</p>}

      <button type="submit" className="scan-btn" disabled={loading}>
        {loading ? 'Scanning…' : 'Run Detection'}
      </button>
    </form>
  )
}
