import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler


def detect_outliers():
    input_path = "data/news_with_sentiment.csv"
    output_path = "data/news_with_outliers.csv"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run sentiment analysis first.")
        return

    df = pd.read_csv(input_path)

    if "Title" not in df.columns or "Sentiment_Score" not in df.columns:
        print("Error: 'Title' or 'Sentiment_Score' column not found.")
        return

    df["Title"] = df["Title"].astype(str).fillna("")

    # 1. Create TF-IDF vectors
    vectorizer = TfidfVectorizer(max_features=1000, use_idf=True)

    # Handle case where there are no titles to vectorize
    if df["Title"].empty:
        print("No titles to analyze for outliers.")
        df["is_outlier"] = False
        df.to_csv(output_path, index=False, encoding="utf-8")
        return

    tfidf_matrix = vectorizer.fit_transform(df["Title"])

    # 2. Combine with sentiment scores
    sentiment_scores = df["Sentiment_Score"].values.reshape(-1, 1)

    if tfidf_matrix.shape[0] == 0:
        print("Error: TF-IDF matrix is empty. Cannot perform outlier detection.")
        df["is_outlier"] = False
        df.to_csv(output_path, index=False, encoding="utf-8")
        return

    features = np.hstack([tfidf_matrix.toarray(), sentiment_scores])

    # 3. Scale the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # 4. Apply Isolation Forest
    # 'contamination' determines the proportion of outliers. 'auto' is a good default.
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    clusters = iso_forest.fit_predict(scaled_features)

    # Outliers are labeled as -1 by IsolationForest as well
    df['is_outlier'] = clusters == -1

    # 5. Save the results
    df.to_csv(output_path, index=False, encoding="utf-8")

    num_outliers = df["is_outlier"].sum()
    print(f"Outlier detection complete. Found {num_outliers} outliers.")
    print(f"Data with outlier information saved to {output_path}")


if __name__ == "__main__":
    detect_outliers()
