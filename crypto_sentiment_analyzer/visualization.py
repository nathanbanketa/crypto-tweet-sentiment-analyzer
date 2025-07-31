# =============================================================================
# VISUALIZATIONS
# =============================================================================

import matplotlib.pyplot as plt

def plot_sentiment_results(df):
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

def plot_detailed_sentiment_analysis(df):
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
