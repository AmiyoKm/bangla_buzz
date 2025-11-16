import argparse
from src.scraper import scrape_news
from src.preprocess import preprocess_data


from src.topics import find_topics
from src.sentiment import analyze_sentiment


def run_scraping():
    print("Running scraping...")
    scrape_news()


def run_preprocessing():
    print("Running preprocessing...")
    preprocess_data()


def run_topic_modeling():
    print("Running topic modeling...")
    find_topics()


def run_sentiment_analysis():
    print("Running sentiment analysis...")
    analyze_sentiment()


def run_pagerank():
    pass


def run_outlier_detection():
    pass


def run_dashboard():
    pass


def main():
    parser = argparse.ArgumentParser(description="BanglaBuzz - News Analysis Pipeline")
    parser.add_argument("--scrape", action="store_true", help="Scrape new articles.")
    parser.add_argument(
        "--preprocess", action="store_true", help="Preprocess raw articles."
    )
    parser.add_argument("--topics", action="store_true", help="Run topic modeling.")
    parser.add_argument(
        "--sentiment", action="store_true", help="Run sentiment analysis."
    )
    parser.add_argument(
        "--pagerank", action="store_true", help="Calculate PageRank of sources."
    )
    parser.add_argument(
        "--outlier", action="store_true", help="Detect outlier articles."
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="Launch the Streamlit dashboard."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run the entire pipeline (scrape, preprocess, analyze).",
    )

    args = parser.parse_args()

    if args.all:
        run_scraping()
        run_preprocessing()
        run_topic_modeling()
        run_sentiment_analysis()
        run_pagerank()
        run_outlier_detection()
        print("\nPipeline finished! Run with --dashboard to see the results.")
    else:
        if args.scrape:
            run_scraping()
        if args.preprocess:
            run_preprocessing()
        if args.topics:
            run_topic_modeling()
        if args.sentiment:
            run_sentiment_analysis()
        if args.pagerank:
            run_pagerank()
        if args.outlier:
            run_outlier_detection()
        if args.dashboard:
            run_dashboard()

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
