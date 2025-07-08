from crypto_sentiment_analyzer.twitter_api import get_user_ids, fetch_all_tweets
from crypto_sentiment_analyzer.preprocess import clean_tweets
from crypto_sentiment_analyzer.sentiment import analyze_sentiment
from crypto_sentiment_analyzer.export import export_to_csv  # Uncomment if implemented
from crypto_sentiment_analyzer.visualization import plot_sentiment_results, plot_detailed_sentiment_analysis  # Uncomment if implemented

def main():
    # 1. Set up target usernames
    usernames = ["cz_binance", "elonmusk", "jack", "saylor", "VitalikButerin", "michael_saylor"]

    # 2. Get user IDs
    user_ids = get_user_ids(usernames)

    # 3. Fetch tweets for all users
    all_tweets = fetch_all_tweets(user_ids)

    # 4. Preprocess tweets
    cleaned_df = clean_tweets(all_tweets)

    # 5. Analyze sentiment
    sentiment_df = analyze_sentiment(cleaned_df)

    # 6. Export results (uncomment if implemented)
    export_to_csv(sentiment_df, "crypto_sentiment_results.csv")

    # 7. Visualize results (uncomment if implemented)
    plot_sentiment_results(sentiment_df)
    plot_detailed_sentiment_analysis(sentiment_df)

if __name__ == "__main__":
    main()
