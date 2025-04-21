import unittest
from bs4 import BeautifulSoup
from headline_extractors import USATodayHeadlineExtractor

class TestUSATodayHeadlineExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = USATodayHeadlineExtractor()
        
    def test_extract_headlines_top_table(self):
        # Sample HTML structure for the new top table layout
        html = """
        <html>
        <body>
            <div class="gnt_m_tt">
                <a class="gnt_m_tl" href="/politics/2024/test-article-1">
                    <div class="gnt_m_tl_c">First Test Headline</div>
                    <div class="gnt_sbt" data-c-ms="Politics" data-c-dt="2024-04-18">Politics • 2 hours ago</div>
                </a>
                <a class="gnt_m_tl" href="/world/2024/test-article-2">
                    <div class="gnt_m_tl_c">Second Test Headline</div>
                    <div class="gnt_sbt" data-c-ms="World" data-c-dt="2024-04-18">World • 3 hours ago</div>
                </a>
                <a class="gnt_m_tl" href="/business/2024/test-article-3">
                    <div class="gnt_m_tl_c">Third Test Headline</div>
                    <div class="gnt_sbt" data-c-ms="Business" data-c-dt="2024-04-18">Business • 4 hours ago</div>
                </a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.usatoday.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Test we got 3 headlines
        self.assertEqual(len(results), 3)
        
        # Test first headline
        self.assertEqual(results[0]['headline'], 'First Test Headline')
        self.assertEqual(results[0]['category'], 'Politics')
        self.assertEqual(results[0]['timestamp'], '2024-04-18')
        self.assertEqual(results[0]['url'], 'https://www.usatoday.com/politics/2024/test-article-1')
        
        # Test second headline
        self.assertEqual(results[1]['headline'], 'Second Test Headline')
        self.assertEqual(results[1]['category'], 'World')
        self.assertEqual(results[1]['timestamp'], '2024-04-18')
        self.assertEqual(results[1]['url'], 'https://www.usatoday.com/world/2024/test-article-2')
        
        # Test third headline
        self.assertEqual(results[2]['headline'], 'Third Test Headline')
        self.assertEqual(results[2]['category'], 'Business')
        self.assertEqual(results[2]['timestamp'], '2024-04-18')
        self.assertEqual(results[2]['url'], 'https://www.usatoday.com/business/2024/test-article-3')

    def test_extract_headlines_legacy(self):
        # Sample HTML structure based on USA Today's typical structure
        html = """
        <html>
        <body>
            <div class="gnt_m">
                <h2 class="gnt_m_hd">First Test Headline</h2>
                <p class="gnt_m_sbt">First subheadline text</p>
                <div class="gnt_m_kw">Politics</div>
                <a href="/politics/2024/test-article-1">Link 1</a>
            </div>
            <article class="gnt_m_flm_a">
                <h3 class="gnt_m_flm_hd">Second Test Headline</h3>
                <p class="gnt_m_flm_sbt">Second subheadline text</p>
                <div class="gnt_m_flm_kw">World</div>
                <a href="/world/2024/test-article-2">Link 2</a>
            </article>
            <div class="gnt_m_flm_b">
                <h2 class="gnt_m_flm_hd">Third Test Headline</h2>
                <p class="gnt_m_flm_sbt">Third subheadline text</p>
                <div class="gnt_m_flm_kw">Business</div>
                <a href="/business/2024/test-article-3">Link 3</a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.usatoday.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Test we got 3 headlines
        self.assertEqual(len(results), 3)
        
        # Test first headline
        self.assertEqual(results[0]['headline'], 'First Test Headline')
        self.assertEqual(results[0]['subheadline'], 'First subheadline text')
        self.assertEqual(results[0]['editorial_tag'], 'Politics')
        self.assertEqual(results[0]['url'], 'https://www.usatoday.com/politics/2024/test-article-1')
        
        # Test second headline
        self.assertEqual(results[1]['headline'], 'Second Test Headline')
        self.assertEqual(results[1]['subheadline'], 'Second subheadline text')
        self.assertEqual(results[1]['editorial_tag'], 'World')
        self.assertEqual(results[1]['url'], 'https://www.usatoday.com/world/2024/test-article-2')
        
        # Test third headline
        self.assertEqual(results[2]['headline'], 'Third Test Headline')
        self.assertEqual(results[2]['subheadline'], 'Third subheadline text')
        self.assertEqual(results[2]['editorial_tag'], 'Business')
        self.assertEqual(results[2]['url'], 'https://www.usatoday.com/business/2024/test-article-3')

    def test_missing_elements(self):
        # Test HTML with missing elements
        html = """
        <html>
        <body>
            <div class="gnt_m">
                <h2 class="gnt_m_hd">Test Headline</h2>
                <!-- Missing subheadline -->
                <a href="/test">Link</a>
            </div>
            <div class="gnt_m">
                <!-- Missing headline -->
                <p class="gnt_m_sbt">Subheadline text</p>
                <a href="/test">Link</a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.usatoday.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Should get no headlines since none have all required elements
        self.assertEqual(len(results), 0)

    def test_wayback_urls(self):
        # Test with Wayback Machine URLs
        html = """
        <html>
        <body>
            <div class="gnt_m_tt">
                <a class="gnt_m_tl" href="https://web.archive.org/web/20250418080432/https://www.usatoday.com/test">
                    <div class="gnt_m_tl_c">Test Headline</div>
                    <div class="gnt_sbt" data-c-ms="Politics" data-c-dt="2024-04-18">Politics • 2 hours ago</div>
                </a>
            </div>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://www.usatoday.com'
        
        results = self.extractor.extract_headlines(soup, base_url)
        
        # Should get one headline with cleaned URL
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], 'https://www.usatoday.com/test')

if __name__ == '__main__':
    unittest.main() 