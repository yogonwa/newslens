from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin
import unicodedata

class HeadlineExtractor(ABC):
    """Abstract base class for source-specific headline extractors"""
    
    @abstractmethod
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract headlines from the source"""
        pass
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return text
            
        # Replace common Unicode quotes and apostrophes with ASCII versions
        replacements = {
            '\u2018': "'",  # Left single quote
            '\u2019': "'",  # Right single quote
            '\u201C': '"',  # Left double quote
            '\u201D': '"',  # Right double quote
            '\u2013': '-',  # En dash
            '\u2014': '--', # Em dash
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # Normalize remaining unicode characters
        text = unicodedata.normalize('NFKC', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

class CNNHeadlineExtractor(HeadlineExtractor):
    """CNN-specific headline extraction"""
    
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        headlines = []
        try:
            # Find all article containers
            article_containers = soup.find_all('a', class_='container__link--type-article')
            
            for container in article_containers:
                # Look for headline text
                headline = container.find('span', class_='container__headline-text')
                if not headline:
                    continue
                    
                headline_text = self.clean_text(headline.get_text(strip=True))
                
                # Look for subheadline in the same container or parent container
                subheadline = None
                parent_container = container.parent
                if parent_container:
                    subheadline_elem = parent_container.find('span', class_='container__headline-text')
                    if subheadline_elem and subheadline_elem != headline and subheadline_elem.get_text(strip=True) != headline_text:
                        subheadline = self.clean_text(subheadline_elem.get_text(strip=True))
                
                # Get article URL and make it absolute
                article_url = container.get('href', '')
                if article_url:
                    article_url = urljoin(base_url, article_url)
                
                # Only include if it's a main headline (based on container classes)
                container_classes = container.get('class', [])
                is_main_headline = any(c in container_classes for c in [
                    'container_lead-package__link',
                    'container_lead-plus-headlines-with-images__link'
                ])
                
                if is_main_headline:
                    headlines.append({
                        'headline': headline_text,
                        'subheadline': subheadline,
                        'url': article_url
                    })
            
            # Sort headlines by their position in the HTML (earlier = higher priority)
            # And limit to top 3 main headlines
            return headlines[:3]
            
        except Exception as e:
            logging.error(f"Error extracting CNN headlines: {e}")
            return []

class FoxNewsHeadlineExtractor(HeadlineExtractor):
    """Fox News-specific headline extraction"""
    
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        headlines = []
        try:
            # Find main headline containers in the main content area
            main_content = soup.find('main')
            if not main_content:
                main_content = soup
                
            # Look for article containers
            article_containers = main_content.find_all('article')
            
            for container in article_containers:
                # Get headline from h2 or h3
                headline_elem = container.find(['h2', 'h3'])
                if not headline_elem:
                    continue
                    
                headline_text = self.clean_text(headline_elem.get_text(strip=True))
                
                # Find the link element
                link = headline_elem.find('a') or container.find('a')
                if not link:
                    continue
                    
                # Get article URL and make it absolute
                article_url = link.get('href', '')
                if article_url:
                    article_url = urljoin(base_url, article_url)
                
                # Look for subheadline in the same container
                subheadline = None
                subheadline_elem = container.find('p', class_='dek') or container.find('p', class_='subtitle')
                if subheadline_elem:
                    subheadline = self.clean_text(subheadline_elem.get_text(strip=True))
                
                # Look for editorial tag (kicker)
                editorial_tag = None
                kicker_elem = container.find('div', class_='kicker')
                if kicker_elem:
                    kicker_text_elem = kicker_elem.find('span', class_='kicker-text')
                    if kicker_text_elem:
                        editorial_tag = self.clean_text(kicker_text_elem.get_text(strip=True))
                
                # Only include if it's a main headline (based on container classes)
                container_classes = container.get('class', [])
                is_main_headline = any(c in container_classes for c in [
                    'article',
                    'article-ct',
                    'main-content'
                ])
                
                if is_main_headline:
                    headlines.append({
                        'headline': headline_text,
                        'subheadline': subheadline,
                        'editorial_tag': editorial_tag,
                        'url': article_url
                    })
            
            # Sort headlines by their position in the HTML (earlier = higher priority)
            # And limit to top 3 main headlines
            return headlines[:3]
            
        except Exception as e:
            logging.error(f"Error extracting Fox News headlines: {e}")
            return []

class NYTHeadlineExtractor(HeadlineExtractor):
    """New York Times-specific headline extraction"""
    
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        headlines = []
        try:
            # Find all story wrapper sections
            story_sections = soup.find_all('section', class_='story-wrapper')
            
            for story in story_sections:
                # Find headline text in indicate-hover paragraph
                headline_elem = story.find('p', class_='indicate-hover')
                # Find the link in the story
                link = story.find('a', href=True)
                
                if headline_elem and link:
                    headline_text = self.clean_text(headline_elem.get_text(strip=True))
                    article_url = urljoin(base_url, link['href'])
                    
                    headlines.append({
                        'headline': headline_text,
                        'url': article_url,
                        'subheadline': None,  # NYT doesn't seem to have these in the new layout
                        'editorial_tag': None
                    })
            
            # Return top 3 headlines as before
            return headlines[:3]
            
        except Exception as e:
            logging.error(f"Error extracting NYT headlines: {e}")
            return []

class WaPoHeadlineExtractor(HeadlineExtractor):
    """Washington Post-specific headline extraction"""
    
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        headlines = []
        try:
            # Find all headline containers - Washington Post uses various container classes
            headline_containers = soup.find_all(['div', 'article'], class_=['headline', 'story-headline', 'article-headline', 'story'])
            
            for container in headline_containers:
                # Get headline from h2, h3, or headline class
                headline_elem = container.find(['h2', 'h3']) or container.find(class_=['headline', 'story-headline'])
                if not headline_elem:
                    continue
                    
                headline_text = self.clean_text(headline_elem.get_text(strip=True))
                if not headline_text:  # Skip if headline is empty
                    continue
                
                # Find the link element
                link = container.find('a', href=True)
                if not link:
                    continue
                    
                # Get article URL and make it absolute
                article_url = link.get('href', '')
                if not article_url:  # Skip if URL is empty
                    continue
                    
                # Clean up Wayback Machine URL if present
                if 'web.archive.org' in article_url:
                    # Extract the original URL from the Wayback URL
                    original_url = article_url.split('https://')[-1]
                    article_url = f'https://{original_url}'
                else:
                    article_url = urljoin(base_url, article_url)
                
                headlines.append({
                    'headline': headline_text,
                    'subheadline': None,  # Simplified - not extracting subheadlines for now
                    'editorial_tag': None,
                    'url': article_url
                })
            
            # Return top 3 headlines
            return headlines[:3]
            
        except Exception as e:
            logging.error(f"Error extracting Washington Post headlines: {e}")
            return []

class USATodayHeadlineExtractor(HeadlineExtractor):
    """USA Today-specific headline extraction"""
    
    CATEGORY_PRIORITIES = {
        'GRAPHICS': 1,  # Top table graphics
        'CELEBRITIES': 2,  # Top table celebrities
        'WORLD': 3,  # Top table world news
        'U.S. News': 4,
        'Investigations': 5,
        'Politics': 6,
        'Sports': 7,
        'Entertainment': 8,
        'Tech': 9,
        'Wellness': 10,
        'Travel': 11,
        'Money': 12,
        'Shopping': 13,
        'USA TODAY 10BEST': 14,
        'Just Curious': 15,
        'Opinion': 16,
        'Tax Season': 17,
        'Trending Video': 18
    }
    
    def extract_headlines(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        headlines = []
        # Only extract from the top table (above the fold)
        top_table = soup.find('div', class_='gnt_m_tt')
        if top_table:
            # Hero headline
            hero = top_table.find('a', class_='gnt_m_he')
            if hero:
                headline_elem = hero.find('span', attrs={'data-tb-title'})
                subtitle_elem = hero.find('div', class_='gnt_sbt')
                if headline_elem:
                    url = hero.get('href', '')
                    if 'web.archive.org' in url:
                        url_parts = url.split('/https://')
                        if len(url_parts) > 1:
                            url = 'https://' + url_parts[-1]
                    elif not url.startswith('http'):
                        url = base_url + url
                    category = subtitle_elem.get('data-c-ms', '') if subtitle_elem else None
                    timestamp = subtitle_elem.get('data-c-dt', '') if subtitle_elem else None
                    headlines.append({
                        'headline': headline_elem.get_text(strip=True),
                        'category': category,
                        'timestamp': timestamp,
                        'url': url,
                        'priority': 0
                    })
            # First 5 regular tiles
            for article in top_table.find_all('a', class_='gnt_m_tl')[:5]:
                if article.get('rel') == 'sponsored':
                    continue
                headline_elem = article.find('div', class_='gnt_m_tl_c')
                subtitle_elem = article.find('div', class_='gnt_sbt')
                if headline_elem:
                    url = article.get('href', '')
                    if 'web.archive.org' in url:
                        url_parts = url.split('/https://')
                        if len(url_parts) > 1:
                            url = 'https://' + url_parts[-1]
                    elif not url.startswith('http'):
                        url = base_url + url
                    category = subtitle_elem.get('data-c-ms', '') if subtitle_elem else None
                    timestamp = subtitle_elem.get('data-c-dt', '') if subtitle_elem else None
                    priority = self.CATEGORY_PRIORITIES.get(category, 20)
                    headlines.append({
                        'headline': headline_elem.get_text(strip=True),
                        'category': category,
                        'timestamp': timestamp,
                        'url': url,
                        'priority': priority
                    })
        return headlines

def get_extractor(source: str) -> Optional[HeadlineExtractor]:
    """Factory function to get the appropriate extractor"""
    # Normalize source name
    source = source.lower()
    if source.endswith('.com'):
        source = source[:-4]
        
    extractors = {
        'cnn': CNNHeadlineExtractor(),
        'foxnews': FoxNewsHeadlineExtractor(),
        'nytimes': NYTHeadlineExtractor(),
        'washingtonpost': WaPoHeadlineExtractor(),
        'usatoday': USATodayHeadlineExtractor(),
        # Add more sources here as they're implemented
    }
    return extractors.get(source) 