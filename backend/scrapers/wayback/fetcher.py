"""
fetcher.py

Provides WaybackFetcher for querying the Wayback Machine CDX API and retrieving the closest archived snapshot for a given URL and time.
Used in the NewsLens pipeline to obtain historical news homepages for screenshotting and analysis.
"""
from datetime import datetime
from typing import Dict, Optional
import logging
import asyncio
import requests
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WaybackFetcher:
    """CDX API client for fetching Wayback Machine snapshots"""
    
    def __init__(self, user_agent: str = "NewsLensBot/0.1"):
        self.cdx_url = "https://web.archive.org/cdx/search/cdx"
        self.wayback_base = "https://web.archive.org/web/"
        self.user_agent = user_agent
        
    def _create_log_context(self, url: str, target_dt: datetime, **kwargs) -> Dict:
        """Create structured log context"""
        return {
            "stage": "wayback_fetch",
            "url": url,
            "target_timestamp": target_dt.isoformat(),
            "snapshot_id": f"{url}_{target_dt.strftime('%Y%m%d%H%M%S')}",
            **kwargs
        }
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def query_wayback_cdx(self, url: str, target_dt: datetime) -> Optional[Dict]:
        """Query Wayback CDX API for closest snapshot"""
        start_time = time.time()
        log_ctx = self._create_log_context(url, target_dt, operation="cdx_query")
        
        params = {
            "url": url,
            "from": target_dt.strftime("%Y%m%d"),
            "to": target_dt.strftime("%Y%m%d"),
            "output": "json",
            "filter": "statuscode:200",
            "collapse": "digest"
        }
        headers = {"User-Agent": self.user_agent}
        
        try:
            # Use asyncio.to_thread for non-blocking HTTP request
            resp = await asyncio.to_thread(
                requests.get,
                self.cdx_url,
                params=params,
                headers=headers,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            
            duration_ms = int((time.time() - start_time) * 1000)
            log_ctx.update({
                "status": "success",
                "duration_ms": duration_ms,
                "response_size": len(str(data))
            })
            
            if len(data) <= 1:  # No snapshots (just header row)
                log_ctx.update({"status": "no_snapshots"})
                logger.warning("No snapshots found", extra=log_ctx)
                return None
                
            # Find closest snapshot to target time
            target_ts = int(target_dt.strftime("%Y%m%d%H%M%S"))
            closest = min(data[1:], key=lambda x: abs(int(x[1]) - target_ts))
            
            log_ctx.update({
                "snapshots_found": len(data) - 1,
                "selected_timestamp": closest[1]
            })
            logger.info("Found Wayback snapshot", extra=log_ctx)
            
            return {
                "wayback_ts": closest[1],
                "original_url": closest[2]
            }
            
        except Exception as e:
            log_ctx.update({
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e),
                "duration_ms": int((time.time() - start_time) * 1000)
            })
            logger.error("Wayback CDX error", extra=log_ctx)
            return None

    async def fetch_snapshot(self, url: str, target_dt: datetime) -> Optional[Dict]:
        """
        Fetch closest snapshot to target time.
        
        Args:
            url (str): The URL to fetch snapshot for
            target_dt (datetime): Target datetime for snapshot
            
        Returns:
            Optional[Dict]: Snapshot data or None if not available
        """
        start_time = time.time()
        log_ctx = self._create_log_context(url, target_dt, operation="fetch_snapshot")
        
        try:
            snapshot = await self.query_wayback_cdx(url, target_dt)
            if not snapshot:
                return None
                
            result = {
                "wayback_url": f"{self.wayback_base}{snapshot['wayback_ts']}/{snapshot['original_url']}",
                "timestamp": datetime.strptime(snapshot['wayback_ts'], "%Y%m%d%H%M%S")
            }
            
            log_ctx.update({
                "status": "success",
                "duration_ms": int((time.time() - start_time) * 1000),
                "wayback_url": result["wayback_url"],
                "actual_timestamp": result["timestamp"].isoformat()
            })
            logger.info("Successfully fetched snapshot", extra=log_ctx)
            
            return result
            
        except Exception as e:
            log_ctx.update({
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e),
                "duration_ms": int((time.time() - start_time) * 1000)
            })
            logger.error("Failed to fetch snapshot", extra=log_ctx)
            return None 