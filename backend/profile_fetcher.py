import requests

from dotenv import load_dotenv
import os

load_dotenv()  # Load env vars from .env

twitter_api_key = os.getenv("TWITTER_API_KEY")

def get_profile_info(username):
    url = "https://api.twitterapi.io/twitter/user/info"
    headers = {"X-API-Key": twitter_api_key}
    params = {"userName": username}
    info = {}
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        data = response.json()
        info['name'] = data['data']['name']
        info['profile_picture'] = data['data']['profilePicture']
        info['description'] = data['data']['description']

    except Exception as e:
        # Catching any other unexpected errors
        print(f'Unexpected error {e}')
    return info
