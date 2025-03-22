from fastapi import FastAPI
from twitter_fetch import fetch_tweets
from ml_model import predict_bot

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Twitter Bot Detection API"}

@app.get("/check-bot/")
def check_bot(username: str):
    tweets = fetch_tweets(username)
    followers = 100  # Replace with real data from Twitter API
    following = 50   # Replace with real data
    tweet_count = len(tweets)

    is_bot = predict_bot(followers, following, tweet_count)
    return {"username": username, "is_bot": bool(is_bot)}
