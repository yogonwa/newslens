from playwright.sync_api import sync_playwright
import logging
import os
from pathlib import Path
from time import sleep

# URLs to capture
URLS = {
    'cnn': 'https://web.archive.org/web/20250418051928/https://www.cnn.com/',
    'foxnews': 'https://web.archive.org/web/20250418105039/https://www.foxnews.com/',
    'nytimes': 'https://web.archive.org/web/20250418073220/https://www.nytimes.com/',
    'washingtonpost': 'https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/',
    'usatoday': 'https://web.archive.org/web/20250418123941/https://www.usatoday.com/'
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def take_screenshot(url: str, output_path: str, max_retries: int = 3) -> bool:
    for attempt in range(max_retries):
        with sync_playwright() as p:
            try:
                # Launch browser with proper args
                browser = p.chromium.launch(
                    headless=True,
                    args=['--disable-gpu', '--disable-dev-shm-usage', '--disable-setuid-sandbox', '--no-sandbox']
                )
                
                # Create context with larger viewport
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 2000},
                    device_scale_factor=2.0
                )
                
                page = context.new_page()
                page.set_default_navigation_timeout(120000)  # 2 minutes
                page.set_default_timeout(120000)
                
                # Navigate and wait for content
                logging.info(f"[Attempt {attempt + 1}] Loading {url}")
                page.goto(url, wait_until='domcontentloaded')
                page.wait_for_selector('body', timeout=30000)
                
                # Take full page screenshot
                page.screenshot(path=output_path, full_page=True)
                logging.info(f"Screenshot saved to {output_path}")
                
                context.close()
                browser.close()
                return True
                
            except Exception as e:
                logging.warning(f"[Attempt {attempt + 1}] Error capturing {url}: {e}")
                if attempt < max_retries - 1:
                    sleep(2)  # Wait before retry
                    continue
                else:
                    logging.error(f"Failed to capture {url} after {max_retries} attempts")
                    return False
            finally:
                try:
                    context.close()
                    browser.close()
                except:
                    pass
    return False

def main():
    # Create temp directory if it doesn't exist
    temp_dir = Path('temp')
    temp_dir.mkdir(exist_ok=True)
    
    failed_urls = []
    
    for name, url in URLS.items():
        output_path = temp_dir / f"{name}.png"
        logging.info(f"Processing {name}")
        
        if not take_screenshot(url, str(output_path)):
            failed_urls.append(name)
    
    if failed_urls:
        print("\nFailed to capture screenshots for:")
        for name in failed_urls:
            print(f"- {name}")
    else:
        print("\nAll screenshots captured successfully")

if __name__ == '__main__':
    main() 