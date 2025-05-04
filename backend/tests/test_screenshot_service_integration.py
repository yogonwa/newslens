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
        # Use a stable Wayback Machine archive URL for CNN
        image_bytesio = await service.capture("https://web.archive.org/web/20240101000000/https://www.cnn.com/")
        assert image_bytesio is not None
        # Should be a BytesIO object with nonzero size
        assert hasattr(image_bytesio, 'read')
        data = image_bytesio.read()
        assert isinstance(data, bytes)
        assert len(data) > 10000  # Should be a real image, not empty
        await service.cleanup()
        await browser.close() 