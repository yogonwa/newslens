import json
import logging
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create screenshots directory at the start
os.makedirs('screenshots', exist_ok=True)

def load_first_url():
    """Load the first URL from the most recent snapshot file."""
    # Find the most recent snapshot file
    files = [f for f in os.listdir('.') if f.startswith('wayback_snapshots_') and f.endswith('.json')]
    if not files:
        raise FileNotFoundError("No snapshot files found")
    
    latest_file = max(files)
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Get the first site and its first timestamp
    first_site = next(iter(data))
    first_timestamp = next(iter(data[first_site]))
    url = data[first_site][first_timestamp]['url']
    
    return url, first_site, first_timestamp

def extract_headlines_and_metadata(url: str) -> dict:
    """Extract headlines and metadata from the archived page."""
    headers = {
        "User-Agent": "NewsLensBot/0.1 (+https://github.com/yourusername/newslens; contact: your@email.com)"
    }
    
    # Section headers and navigation elements to exclude
    exclude_headers = {
        'More top stories', 'International affairs', 'On campus', 'CNN Podcasts',
        'In the spotlight', 'Check these out', 'For Subscribers', 'CNN Underscored',
        'Best-in-class', 'Expert-backed guides', 'Editors\' picks', 'Business',
        'Entertainment', 'Space and Science', 'Travel', 'Style', 'health and wellness',
        'More Politics', 'US', 'World', 'CNN podcasts', 'Sports', 'Video',
        'Food and Home', 'Paid Content', 'More from CNN', 'Health', 'Investing',
        'Photos', 'Paid Partner Content', 'CNN Games + Quizzes', 'In case you missed it'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Save the raw HTML
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract headlines (h1 and h2 tags)
        headlines = []
        for tag in soup.find_all(['h1', 'h2']):
            text = tag.get_text(strip=True)
            # Only include headlines that aren't in the exclude list and aren't empty
            if text and text not in exclude_headers:
                headlines.append({
                    'text': text,
                    'tag': tag.name
                })
        
        # Extract metadata
        metadata = {
            'title': soup.title.string if soup.title else None,
            'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None,
            'headlines': headlines,
            'timestamp': datetime.now().isoformat(),
            'url': url
        }
        
        return metadata, html_content
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching page: {e}")
        return None, None

def take_screenshot(url: str, site: str, timestamp: str):
    """Take a screenshot of the archived page."""
    with sync_playwright() as p:
        # Launch browser with increased timeout and macOS-specific settings
        browser = p.chromium.launch(
            headless=True,  # Force headless mode
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-sandbox'
            ]
        )
        
        # Set viewport to standard desktop size
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # Standard desktop resolution
            device_scale_factor=2.0  # Higher resolution for retina displays
        )
        page = context.new_page()
        
        try:
            logging.info(f"Navigating to URL: {url}")
            # Set navigation timeout
            page.set_default_navigation_timeout(120000)  # 2 minutes
            page.set_default_timeout(120000)  # 2 minutes
            
            # Navigate with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = page.goto(url, wait_until='domcontentloaded')
                    if response and response.ok:
                        break
                    logging.warning(f"Attempt {attempt + 1} failed, retrying...")
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logging.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                    time.sleep(5)
            
            # Wait for the page to load
            logging.info("Waiting for page to load...")
            try:
                page.wait_for_selector('body', timeout=30000)
            except Exception as e:
                logging.warning(f"Timeout waiting for body element: {str(e)}")
            
            # Take viewport-only screenshot
            screenshot_path = f'screenshots/{site}_{timestamp}.png'
            logging.info(f"Attempting to take screenshot to: {screenshot_path}")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            
            # Take screenshot with retry - only capture viewport
            for attempt in range(3):
                try:
                    page.screenshot(
                        path=screenshot_path,
                        full_page=False,  # Only capture viewport
                        clip={
                            'x': 0,
                            'y': 0,
                            'width': 1920,
                            'height': 1080
                        }
                    )
                    logging.info(f"Screenshot saved successfully to {screenshot_path}")
                    
                    # Save a full-page version as well for reference
                    full_page_path = f'screenshots/{site}_{timestamp}_full.png'
                    page.screenshot(path=full_page_path, full_page=True)
                    logging.info(f"Full page screenshot saved to {full_page_path}")
                    break
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    logging.warning(f"Screenshot attempt {attempt + 1} failed: {str(e)}, retrying...")
                    time.sleep(2)
            
        except Exception as e:
            logging.error(f"Error taking screenshot: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
        finally:
            try:
                context.close()
            except Exception as e:
                logging.warning(f"Error closing context: {str(e)}")
            try:
                browser.close()
            except Exception as e:
                logging.warning(f"Error closing browser: {str(e)}")

def main():
    try:
        # Load the first URL
        url, site, timestamp = load_first_url()
        logging.info(f"Processing URL: {url}")
        
        # Extract headlines and metadata
        metadata, html_content = extract_headlines_and_metadata(url)
        if metadata:
            # Save metadata to JSON
            metadata_file = f'screenshots/{site}_{timestamp}_metadata.json'
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            logging.info(f"Metadata saved to {metadata_file}")
            
            # Save raw HTML
            html_file = f'screenshots/{site}_{timestamp}_raw.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"Raw HTML saved to {html_file}")
        
        # Take screenshot
        take_screenshot(url, site, timestamp)
        
    except Exception as e:
        logging.error(f"Error in main process: {e}")
        import traceback
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main() 