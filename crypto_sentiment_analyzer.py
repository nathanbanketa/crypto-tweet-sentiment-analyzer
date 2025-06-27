#!/usr/bin/env python3
"""
Crypto Tweet Sentiment Analyzer
Analyzes sentiment from major crypto influencers on Twitter
"""

# =============================================================================
# 1. IMPORTS AND SETUP
# =============================================================================

import requests
import pandas as pd
import time
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Set style for better plots
plt.style.use('default')
sns.set_palette("husl")

print("All imports successful!")

# =============================================================================
# 2. TWITTER API AUTHENTICATION
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

# =============================================================================
# 6. CREATE DATAFRAME AND PREPROCESS TWEETS
# =============================================================================

# Create DataFrame
df = pd.DataFrame(all_tweets, columns=['text', 'created_at', 'username'])
df['created_at'] = pd.to_datetime(df['created_at'])

def clean_tweet(text):
    """Clean tweet text by removing URLs, mentions, and hashtags"""
    if pd.isna(text):
        return ""
    text = re.sub(r"http\S+|@\S+|#\S+", "", text)  # Remove URLs, mentions, and hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()

df['cleaned_text'] = df['text'].apply(clean_tweet)
df = df[df['cleaned_text'].str.len() > 10]  # Remove very short tweets

print(f"DataFrame shape: {df.shape}")
print(df.head())

# =============================================================================
# 7. SENTIMENT ANALYSIS
# =============================================================================

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment
def get_sentiment(text):
    """Get sentiment scores for text"""
    scores = analyzer.polarity_scores(text)
    return scores

# Apply sentiment analysis
sentiment_scores = df['cleaned_text'].apply(get_sentiment)
df['compound_sentiment'] = sentiment_scores.apply(lambda x: x['compound'])
df['positive_sentiment'] = sentiment_scores.apply(lambda x: x['pos'])
df['negative_sentiment'] = sentiment_scores.apply(lambda x: x['neg'])
df['neutral_sentiment'] = sentiment_scores.apply(lambda x: x['neu'])

# Add sentiment category
def categorize_sentiment(compound):
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

df['sentiment_category'] = df['compound_sentiment'].apply(categorize_sentiment)

print("Sentiment Analysis Complete!")
print(df[['username', 'cleaned_text', 'compound_sentiment', 'sentiment_category']].head())

# =============================================================================
# 8. VISUALIZATIONS
# =============================================================================

# 1. Overall sentiment distribution
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sentiment_counts = df['sentiment_category'].value_counts()
colors = ['#2E8B57', '#FF6B6B', '#4682B4']
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
plt.title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')

# 2. Sentiment by user
plt.subplot(2, 2, 2)
user_sentiment = df.groupby('username')['compound_sentiment'].mean().sort_values()
bars = plt.bar(range(len(user_sentiment)), user_sentiment.values, 
               color=['red' if x < 0 else 'green' if x > 0 else 'gray' for x in user_sentiment.values])
plt.xticks(range(len(user_sentiment)), user_sentiment.index, rotation=45)
plt.title('Average Sentiment by User', fontsize=14, fontweight='bold')
plt.ylabel('Compound Sentiment Score')
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)

# 3. Sentiment over time
plt.subplot(2, 2, 3)
df_sorted = df.sort_values('created_at')
plt.scatter(df_sorted['created_at'], df_sorted['compound_sentiment'], 
           alpha=0.6, c=df_sorted['compound_sentiment'], cmap='RdYlGn')
plt.title('Sentiment Over Time', fontsize=14, fontweight='bold')
plt.ylabel('Compound Sentiment Score')
plt.xticks(rotation=45)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)

# 4. Sentiment distribution histogram
plt.subplot(2, 2, 4)
plt.hist(df['compound_sentiment'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Sentiment Score Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Compound Sentiment Score')
plt.ylabel('Frequency')
plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Detailed sentiment analysis by user
plt.figure(figsize=(15, 10))

# Sentiment breakdown by user
user_sentiment_breakdown = df.groupby(['username', 'sentiment_category']).size().unstack(fill_value=0)

ax = user_sentiment_breakdown.plot(kind='bar', stacked=True, 
                                   color=['#FF6B6B', '#4682B4', '#2E8B57'],
                                   figsize=(12, 6))
plt.title('Sentiment Breakdown by User', fontsize=14, fontweight='bold')
plt.xlabel('User', fontsize=12)
plt.ylabel('Number of Tweets', fontsize=12)
plt.legend(title='Sentiment Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Summary statistics
print("\n=== SENTIMENT ANALYSIS SUMMARY ===")
print(f"Total tweets analyzed: {len(df)}")
print(f"Average sentiment score: {df['compound_sentiment'].mean():.3f}")
print(f"Sentiment standard deviation: {df['compound_sentiment'].std():.3f}")
print("\nSentiment by user:")
for user in df['username'].unique():
    user_data = df[df['username'] == user]
    avg_sentiment = user_data['compound_sentiment'].mean()
    tweet_count = len(user_data)
    print(f"{user}: {avg_sentiment:.3f} ({tweet_count} tweets)")

# =============================================================================
# 9. CRYPTO-SPECIFIC SENTIMENT ANALYSIS
# =============================================================================

# Filter for crypto-related tweets
crypto_keywords = ['bitcoin', 'btc', 'crypto', 'cryptocurrency', 'eth', 'ethereum', 
                  'blockchain', 'defi', 'nft', 'altcoin', 'hodl', 'moon', 'pump', 'dump']

def is_crypto_related(text):
    """Check if tweet contains crypto-related keywords"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in crypto_keywords)

df['crypto_related'] = df['cleaned_text'].apply(is_crypto_related)
crypto_tweets = df[df['crypto_related'] == True]

print(f"Crypto-related tweets: {len(crypto_tweets)} out of {len(df)} total tweets")

# Crypto sentiment analysis
if len(crypto_tweets) > 0:
    plt.figure(figsize=(15, 6))
    
    plt.subplot(1, 2, 1)
    crypto_sentiment = crypto_tweets.groupby('username')['compound_sentiment'].mean().sort_values()
    bars = plt.bar(range(len(crypto_sentiment)), crypto_sentiment.values,
                   color=['red' if x < 0 else 'green' if x > 0 else 'gray' for x in crypto_sentiment.values])
    plt.xticks(range(len(crypto_sentiment)), crypto_sentiment.index, rotation=45)
    plt.title('Crypto Sentiment by User', fontsize=14, fontweight='bold')
    plt.ylabel('Average Sentiment Score')
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.subplot(1, 2, 2)
    crypto_sentiment_counts = crypto_tweets['sentiment_category'].value_counts()
    plt.pie(crypto_sentiment_counts.values, labels=crypto_sentiment_counts.index, 
            autopct='%1.1f%%', colors=['#2E8B57', '#FF6B6B', '#4682B4'])
    plt.title('Crypto Tweet Sentiment Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print("\n=== CRYPTO SENTIMENT SUMMARY ===")
    print(f"Average crypto sentiment: {crypto_tweets['compound_sentiment'].mean():.3f}")
    print("\nTop positive crypto tweets:")
    top_positive = crypto_tweets.nlargest(3, 'compound_sentiment')[['username', 'cleaned_text', 'compound_sentiment']]
    for _, row in top_positive.iterrows():
        print(f"{row['username']}: {row['compound_sentiment']:.3f} - {row['cleaned_text'][:100]}...")
    
    print("\nTop negative crypto tweets:")
    top_negative = crypto_tweets.nsmallest(3, 'compound_sentiment')[['username', 'cleaned_text', 'compound_sentiment']]
    for _, row in top_negative.iterrows():
        print(f"{row['username']}: {row['compound_sentiment']:.3f} - {row['cleaned_text'][:100]}...")
else:
    print("No crypto-related tweets found!")

# =============================================================================
# 10. EXPORT RESULTS
# =============================================================================

# Save results to CSV
df.to_csv('crypto_sentiment_results.csv', index=False)
print("Results saved to 'crypto_sentiment_results.csv'")

# Display final summary
print("\n=== FINAL SUMMARY ===")
print(f"Total tweets analyzed: {len(df)}")
print(f"Users analyzed: {len(df['username'].unique())}")
print(f"Date range: {df['created_at'].min()} to {df['created_at'].max()}")
print(f"Overall sentiment: {df['compound_sentiment'].mean():.3f}")
print(f"Crypto-related tweets: {len(crypto_tweets)}")

print("\nAnalysis complete! Check the generated visualizations and CSV file.") 