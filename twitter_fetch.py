import tweepy

def fetch_tweets(username, count=10):
    tweets = api.user_timeline(screen_name=username, count=count, tweet_mode="extended")
    return [tweet.full_text for tweet in tweets]
