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