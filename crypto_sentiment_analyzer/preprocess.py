# =============================================================================
# 6. CREATE DATAFRAME AND PREPROCESS TWEETS
# =============================================================================

# Create DataFrame
df = pd.DataFrame(all_tweets, columns=['text', 'created_at', 'username'])  # type: ignore
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