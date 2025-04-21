import unittest
from bs4 import BeautifulSoup
from headline_extractors import NYTHeadlineExtractor

class TestNYTHeadlineExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = NYTHeadlineExtractor()
        
    def test_extract_headlines(self):
        # Sample HTML structure
        html = """
        <html>
        <body>
            <section class="story-wrapper">
                <p class="indicate-hover">First Test Headline</p>
                <a href="/2024/03/test-article-1">Link 1</a>
            </section>
            <section class="story-wrapper">
                <p class="indicate-hover">Second Test Headline</p>
                <a href="/2024/03/test-article-2">Link 2</a>
            </section>
            <section class="story-wrapper">
                <p class="indicate-hover">Third Test Headline</p>
                <a href="/2024/03/test-article-3">Link 3</a>
            </section>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.nytimes.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Test we got 3 headlines
        self.assertEqual(len(results), 3)
        
        # Test first headline
        self.assertEqual(results[0]['headline'], 'First Test Headline')
        self.assertEqual(results[0]['url'], 'https://www.nytimes.com/2024/03/test-article-1')
        
        # Test second headline
        self.assertEqual(results[1]['headline'], 'Second Test Headline')
        self.assertEqual(results[1]['url'], 'https://www.nytimes.com/2024/03/test-article-2')
        
        # Test third headline
        self.assertEqual(results[2]['headline'], 'Third Test Headline')
        self.assertEqual(results[2]['url'], 'https://www.nytimes.com/2024/03/test-article-3')

    def test_missing_elements(self):
        # Test HTML with missing elements
        html = """
        <html>
        <body>
            <section class="story-wrapper">
                <p class="indicate-hover">Test Headline</p>
                <!-- Missing link -->
            </section>
            <section class="story-wrapper">
                <!-- Missing headline -->
                <a href="/test">Link</a>
            </section>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.nytimes.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Should get no headlines since none have both required elements
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main() 