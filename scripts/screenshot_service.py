from playwright.async_api import async_playwright
import logging
from io import BytesIO
import asyncio
from typing import Optional, Dict

class ScreenshotService:
    """Handles Wayback Machine screenshot capture using Playwright"""
    
    def __init__(self, width: int = 1920, height: int = 2000, device_scale_factor: float = 2.0):
        self.viewport = {
            "width": width,
            "height": height,
            "device_scale_factor": device_scale_factor
        }
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) NewsLensBot/1.0"

    async def capture_screenshot(self, url: str, max_retries: int = 3) -> Optional[BytesIO]:
        """
        Capture a full-page screenshot using Playwright
        Returns BytesIO object containing the PNG image
        """
        for attempt in range(max_retries):
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(
                        headless=True,
                        args=['--disable-gpu', '--disable-dev-shm-usage', 
                              '--disable-setuid-sandbox', '--no-sandbox']
                    )
                    
                    context = await browser.new_context(viewport=self.viewport)
                    page = await context.new_page()
                    
                    # Set longer timeouts for Wayback Machine
                    page.set_default_navigation_timeout(120000)
                    page.set_default_timeout(120000)
                    
                    try:
                        await page.goto(url, wait_until='domcontentloaded')
                    except Exception as e:
                        logging.warning(f"[Attempt {attempt+1}] Navigation error: {e}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2)
                            continue
                        raise
                    
                    # Remove Wayback toolbar
                    await page.evaluate("""() => {
                        const waybackElements = ['#wm-ipp', '#wm-ipp-base', '#wm-ipp-print'];
                        waybackElements.forEach(sel => {
                            const el = document.querySelector(sel);
                            if (el) el.remove();
                        });
                    }""")
                    
                    # Short wait for any layout shifts
                    await asyncio.sleep(1)
                    
                    # Capture screenshot to bytes
                    screenshot_bytes = await page.screenshot(full_page=True, type='png')
                    return BytesIO(screenshot_bytes)
                    
            except Exception as e:
                logging.error(f"Screenshot error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2)
        
        return None 