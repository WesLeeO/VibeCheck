from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tweet_fetcher import get_recent_tweets
from sentiment import analyze_sentiment
from tweet_analyzer import TweetAnalyzer
from profile_fetcher import get_profile_info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/analyze/{username}")
def analyze_user(username: str):
    try:
        profile_info = get_profile_info(username)
        tweets = get_recent_tweets(username)
        analyzer = TweetAnalyzer()
        results = analyzer.analyze_tweets(tweets)
        return {"username": username, "results": results, 'info': profile_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    