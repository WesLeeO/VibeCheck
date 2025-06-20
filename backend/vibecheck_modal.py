import modal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from modal import App, asgi_app, Secret
from tweet_fetcher import get_recent_tweets
from sentiment import analyze_sentiment
from tweet_analyzer import TweetAnalyzer
from profile_fetcher import get_profile_info

# Create your Modal App
app = App("vibecheck-nlp")
fapp = FastAPI()

fapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the image with required dependencies
image = (
    modal.Image.debian_slim()
    .pip_install("transformers", "torch", "numpy", "fastapi", "uvicorn", "pydantic", "python-dotenv", "matplotlib", "wordcloud")
    .add_local_dir(".", remote_path="/root/vibecheck")  # Mounts the current directory to the container
)

twitter_secret = Secret.from_name("twitter-api-key")

@fapp.get("/analyze/{username}")
async def analyze_user(username: str):
    try:
        profile_info = get_profile_info(username)
        tweets = get_recent_tweets(username)
        analyzer = TweetAnalyzer()
        results = analyzer.analyze_tweets(tweets)
        word_cloud_encoding = analyzer.word_cloud([tweet for tweet, _ in tweets])
        return {"username": username, "results": results, 'info': profile_info, 'word_cloud': f"data:image/png;base64,{word_cloud_encoding}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.function(
    gpu="any",
    image=image,
    secrets=[twitter_secret],  # This makes the secret available to os.getenv()
)
@asgi_app()
def fastapi_app():
    return fapp