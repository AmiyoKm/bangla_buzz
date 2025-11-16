import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

def show_dashboard():
    st.set_page_config(page_title="BanglaBuzz Dashboard", layout="wide")
    st.title("BanglaBuzz: News Trend and Sentiment Analysis")

    # --- File Paths ---
    topics_file = "data/topics.json"
    sentiment_file = "data/news_with_sentiment.csv"
    outliers_file = "data/news_with_outliers.csv"

    # --- Check if data files exist ---
    if not all(os.path.exists(f) for f in [topics_file, sentiment_file, outliers_file]):
        st.error("Data files not found. Please run the full pipeline first (`uv run python3 main.py --all`)")
        return

    # --- Load Data ---
    try:
        with open(topics_file, 'r', encoding='utf-8') as f:
            topics = json.load(f)
        
        sentiment_df = pd.read_csv(sentiment_file)
        outliers_df = pd.read_csv(outliers_file)
    except (FileNotFoundError, json.JSONDecodeError, pd.errors.EmptyDataError) as e:
        st.error(f"Error loading data files: {e}. Please ensure the pipeline has run successfully.")
        return

    # --- Dashboard Layout ---
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Trending Topics", "Sentiment Analysis", "Outlier Detection"])

    if page == "Overview":
        st.header("Project Overview")
        st.write("""
        This dashboard presents an analysis of news articles from various Bangladeshi sources.
        It includes trending topics, sentiment analysis, and outlier detection.
        Navigate through the different sections using the sidebar.
        """)
        
        # --- Key Metrics ---
        st.subheader("Key Metrics")
        num_articles = len(sentiment_df)
        num_outliers = outliers_df['is_outlier'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Articles Analyzed", num_articles)
        col2.metric("Outliers Detected", f"{num_outliers}")
        
        if num_articles > 0:
            sentiment_df['Sentiment_Label'] = sentiment_df['Sentiment'].map({'LABEL_1': 'Positive', 'LABEL_0': 'Negative'}).fillna('Unknown')
            positive_sentiments = (sentiment_df['Sentiment_Label'] == 'Positive').sum()
            col3.metric("Positive Sentiment Articles", f"{positive_sentiments} ({((positive_sentiments/num_articles)*100):.1f}%)")

    elif page == "Trending Topics":
        st.header("Top 10 Trending Topics")
        st.write("Topics identified using LDA topic modeling.")
        
        if topics and "message" not in topics:
            for topic_name, topic_words in topics.items():
                st.subheader(topic_name)
                st.write(topic_words)
        else:
            st.warning("No topics found or topics file is empty.")

    elif page == "Sentiment Analysis":
        st.header("Sentiment Analysis of News Headlines")

        sentiment_df['Sentiment_Label'] = sentiment_df['Sentiment'].map({'LABEL_1': 'Positive', 'LABEL_0': 'Negative'}).fillna('Unknown')

        st.subheader("Overall Sentiment Distribution")
        sentiment_counts = sentiment_df['Sentiment_Label'].value_counts()
        
        if not sentiment_counts.empty:
            fig = px.pie(
                sentiment_counts, 
                values=sentiment_counts.values, 
                names=sentiment_counts.index, 
                title="Sentiment Distribution",
                color_discrete_map={'Positive':'green', 'Negative':'red', 'Unknown':'grey'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No sentiment data to display.")

        st.subheader("Sample Articles")
        
        st.write("Most Positive Articles")
        positive_samples = sentiment_df[sentiment_df['Sentiment_Label'] == 'Positive'].sort_values(by='Sentiment_Score', ascending=False).head(5)
        st.dataframe(positive_samples[['Title', 'Source', 'Sentiment_Score']])

        st.write("Most Negative Articles")
        negative_samples = sentiment_df[sentiment_df['Sentiment_Label'] == 'Negative'].sort_values(by='Sentiment_Score', ascending=False).head(5)
        st.dataframe(negative_samples[['Title', 'Source', 'Sentiment_Score']])


    elif page == "Outlier Detection":
        st.header("Outlier Articles")
        st.write(f"A total of **{outliers_df['is_outlier'].sum()}** outliers were detected based on linguistic and sentiment features.")
        st.info("These are articles that are statistically different from the majority of the news headlines.")

        outlier_articles = outliers_df[outliers_df['is_outlier'] == True]
        
        if not outlier_articles.empty:
            st.dataframe(outlier_articles[['Title', 'Source', 'Sentiment', 'Sentiment_Score']])
        else:
            st.warning("No outliers were detected.")

if __name__ == '__main__':
    show_dashboard()
