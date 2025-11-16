
# BanglaBuzz: News Trend and Sentiment Analysis

BanglaBuzz is a Python-based news analysis pipeline that scrapes news articles from various Bangladeshi news websites, performs analysis, and presents the results in an interactive dashboard.

## Features

- **News Scraping:** Scrapes the latest news headlines from multiple Bangladeshi news sources.
- **Text Preprocessing:** Cleans and preprocesses the scraped text data for analysis.
- **Topic Modeling:** Identifies trending topics from the news headlines using Latent Dirichlet Allocation (LDA).
- **Sentiment Analysis:** Performs sentiment analysis on news headlines to determine the overall sentiment (Positive, Negative, Neutral).
- **Outlier Detection:** Detects outlier news articles that are statistically different from the majority.
- **Interactive Dashboard:** A Streamlit-based dashboard to visualize the analysis results.

## Technologies Used

- **Programming Language:** Python 3
- **Data Scraping:** `requests`, `beautifulsoup4`
- **Data Manipulation:** `pandas`, `numpy`
- **Machine Learning & NLP:** `scikit-learn`, `nltk`, `gensim`, `transformers`, `torch`, `bnlp_toolkit`
- **Dashboard:** `streamlit`, `plotly`
- **Dependency Management:** `uv`

## Project Structure

```
.
├── data/                 # CSV and JSON files for the data pipeline
├── src/                  # Source code for the project
│   ├── scraper.py        # News scraping logic
│   ├── preprocess.py     # Data preprocessing logic
│   ├── topics.py         # Topic modeling logic
│   ├── sentiment.py      # Sentiment analysis logic
│   ├── outlier.py        # Outlier detection logic
│   └── dashboard.py      # Streamlit dashboard application
├── main.py               # Main script to run the pipeline
├── requirements.txt      # Project dependencies
├── config.json           # Configuration file
└── README.md             # This file
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/BanglaBuzz.git
    cd BanglaBuzz
    ```

2.  **Install dependencies using uv:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Usage

The project uses a command-line interface to run the different stages of the pipeline.

### Running the Entire Pipeline

To run all the stages of the pipeline from scraping to analysis, use the `--all` flag:

```bash
uv run python3 main.py --all
```

### Running Individual Stages

You can also run each stage of the pipeline individually:

-   **Scrape News:**
    ```bash
    uv run python3 main.py --scrape
    ```

-   **Preprocess Data:**
    ```bash
    uv run python3 main.py --preprocess
    ```

-   **Topic Modeling:**
    ```bash
    uv run python3 main.py --topics
    ```

-   **Sentiment Analysis:**
    ```bash
    uv run python3 main.py --sentiment
    ```

-   **Outlier Detection:**
    ```bash
    uv run python3 main.py --outlier
    ```

### Launching the Dashboard

After running the analysis pipeline, you can view the results in the interactive dashboard:

```bash
uv run python3 main.py --dashboard
```

This will start the Streamlit application, and you can access it in your web browser at `http://localhost:8501`.

## Data Flow

1.  **Raw Data:** The `scraper.py` script scrapes news headlines and stores them in `data/raw_data.csv`.
2.  **Clean Data:** The `preprocess.py` script cleans the raw data and saves it to `data/clean_news.csv`.
3.  **Topic Modeling:** The `topics.py` script identifies topics from the cleaned data and saves them to `data/topics.json`.
4.  **Sentiment Analysis:** The `sentiment.py` script performs sentiment analysis and saves the results to `data/news_with_sentiment.csv`.
5.  **Outlier Detection:** The `outlier.py` script detects outliers and saves the final dataset to `data/news_with_outliers.csv`.
6.  **Dashboard:** The `dashboard.py` script reads the data from the `data/` directory and displays it in the Streamlit dashboard.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
