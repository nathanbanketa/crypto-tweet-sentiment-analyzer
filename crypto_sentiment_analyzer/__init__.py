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