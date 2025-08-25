import requests
import time
from dotenv import load_dotenv
import os

load_dotenv
BEARER_TOKEN = os.getenv("API_KEY")

# =============================================================================
# TWITTER API AUTHENTICATION
# =============================================================================
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'User-Agent': 'CryptoSentimentBot/1.0'
}

print("API headers configured!")

# =============================================================================
# TARGET CRYPTO ACCOUNTS
# =============================================================================

usernames = ["cz_binance", "BTCTN"]
print(f"Targeting {len(usernames)} crypto influencers: {usernames}")

# =============================================================================
# GET USER IDS FROM USERNAMES
# =============================================================================

def get_user_id(username):
    """Get user ID from username"""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['data']['id']
    else:
        print(f"Error getting user ID for {username}: {response.status_code}")
        return None


def get_user_ids(usernames):
    """Get user IDs for a list of usernames. Returns dict {username: user_id}"""
    user_ids = {}
    for username in usernames:
        user_id = get_user_id(username)
        if user_id:
            user_ids[username] = user_id
        time.sleep(1)  # Rate limiting
    return user_ids


def fetch_tweets(user_id, username, max_results=10):
    """Fetch tweets for a specific user"""
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text,public_metrics",
        "exclude": "retweets,replies"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get('data', [])
        return [(tweet['text'], tweet['created_at'], username) for tweet in data]
    else:
        print(f"Error fetching tweets for {username}: {response.status_code}")
        return []


def fetch_all_tweets(user_ids, max_results=10):
    """Fetch tweets for all users in user_ids dict. Returns list of (text, created_at, username)"""
    all_tweets = []
    for username, user_id in user_ids.items():
        print(f"Fetching tweets for {username}...")
        tweets = fetch_tweets(user_id, username, max_results=max_results)
        all_tweets.extend(tweets)
        time.sleep(2)  # Rate limiting
    return all_tweets