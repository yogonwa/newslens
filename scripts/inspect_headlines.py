from backend.scrapers.extractors.headline_extractors import get_extractor
from bs4 import BeautifulSoup
import requests

URLS = {
    "cnn": "https://web.archive.org/web/20250418051928/https://www.cnn.com/",
    "foxnews": "https://web.archive.org/web/20250418105039/https://www.foxnews.com/",
    "nytimes": "https://web.archive.org/web/20250418073220/https://www.nytimes.com/",
    "usatoday": "https://web.archive.org/web/20250418123941/https://www.usatoday.com/",
    "washingtonpost": "https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/",
}

BASE_URLS = {
    "cnn": "https://www.cnn.com",
    "foxnews": "https://www.foxnews.com",
    "nytimes": "https://www.nytimes.com",
    "usatoday": "https://www.usatoday.com",
    "washingtonpost": "https://www.washingtonpost.com",
}

def inspect_headlines():
    for source, url in URLS.items():
        print(f"\n=== {source.upper()} ===")
        extractor = get_extractor(source)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        headlines = extractor.extract_headlines(soup, base_url=BASE_URLS[source])
        if not headlines:
            print("No headlines extracted.")
        else:
            for i, h in enumerate(headlines, 1):
                print(f"{i}. {h}")

if __name__ == "__main__":
    inspect_headlines() 