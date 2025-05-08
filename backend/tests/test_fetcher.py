import pytest
import asyncio
from datetime import datetime
from unittest.mock import patch, MagicMock
from backend.scrapers.wayback.fetcher import WaybackFetcher
from backend.shared.utils.timezone import et_to_utc

@pytest.mark.asyncio
async def test_fetch_snapshot_success():
    fetcher = WaybackFetcher()
    test_url = "https://www.cnn.com"
    test_dt_et = datetime(2025, 2, 20, 9, 0)
    test_dt_utc = et_to_utc(test_dt_et)
    # Minimal valid CDX API response: header + one snapshot
    mock_json = [
        ["irrelevant", "timestamp", "original_url"],
        ["row0", "20250220090000", test_url]
    ]
    
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_json
        mock_resp.status_code = 200
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        
        result = await fetcher.fetch_snapshot(test_url, test_dt_utc)
        assert result is not None
        assert result["wayback_url"].startswith("https://web.archive.org/web/")
        assert result["timestamp"].year == 2025

@pytest.mark.asyncio
async def test_fetch_snapshot_no_result():
    fetcher = WaybackFetcher()
    test_url = "https://www.unknown.com"
    test_dt_et = datetime(2025, 2, 20, 9, 0)
    test_dt_utc = et_to_utc(test_dt_et)
    # Minimal valid header only (no snapshots)
    mock_json = [["irrelevant", "timestamp", "original_url"]]
    
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_json
        mock_resp.status_code = 200
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        
        result = await fetcher.fetch_snapshot(test_url, test_dt_utc)
        assert result is None

@pytest.mark.asyncio
async def test_fetch_snapshot_error():
    fetcher = WaybackFetcher()
    test_url = "https://www.error.com"
    test_dt_et = datetime(2025, 2, 20, 9, 0)
    test_dt_utc = et_to_utc(test_dt_et)
    
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        result = await fetcher.fetch_snapshot(test_url, test_dt_utc)
        assert result is None 