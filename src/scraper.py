import csv

import requests
from bs4 import BeautifulSoup

SOURCES = [
    "https://www.prothomalo.com/",
    "https://www.prothomalo.com/bangladesh",
    "https://www.prothomalo.com/world",
    "https://www.prothomalo.com/politics",
]


def scrape_news():
    csv_filename = "data/raw_data.csv"
    data_to_save = []
    seen_titles = set()
    
    for source in SOURCES:
        req = requests.get(source, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(req.content, "html.parser")
        title_tags = soup.find_all("span", class_="tilte-no-link-parent")

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
