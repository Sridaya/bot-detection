"""
train_model.py
Trains a Random Forest classifier on the Twitter bot-detection dataset
(2,797 labeled accounts: followers, friends, favourites, statuses, verified, etc.)
Saves the trained model + feature list to model/bot_model.joblib
"""

import re
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, classification_report
import joblib

DATA_PATH = "data/bot_dataset.csv"
MODEL_PATH = "model/bot_model.joblib"


def clean_text(val):
    """Strip stray quote characters left over from the raw export."""
    if pd.isna(val):
        return ""
    return re.sub(r'^"+|"+$', "", str(val)).strip()


def to_bool(val):
    return str(val).strip().upper() == "TRUE"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ["screen_name", "name", "description"]:
        df[col] = df[col].apply(clean_text)

    numeric_cols = ["followers_count", "friends_count", "listed_count", "favourites_count", "statuses_count"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["verified"] = df["verified"].apply(to_bool).astype(int)
    df["default_profile"] = df["default_profile"].apply(to_bool).astype(int)
    df["default_profile_image"] = df["default_profile_image"].apply(to_bool).astype(int)

    # --- Engineered features (mirrors patterns used in published bot-detection research) ---
    df["followers_friends_ratio"] = df["followers_count"] / (df["friends_count"] + 1)
    df["tweets_to_followers"] = np.log1p(df["statuses_count"]) * np.log1p(df["followers_count"])
    df["favourites_per_tweet"] = df["favourites_count"] / (df["statuses_count"] + 1)
    df["screen_name_length"] = df["screen_name"].str.len()
    df["screen_name_has_digits"] = df["screen_name"].str.contains(r"\d", regex=True).astype(int)
    df["description_length"] = df["description"].str.len()
    df["has_description"] = (df["description_length"] > 0).astype(int)

    return df


FEATURE_COLUMNS = [
    "followers_count",
    "friends_count",
    "listed_count",
    "favourites_count",
    "statuses_count",
    "verified",
    "default_profile",
    "default_profile_image",
    "followers_friends_ratio",
    "tweets_to_followers",
    "favourites_per_tweet",
    "screen_name_length",
    "screen_name_has_digits",
    "description_length",
    "has_description",
]


def main():
    raw = pd.read_csv(DATA_PATH)
    df = build_features(raw)
    df["bot"] = pd.to_numeric(df["bot"], errors="coerce").fillna(0).astype(int)

    X = df[FEATURE_COLUMNS]
    y = df["bot"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }

    print("=== Model evaluation ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print()
    print(classification_report(y_test, y_pred, target_names=["human", "bot"]))

    importances = sorted(
        zip(FEATURE_COLUMNS, model.feature_importances_), key=lambda x: -x[1]
    )
    print("=== Feature importances ===")
    for name, imp in importances:
        print(f"{name}: {round(imp, 4)}")

    joblib.dump({"model": model, "features": FEATURE_COLUMNS, "metrics": metrics}, MODEL_PATH)
    print(f"\nSaved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
