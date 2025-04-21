import unittest
from bs4 import BeautifulSoup
from headline_extractors import WaPoHeadlineExtractor

class TestWaPoHeadlineExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = WaPoHeadlineExtractor()
        
    def test_extract_headlines(self):
        # Sample HTML structure based on Washington Post's typical structure
        html = """
        <html>
        <body>
            <div class="story-headline">
                <h2>First Test Headline</h2>
                <p class="story-subheadline">First subheadline text</p>
                <span class="kicker">Politics</span>
                <a href="/politics/2024/test-article-1">Link 1</a>
            </div>
            <article class="article-headline">
                <h3>Second Test Headline</h3>
                <div class="article-subheadline">Second subheadline text</div>
                <div class="article-kicker">World</div>
                <a href="/world/2024/test-article-2">Link 2</a>
            </article>
            <div class="headline">
                <h2>Third Test Headline</h2>
                <p class="subheadline">Third subheadline text</p>
                <span class="kicker">Business</span>
                <a href="/business/2024/test-article-3">Link 3</a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.washingtonpost.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Test we got 3 headlines
        self.assertEqual(len(results), 3)
        
        # Test first headline
        self.assertEqual(results[0]['headline'], 'First Test Headline')
        self.assertEqual(results[0]['subheadline'], 'First subheadline text')
        self.assertEqual(results[0]['editorial_tag'], 'Politics')
        self.assertEqual(results[0]['url'], 'https://www.washingtonpost.com/politics/2024/test-article-1')
        
        # Test second headline
        self.assertEqual(results[1]['headline'], 'Second Test Headline')
        self.assertEqual(results[1]['subheadline'], 'Second subheadline text')
        self.assertEqual(results[1]['editorial_tag'], 'World')
        self.assertEqual(results[1]['url'], 'https://www.washingtonpost.com/world/2024/test-article-2')
        
        # Test third headline
        self.assertEqual(results[2]['headline'], 'Third Test Headline')
        self.assertEqual(results[2]['subheadline'], 'Third subheadline text')
        self.assertEqual(results[2]['editorial_tag'], 'Business')
        self.assertEqual(results[2]['url'], 'https://www.washingtonpost.com/business/2024/test-article-3')

    def test_missing_elements(self):
        # Test HTML with missing elements
        html = """
        <html>
        <body>
            <div class="headline">
                <h2>Test Headline</h2>
                <!-- Missing subheadline -->
                <a href="/test">Link</a>
            </div>
            <div class="headline">
                <!-- Missing headline -->
                <p class="subheadline">Subheadline text</p>
                <a href="/test">Link</a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.washingtonpost.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Should get no headlines since none have all required elements
        self.assertEqual(len(results), 0)

    def test_wayback_urls(self):
        # Test with Wayback Machine URLs
        html = """
        <html>
        <body>
            <div class="headline">
                <h2>Test Headline</h2>
                <a href="https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/test">Link</a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.washingtonpost.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Should clean up Wayback URL
        self.assertEqual(results[0]['url'], 'https://www.washingtonpost.com/test')

if __name__ == '__main__':
    unittest.main() 