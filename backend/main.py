"""
main.py — FastAPI backend for the Twitter/X Bot Detector.

Endpoints:
  POST /api/check      -> run a prediction on manually entered account stats
  GET  /api/history     -> list past checks (most recent first)
  DELETE /api/history    -> clear history
  GET  /api/health      -> simple health check for deployment platforms
"""

import os
import sqlite3
import time
from contextlib import contextmanager

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from features import build_feature_vector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "bot_model.joblib")
DB_PATH = os.path.join(BASE_DIR, "history.db")

app = FastAPI(title="Twitter Bot Detector API")

# Allow the deployed frontend (and local dev) to call this API.
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bundle = joblib.load(MODEL_PATH)
MODEL = bundle["model"]
FEATURE_COLUMNS = bundle["features"]
TRAIN_METRICS = bundle["metrics"]


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                is_bot INTEGER,
                confidence REAL,
                checked_at REAL,
                top_reasons TEXT
            )
            """
        )


init_db()


class CheckRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    followers_count: int = Field(..., ge=0)
    friends_count: int = Field(..., ge=0)
    listed_count: int = Field(0, ge=0)
    favourites_count: int = Field(0, ge=0)
    statuses_count: int = Field(0, ge=0)
    verified: bool = False
    default_profile: bool = False
    default_profile_image: bool = False
    bio: str = ""
    account_age_days: int = Field(365, ge=0)


class CheckResponse(BaseModel):
    username: str
    is_bot: bool
    confidence: float
    label: str
    top_reasons: list[str]


@app.get("/api/health")
def health():
    return {"status": "ok", "model_metrics": TRAIN_METRICS}


@app.post("/api/check", response_model=CheckResponse)
def check_bot(payload: CheckRequest):
    try:
        vector, reasons = build_feature_vector(payload.dict(), MODEL, FEATURE_COLUMNS)
        proba = MODEL.predict_proba([vector])[0]
        bot_confidence = float(proba[1])
        is_bot = bot_confidence >= 0.5

        with get_db() as conn:
            conn.execute(
                "INSERT INTO history (username, is_bot, confidence, checked_at, top_reasons) VALUES (?, ?, ?, ?, ?)",
                (
                    payload.username,
                    int(is_bot),
                    bot_confidence,
                    time.time(),
                    "; ".join(reasons),
                ),
            )

        return CheckResponse(
            username=payload.username,
            is_bot=is_bot,
            confidence=round(bot_confidence if is_bot else 1 - bot_confidence, 4),
            label="Likely Bot" if is_bot else "Likely Human",
            top_reasons=reasons,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/history")
def get_history(limit: int = 20):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT username, is_bot, confidence, checked_at, top_reasons FROM history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


@app.delete("/api/history")
def clear_history():
    with get_db() as conn:
        conn.execute("DELETE FROM history")
    return {"status": "cleared"}
