# =============================================================================
# SENTIMENT ANALYSIS
# =============================================================================

# Requires: pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_sentiment(text):
    """Get sentiment scores for text"""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores

def categorize_sentiment(compound):
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_sentiment(df):
    """Takes a DataFrame, adds sentiment columns, and returns the DataFrame."""
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = df['cleaned_text'].apply(lambda text: analyzer.polarity_scores(text))
    df['compound_sentiment'] = sentiment_scores.apply(lambda x: x['compound'])
    df['positive_sentiment'] = sentiment_scores.apply(lambda x: x['pos'])
    df['negative_sentiment'] = sentiment_scores.apply(lambda x: x['neg'])
    df['neutral_sentiment'] = sentiment_scores.apply(lambda x: x['neu'])
    df['sentiment_category'] = df['compound_sentiment'].apply(categorize_sentiment)
    return df
