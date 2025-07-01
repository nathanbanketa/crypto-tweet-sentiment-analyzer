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
sentiment_scores = df['cleaned_text'].apply(get_sentiment)  # type: ignore
df['compound_sentiment'] = sentiment_scores.apply(lambda x: x['compound'])  # type: ignore
df['positive_sentiment'] = sentiment_scores.apply(lambda x: x['pos'])  # type: ignore
df['negative_sentiment'] = sentiment_scores.apply(lambda x: x['neg'])  # type: ignore
df['neutral_sentiment'] = sentiment_scores.apply(lambda x: x['neu'])  # type: ignore

# Add sentiment category
def categorize_sentiment(compound):
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

df['sentiment_category'] = df['compound_sentiment'].apply(categorize_sentiment)  # type: ignore

print("Sentiment Analysis Complete!")
print(df[['username', 'cleaned_text', 'compound_sentiment', 'sentiment_category']].head())  # type: ignore
