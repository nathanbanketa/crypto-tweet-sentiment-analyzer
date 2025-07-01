# =============================================================================
# 6. CREATE DATAFRAME AND PREPROCESS TWEETS
# =============================================================================

import pandas as pd
import re

def clean_tweet(text):
    """Clean tweet text by removing URLs, mentions, and hashtags"""
    if pd.isna(text):
        return ""
    text = re.sub(r"http\S+|@\S+|#\S+", "", text)  # Remove URLs, mentions, and hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()


def clean_tweets(tweets):
    """Takes a list of (text, created_at, username) and returns a cleaned DataFrame."""
    columns = ['text', 'created_at', 'username']
    if tweets:
        df = pd.DataFrame.from_records(tweets, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['cleaned_text'] = df['text'].apply(clean_tweet)
    df = df[df['cleaned_text'].str.len() > 10]  # Remove very short tweets
    return df