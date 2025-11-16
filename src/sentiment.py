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
    def get_sentiment_details(text):
        if not text.strip():
            return 'Neutral', 0.0
        result = sentiment_pipeline(text)[0]
        return result['label'], result['score']

    # Get both label and score in one go
    details = df['Title'].apply(get_sentiment_details)
    
    # Map labels and assign to columns
    label_map = {'LABEL_1': 'Positive', 'LABEL_0': 'Negative', 'neutral': 'Neutral'}
    df['Sentiment'] = details.apply(lambda x: label_map.get(x[0], 'Unknown'))
    df['Sentiment_Score'] = details.apply(lambda x: x[1])

    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Sentiment analysis complete. Data with sentiment saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment()
