import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.scrapers.screenshot_service import ScreenshotService
from io import BytesIO
from backend.shared.utils.timezone import et_to_utc

@pytest.mark.asyncio
async def test_capture_success(monkeypatch):
    service = ScreenshotService()
    # Mock _init_browser to do nothing
    monkeypatch.setattr(service, "_init_browser", AsyncMock())
    # Mock browser/context/page
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_page.screenshot.return_value = b'fakeimagebytes'
    mock_page.set_default_navigation_timeout = MagicMock()
    mock_page.set_default_timeout = MagicMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_context.new_page.return_value = mock_page
    mock_context.close.return_value = AsyncMock()
    service.browser = AsyncMock()
    service.browser.new_context.return_value = mock_context

    result = await service.capture("http://example.com")
    assert isinstance(result, BytesIO)
    assert result.read() == b'fakeimagebytes'

@pytest.mark.asyncio
async def test_capture_error(monkeypatch):
    service = ScreenshotService()
    monkeypatch.setattr(service, "_init_browser", AsyncMock())
    # Simulate error in new_context
    service.browser = AsyncMock()
    service.browser.new_context.side_effect = Exception("browser error")
    result = await service.capture("http://example.com")
    assert result is None 