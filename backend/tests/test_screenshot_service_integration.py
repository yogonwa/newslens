import pytest
from backend.scrapers.screenshot_service import ScreenshotService
from playwright.async_api import async_playwright

# List of sources and their Wayback URLs
SOURCES = [
    ("cnn", "https://web.archive.org/web/20250418051928/https://www.cnn.com/"),
    ("foxnews", "https://web.archive.org/web/20250418105039/https://www.foxnews.com/"),
    ("nytimes", "https://web.archive.org/web/20250418073220/https://www.nytimes.com/"),
    ("washingtonpost", "https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/"),
    ("usatoday", "https://web.archive.org/web/20250418123941/https://www.usatoday.com/")
]

@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize("source, url", SOURCES)
async def test_capture_real_page(source, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        service = ScreenshotService()
        service.browser = browser
        image_bytesio = await service.capture(url)
        assert image_bytesio is not None
        # Save the screenshot for visual inspection
        filename = f"test_fullsize_screenshot_{source}.png"
        with open(filename, "wb") as f:
            f.write(image_bytesio.read())
        image_bytesio.seek(0)  # Reset for any further use
        # Should be a BytesIO object with nonzero size
        assert hasattr(image_bytesio, 'read')
        data = image_bytesio.read()
        assert isinstance(data, bytes)
        assert len(data) > 10000  # Should be a real image, not empty
        await service.cleanup()
        await browser.close() 