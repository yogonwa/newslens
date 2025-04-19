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

def get_extractor(source: str) -> Optional[HeadlineExtractor]:
    """Factory function to get the appropriate extractor"""
    # Normalize source name
    source = source.lower()
    if source.endswith('.com'):
        source = source[:-4]
        
    extractors = {
        'cnn': CNNHeadlineExtractor(),
        'foxnews': FoxNewsHeadlineExtractor(),
        # Add more sources here as they're implemented
    }
    return extractors.get(source) 