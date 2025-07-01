# =============================================================================
# TWITTER API AUTHENTICATION
# =============================================================================

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEl72QEAAAAA%2FLoqTtdehu8qkfZY1oqZB6Rz6yg%3DMI0YdLTx5GH0RB3tjMfi7DqTB4GNFyie8RYEZtC6J22beoFxgd"

headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'User-Agent': 'CryptoSentimentBot/1.0'
}

print("API headers configured!")

# =============================================================================
# 3. TARGET CRYPTO ACCOUNTS
# =============================================================================

usernames = ["cz_binance", "elonmusk", "jack", "saylor", "VitalikButerin", "michael_saylor"]
print(f"Targeting {len(usernames)} crypto influencers: {usernames}")

# =============================================================================
# 4. GET USER IDS FROM USERNAMES
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

# Get user IDs
user_ids = {}
for username in usernames:
    user_id = get_user_id(username)
    if user_id:
        user_ids[username] = user_id
    time.sleep(1)  # Rate limiting

print("User IDs:", user_ids)

# =============================================================================
# 5. FETCH TWEETS
# =============================================================================

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

# Fetch tweets for all users
all_tweets = []
for username, user_id in user_ids.items():
    print(f"Fetching tweets for {username}...")
    tweets = fetch_tweets(user_id, username)
    all_tweets.extend(tweets)
    time.sleep(2)  # Rate limiting

print(f"Total tweets fetched: {len(all_tweets)}")