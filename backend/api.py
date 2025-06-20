from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tweet_fetcher import get_recent_tweets
from sentiment import analyze_sentiment
from tweet_analyzer import TweetAnalyzer
from profile_fetcher import get_profile_info
import uvicorn 
import os

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
        word_cloud_encoding = analyzer.word_cloud([tweet for tweet, _ in tweets])
        return {"username": username, "results": results, 'info': profile_info, 'word_cloud': f"data:image/png;base64,{word_cloud_encoding}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    