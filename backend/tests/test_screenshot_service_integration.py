import pytest
from backend.scrapers.screenshot_service import ScreenshotService
from playwright.async_api import async_playwright

@pytest.mark.integration
@pytest.mark.asyncio
async def test_capture_real_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        service = ScreenshotService()
        service.browser = browser
        # Use the specified Wayback Machine archive URL for CNN
        url = "https://web.archive.org/web/20250418051928/https://www.cnn.com/"
        image_bytesio = await service.capture(url)
        assert image_bytesio is not None
        # Save the screenshot for visual inspection
        with open("test_fullsize_screenshot.png", "wb") as f:
            f.write(image_bytesio.read())
        image_bytesio.seek(0)  # Reset for any further use
        # Should be a BytesIO object with nonzero size
        assert hasattr(image_bytesio, 'read')
        data = image_bytesio.read()
        assert isinstance(data, bytes)
        assert len(data) > 10000  # Should be a real image, not empty
        await service.cleanup()
        await browser.close() 