import csv

import requests
from bs4 import BeautifulSoup

SOURCES = [
    "https://www.prothomalo.com/",
    "https://bangla.bdnews24.com/",
    "https://bangla.thedailystar.net/"
]


def scrape_news():
    csv_filename = "data/raw_data.csv"
    data_to_save = []
    seen_titles = set()

    for source in SOURCES:
        req = requests.get(source, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(req.content, "html.parser")
        title_tags = soup.find_all("span", class_="tilte-no-link-parent") + soup.find_all("h4",class_="title") + soup.find_all("h2", class_="Title")

        for title_tag in title_tags:
            title = title_tag.text.strip()
            if title not in seen_titles:
                data_to_save.append([title, source])
                seen_titles.add(title)

    headers = ["Title", "Source"]

    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerows(data_to_save)

    print(f"Successfully saved data to {csv_filename}")
