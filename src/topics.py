import pandas as pd
import gensim
from gensim import corpora
import json
import os

def find_topics():
    """
    Performs LDA topic modeling on the cleaned news data.
    """
    input_path = "data/clean_news.csv"
    output_path = "data/topics.json"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run the preprocessing step first.")
        return

    df = pd.read_csv(input_path)
    
    if 'Title' not in df.columns:
        print("Error: 'Title' column not found in clean_news.csv.")
        return
    
    df['Title'] = df['Title'].astype(str).fillna('')
    
    tokenized_data = [text.split() for text in df['Title']]

    dictionary = corpora.Dictionary(tokenized_data)
    corpus = [dictionary.doc2bow(text) for text in tokenized_data]

    if not corpus or not any(corpus):
        print("Error: Corpus is empty. Cannot train LDA model.")
        # Create an empty topics file to avoid downstream errors
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"message": "No topics found due to empty corpus."}, f, ensure_ascii=False, indent=4)
        return
        
    lda_model = gensim.models.LdaModel(
        corpus,
        num_topics=10,
        id2word=dictionary,
        passes=15,
        random_state=42
    )

    topics = lda_model.print_topics(num_words=5)
    
    formatted_topics = {}
    for topic_id, topic_words in topics:
        formatted_topics[f"Topic {topic_id + 1}"] = topic_words

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_topics, f, ensure_ascii=False, indent=4)

    print(f"Topic modeling complete. Topics saved to {output_path}")

if __name__ == "__main__":
    find_topics()
