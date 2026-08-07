# Signal — Twitter/X Bot Detector

A machine learning tool that estimates whether a Twitter/X account is a bot,
based on public account-level signals (followers, following, activity,
profile completeness) — no live Twitter API access required.

> **Why no live API?** X (formerly Twitter) discontinued free-tier read
> access to its API in 2026. Rather than depend on paid API access, this
> tool works from account stats you enter manually (all of which are
> visible on any public profile page), and runs them through a model
> trained on a real labeled dataset of ~2,800 Twitter accounts.

## Live demo

- Frontend: _add your deployed Vercel URL here_
- Backend API: _add your deployed Render URL here_

## Architecture

```
bot-detection/
├── backend/            FastAPI + scikit-learn
│   ├── main.py         API endpoints (/api/check, /api/history)
│   ├── features.py     Feature engineering + explanation logic
│   ├── train_model.py  Model training script
│   ├── data/            Training dataset (2,797 labeled accounts)
│   └── model/           Saved trained model (bot_model.joblib)
└── frontend/            React (Vite)
    └── src/              Form, result gauge, history view
```

## Model

- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Dataset:** 2,797 labeled Twitter accounts (1,476 human / 1,321 bot),
  with real features — followers, friends, favourites, statuses, verified
  status, default profile flags.
- **Engineered features:** followers-to-friends ratio, tweets-to-followers
  (log-scaled reach), favourites-per-tweet, bio length, screen-name patterns.
- **Test-set performance:**
  - Accuracy: 91.3%
  - Precision: 93.2%
  - Recall: 87.9%
  - ROC AUC: 97.2%

Run `python train_model.py` inside `backend/` to retrain and see the full
report, including per-feature importance.

## Running locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```
API runs at `http://localhost:8000`. Interactive docs at `/docs`.

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
App runs at `http://localhost:5173`.

## Deployment

**Backend (Render — free tier):**
1. New Web Service → connect this repo, root directory `backend`
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable `ALLOWED_ORIGINS` = your deployed frontend URL

**Frontend (Vercel):**
1. Import this repo, root directory `frontend`
2. Framework preset: Vite
3. Add environment variable `VITE_API_URL` = your deployed backend URL

## Tech stack

Python, FastAPI, scikit-learn, pandas, SQLite · React (Vite) · Render + Vercel

---
Built by Dayasri K
