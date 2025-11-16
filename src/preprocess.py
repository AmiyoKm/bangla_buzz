import pandas as pd
from bnlp.corpus import _stopwords
import os

def preprocess_data():
    """
    Reads raw news data, cleans it, removes stopwords, and saves the result.
    """
    input_path = "data/raw_data.csv"
    output_path = "data/clean_news.csv"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run the scraper first with 'uv run python3 main.py --scrape'")
        return

    df = pd.read_csv(input_path)

    # Fill missing values
    df["Title"] = df["Title"].fillna("")
    if "Text" in df.columns:
        df["Text"] = df["Text"].fillna("")

    # Remove stopwords from title
    bengali_stopwords = _stopwords.bengali_stopwords
    df["Title"] = df["Title"].apply(
        lambda x: " ".join([word for word in str(x).split() if word not in bengali_stopwords])
    )

    # Save cleaned data
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Preprocessing complete. Cleaned data saved to {output_path}")

if __name__ == "__main__":
    preprocess_data()
