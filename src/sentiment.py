import pandas as pd
from transformers import pipeline
import os

def analyze_sentiment():
    input_path = "data/clean_news.csv"
    output_path = "data/news_with_sentiment.csv"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run the preprocessing step first.")
        return

    df = pd.read_csv(input_path)

    if 'Title' not in df.columns:
        print("Error: 'Title' column not found in clean_news.csv.")
        return

    # Ensure 'Title' column is string type and handle NaN values
    df['Title'] = df['Title'].astype(str).fillna('')

    # Initialize the sentiment analysis pipeline
    sentiment_pipeline = pipeline(
        task="sentiment-analysis",
        model="DipsankarSinha/bangla-sentiment-analysis-v2_2025",
        tokenizer="csebuetnlp/banglabert",
        framework="pt",
        use_fast=False
    )

    # Perform sentiment analysis on each title
    df['Sentiment'] = df['Title'].apply(
        lambda x: sentiment_pipeline(x)[0]['label'] if x.strip() else 'neutral'
    )
    df['Sentiment_Score'] = df['Title'].apply(
        lambda x: sentiment_pipeline(x)[0]['score'] if x.strip() else 0.0
    )

    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Sentiment analysis complete. Data with sentiment saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment()
