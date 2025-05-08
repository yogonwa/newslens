import os
import pytest
from bs4 import BeautifulSoup
from backend.scrapers.extractors import headline_extractors
from backend.shared.utils.timezone import et_to_utc

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

SAMPLES = [
    ("cnn", "cnn_sample.html", "https://www.cnn.com"),
    ("foxnews", "foxnews_sample.html", "https://www.foxnews.com"),
    ("nytimes", "nytimes_sample.html", "https://www.nytimes.com"),
    ("washingtonpost", "wapo_sample.html", "https://www.washingtonpost.com"),
    ("usatoday", "usatoday_sample.html", "https://www.usatoday.com"),
]

def load_html(filename):
    path = os.path.join(FIXTURE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return f.read()

@pytest.mark.parametrize("source, filename, base_url", SAMPLES)
def test_headline_extractor_extracts_headlines(source, filename, base_url):
    html = load_html(filename)
    soup = BeautifulSoup(html, "html.parser")
    extractor = headline_extractors.get_extractor(source)
    assert extractor is not None, f"Extractor not found for {source}"
    headlines = extractor.extract_headlines(soup, base_url)
    assert isinstance(headlines, list), f"Extractor for {source} did not return a list"
    assert len(headlines) > 0, f"No headlines extracted for {source}"
    for headline in headlines:
        assert isinstance(headline, dict), f"Headline is not a dict for {source}"
        assert "headline" in headline and headline["headline"], f"Missing or empty 'headline' for {source}"
        assert "url" in headline and headline["url"], f"Missing or empty 'url' for {source}"

@pytest.mark.parametrize("source, filename, base_url", SAMPLES)
def test_headline_extractor_handles_invalid_html(source, filename, base_url):
    # Pass invalid HTML to ensure robust error handling
    soup = BeautifulSoup("<html><body><div>Not a real page</div></body></html>", "html.parser")
    extractor = headline_extractors.get_extractor(source)
    assert extractor is not None, f"Extractor not found for {source}"
    headlines = extractor.extract_headlines(soup, base_url)
    assert isinstance(headlines, list), f"Extractor for {source} did not return a list on invalid HTML"
    # Should not raise, may return empty list

# Edge case: test with empty soup
def test_headline_extractor_empty_soup():
    for source, _, base_url in SAMPLES:
        extractor = headline_extractors.get_extractor(source)
        assert extractor is not None, f"Extractor not found for {source}"
        soup = BeautifulSoup("", "html.parser")
        headlines = extractor.extract_headlines(soup, base_url)
        assert isinstance(headlines, list), f"Extractor for {source} did not return a list on empty soup"
        # Should not raise, may return empty list 