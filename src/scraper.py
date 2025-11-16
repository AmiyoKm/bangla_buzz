import csv

import requests
from bs4 import BeautifulSoup

SOURCES = [
    ("https://www.prothomalo.com/", "span", "tilte-no-link-parent"),
    ("https://bangla.bdnews24.com/", "h2", "Title"),
    ("https://bangla.thedailystar.net/", "h3", "title"),
    ("https://bangla.dhakatribune.com/", "h2", "title"),
    ("https://www.banglanews24.com/", "h5", "lh-base"),
    ("https://www.tbsnews.net/bangla/", "h3", "poynternarrowsemibold"),
    ("https://www.risingbd.com/", "h3", ""),
    ("https://www.dhakapost.com/", "h3", ""),
    ("https://www.dhakapost.com/", "h2", ""),
    ("https://www.dhakapost.com/", "h1", ""),
]


def scrape_news():
    csv_filename = "data/raw_data.csv"
    data_to_save = []

    for source, tag, class_name in SOURCES:
        req = requests.get(source, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(req.content, "html.parser")
        if class_name:
            title_tags = soup.find_all(tag, class_=class_name)
        else:
            title_tags = soup.find_all(tag)

        for title_tag in title_tags:
            title = title_tag.text.strip()
            data_to_save.append([title, source])
        print(len(title_tags))
    headers = ["Title", "Source"]

    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerows(data_to_save)

    print(f"Successfully saved data to {csv_filename}")
