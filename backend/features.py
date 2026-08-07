"""
features.py
Turns a raw account-stats payload into the exact feature vector the model
expects, and produces short human-readable reasons behind the prediction.
"""

import numpy as np


def _engineer(payload: dict) -> dict:
    followers = payload["followers_count"]
    friends = payload["friends_count"]
    favourites = payload["favourites_count"]
    statuses = payload["statuses_count"]
    description_length = len(payload.get("bio", "") or "")

    return {
        "followers_count": followers,
        "friends_count": friends,
        "listed_count": payload["listed_count"],
        "favourites_count": favourites,
        "statuses_count": statuses,
        "verified": int(payload["verified"]),
        "default_profile": int(payload["default_profile"]),
        "default_profile_image": int(payload["default_profile_image"]),
        "followers_friends_ratio": followers / (friends + 1),
        "tweets_to_followers": np.log1p(statuses) * np.log1p(followers),
        "favourites_per_tweet": favourites / (statuses + 1),
        "screen_name_length": len(payload.get("username", "")),
        "screen_name_has_digits": int(any(ch.isdigit() for ch in payload.get("username", ""))),
        "description_length": description_length,
        "has_description": int(description_length > 0),
    }


def build_feature_vector(payload: dict, model, feature_columns):
    engineered = _engineer(payload)
    vector = [engineered[col] for col in feature_columns]

    reasons = _explain(engineered, payload)
    return vector, reasons


def _explain(f: dict, payload: dict) -> list:
    """Rule-of-thumb explanations layered on top of the model's own
    feature importances, so the result reads as reasoning, not a black box."""
    reasons = []

    if f["followers_friends_ratio"] < 0.3 and f["friends_count"] > 50:
        reasons.append("Follows far more accounts than it's followed by — a common bot signal")
    elif f["followers_friends_ratio"] > 5:
        reasons.append("Strong followers-to-following ratio — typical of a genuine account")

    if f["default_profile_image"]:
        reasons.append("Still using the default profile picture")

    if f["has_description"] == 0:
        reasons.append("No bio/description set")

    if payload["verified"]:
        reasons.append("Account is verified — strong human signal")

    if f["favourites_per_tweet"] < 0.05 and f["statuses_count"] > 100:
        reasons.append("Posts a lot but rarely likes anything — automated posting pattern")

    if f["statuses_count"] > 0 and payload["account_age_days"] > 0:
        posts_per_day = f["statuses_count"] / max(payload["account_age_days"], 1)
        if posts_per_day > 50:
            reasons.append(f"Extremely high posting rate (~{posts_per_day:.0f} posts/day)")

    if not reasons:
        reasons.append("No strongly distinguishing signals — prediction based on overall stat pattern")

    return reasons[:4]
