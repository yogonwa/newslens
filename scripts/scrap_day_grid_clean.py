from playwright.sync_api import sync_playwright
import tempfile
import os
import logging
from time import sleep

def take_screenshot(wayback_url: str, site_key: str, timestamp: str) -> (str, int, dict):
    """
    Navigates to a Wayback Machine URL, removes unwanted header/banner elements,
    and captures a clean full-page screenshot.

    Args:
        wayback_url (str): Full URL to the Wayback snapshot.
        site_key (str): Identifier for the news source (e.g., cnn.com).
        timestamp (str): Wayback timestamp string.

    Returns:
        (screenshot_path, file_size, metadata_dict)
    """
    max_retries = 3
    for attempt in range(max_retries):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-gpu', '--disable-dev-shm-usage', '--disable-setuid-sandbox', '--no-sandbox'
            ])
            context = browser.new_context(viewport={'width': 1920, 'height': 2000}, device_scale_factor=2.0)
            page = context.new_page()
            try:
                page.set_default_navigation_timeout(120000)
                page.set_default_timeout(120000)
                try:
                    page.goto(wayback_url, wait_until='domcontentloaded')
                except Exception as e:
                    logging.warning(f"[Attempt {attempt+1}] Navigation error for {wayback_url}: {e}")
                    if attempt < max_retries - 1:
                        sleep(2)
                        continue
                    else:
                        raise

                # Remove Wayback and site-specific headers
                page.evaluate("""
                    // Remove Wayback toolbar
                    const wm = document.getElementById('wm-ipp');
                    if (wm) wm.remove();

                    // Remove common site header and ad banners
                    const selectorsToRemove = [
                        'header',
                        'iframe',
                        '.ad',
                        '.banner',
                        '[id^="ad-"]',
                        '[class*="ad-"]',
                        '[class*="banner"]',
                        '[role="banner"]'
                    ];
                    selectorsToRemove.forEach(sel => {
                        document.querySelectorAll(sel).forEach(el => el.remove());
                    });

                    // Scroll to bottom to trigger lazy loading
                    window.scrollTo(0, document.body.scrollHeight);
                """)
                
                sleep(1)  # Allow DOM updates and lazy loads to settle

                # Dynamically calculate full page height
                full_height = page.evaluate("document.body.scrollHeight")

                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    try:
                        page.screenshot(
                            path=tmp.name,
                            clip={
                                'x': 0,
                                'y': 0,
                                'width': 1920,
                                'height': full_height
                            }
                        )
                        size = os.path.getsize(tmp.name)
                        return tmp.name, size, {
                            "width": 1920,
                            "height": full_height,
                            "crop_top": 0  # No manual crop needed
                        }
                    except Exception as e:
                        logging.warning(f"[Attempt {attempt+1}] Screenshot error for {wayback_url}: {e}")
                        if attempt < max_retries - 1:
                            sleep(2)
                            continue
                        else:
                            raise
            finally:
                context.close()
                browser.close()
    return None, 0, {}
