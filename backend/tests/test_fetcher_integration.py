import pytest
from datetime import datetime
from backend.scrapers.wayback.fetcher import WaybackFetcher
from backend.shared.utils.timezone import et_to_utc

@pytest.mark.integration
@pytest.mark.asyncio
async def test_fetch_snapshot_integration():
    fetcher = WaybackFetcher()
    test_url = "https://www.cnn.com"
    # Use the date/time from the provided Wayback URL (assume ET slot)
    test_dt_et = datetime(2025, 4, 18, 5, 19, 28)
    test_dt_utc = et_to_utc(test_dt_et)
    result = await fetcher.fetch_snapshot(test_url, test_dt_utc)
    assert result is not None
    assert "wayback_url" in result
    assert "timestamp" in result
    # Optionally, check that the wayback_url matches the expected prefix
    assert result["wayback_url"].startswith("https://web.archive.org/web/") 