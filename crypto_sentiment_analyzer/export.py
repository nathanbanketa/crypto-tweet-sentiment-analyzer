# =============================================================================
# 10. EXPORT RESULTS
# =============================================================================

def export_to_csv(df, filename="crypto_sentiment_results.csv"):
    df.to_csv(filename, index=False)
    print(f"Results saved to '{filename}'")
    print("\n=== FINAL SUMMARY ===")
    print(f"Total tweets analyzed: {len(df)}")
    print(f"Users analyzed: {len(df['username'].unique())}")
    print(f"Date range: {df['created_at'].min()} to {df['created_at'].max()}")
    print(f"Overall sentiment: {df['compound_sentiment'].mean():.3f}")
    print("\nAnalysis complete! Check the generated visualizations and CSV file.")