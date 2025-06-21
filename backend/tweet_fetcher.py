import requests

from dotenv import load_dotenv
import os

load_dotenv()  # Load env vars from .env

twitter_api_key = os.getenv("TWITTER_API_KEY")



def get_recent_tweets(username, limit = 10):
    url = "https://api.twitterapi.io/twitter/user/last_tweets"
    headers = {"X-API-Key": twitter_api_key}
    params = {"userName": username}
    tweets = []
    while len(tweets) <= limit:
        try:
            response = requests.request("GET", url, headers=headers, params=params)
            data = response.json()
            print(f'data tweet {data}', flush=True)
            for tweet in data['data']['tweets']:
                tweets.append((tweet['text'], tweet['createdAt']))
            if data['has_next_page']:
                params['cursor'] = data['next_cursor']
            else:
                break
        except Exception as e:
            # Catching any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            break
    return tweets