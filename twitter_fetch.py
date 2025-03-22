import tweepy

API_KEY = "3AvxDwIQrQUDuViKbFxzUMuPw"
API_SECRET_KEY ="NRxVq6kaCZhzZxyLVTT1KjaKVzpuKrp2L91Y8Epdz7v4rfKx44" 
ACCESS_TOKEN = "1892943787795890176-FbL7UbhFPQzDaVgWdVKkDnxkEMr7LN"
ACCESS_SECRET = "6ISHq8d2CduCVpZd2oK7MFkpMC92vZszCTlrfssezuuwf"

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def fetch_tweets(username, count=10):
    tweets = api.user_timeline(screen_name=username, count=count, tweet_mode="extended")
    return [tweet.full_text for tweet in tweets]
