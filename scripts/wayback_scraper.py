from datetime import datetime, timedelta
import logging
import asyncio
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from backend.scrapers.extractors.headline_extractors import get_extractor
from backend.db.models import HeadlineDocument, Screenshot, Headline, HeadlineMeta, DocumentHeadlineMetadata

from .config import Config
from .screenshot_service import ScreenshotService
from .s3_service import S3Service
from .db_service import DBService
from .crop_service import NewsCropper

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT
)

def extract_headlines(wayback_url: str, site_key: str) -> List[dict]:
    """Existing headline extraction logic"""
    headers = {"User-Agent": Config.WAYBACK_USER_AGENT}
    try:
        resp = requests.get(wayback_url, headers=headers, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        extractor = get_extractor(site_key)
        if not extractor:
            logging.warning(f"No extractor for {site_key}")
            return []
        return extractor.extract_headlines(soup, f"https://{site_key}")
    except Exception as e:
        logging.error(f"Headline extraction error for {site_key}: {e}")
        return []

class WaybackScraper:
    def __init__(self):
        self.config = Config
        self.screenshot_service = ScreenshotService(**self.config.VIEWPORT)
        self.s3_service = S3Service(self.config.S3_BUCKET)
        self.db_service = DBService(self.config.MONGO_URI)
        self.cropper = NewsCropper()
        self.error_count = 0

    async def query_wayback_cdx(self, site: str, target_dt: datetime) -> Optional[Dict]:
        """Query Wayback CDX API for closest snapshot"""
        params = {
            "url": site,
            "from": target_dt.strftime("%Y%m%d"),
            "to": target_dt.strftime("%Y%m%d"),
            **self.config.WAYBACK_CDX_PARAMS
        }
        headers = {"User-Agent": self.config.WAYBACK_USER_AGENT}
        
        try:
            resp = requests.get(
                self.config.WAYBACK_CDX_API,
                params=params,
                headers=headers,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            
            if len(data) <= 1:  # First row is header
                return None
                
            # Find closest snapshot to target time
            target_ts = int(target_dt.strftime("%Y%m%d%H%M%S"))
            closest = min(data[1:], key=lambda x: abs(int(x[1]) - target_ts))
            
            return {
                "wayback_ts": closest[1],
                "original_url": closest[2]
            }
            
        except Exception as e:
            logging.error(f"Wayback CDX error for {site} at {target_dt}: {e}")
            return None

    async def process_single_snapshot(
        self,
        source: Dict,
        target_dt: datetime
    ) -> Optional[Tuple[str, Dict]]:
        """Process a single source at specific time"""
        try:
            # 1. Get Wayback snapshot
            cdx_data = await self.query_wayback_cdx(source['url'], target_dt)
            if not cdx_data:
                logging.warning(f"No Wayback snapshot for {source['name']} at {target_dt}")
                return None

            wayback_url = f"{self.config.WAYBACK_BASE}{cdx_data['wayback_ts']}/{cdx_data['original_url']}"
            actual_dt = datetime.strptime(cdx_data['wayback_ts'], "%Y%m%d%H%M%S")

            # 2. Capture screenshot
            screenshot_buffer = await self.screenshot_service.capture_screenshot(wayback_url)
            if not screenshot_buffer:
                logging.error(f"Screenshot failed for {source['name']} at {wayback_url}")
                return None

            # 3. Crop screenshot
            try:
                cropped_image, crop_meta = self.cropper.crop_by_source(screenshot_buffer, source['key'])
            finally:
                screenshot_buffer.close()

            # 4. Upload to S3
            s3_key = f"auto/{target_dt.date()}/{source['key']}_{target_dt.strftime('%H%M')}.png"
            try:
                s3_url = await self.s3_service.upload_buffer(
                    cropped_image,
                    s3_key,
                    metadata={
                        'source': source['name'],
                        'timestamp': target_dt.isoformat(),
                        'wayback_url': wayback_url
                    }
                )
            finally:
                cropped_image.close()

            # 5. Extract headlines using existing logic
            headlines_raw = await asyncio.to_thread(extract_headlines, wayback_url, source['key'])
            headlines = []
            for idx, h in enumerate(headlines_raw):
                # Only include headline-level metadata fields if present
                headline_meta_fields = {}
                if h.get('editorial_tag') is not None:
                    headline_meta_fields['editorial_tag'] = h.get('editorial_tag')
                if h.get('subheadline') is not None:
                    headline_meta_fields['subheadline'] = h.get('subheadline')
                if h.get('url') is not None:
                    headline_meta_fields['article_url'] = h.get('url')
                metadata = None
                if headline_meta_fields:
                    metadata = HeadlineMeta(**headline_meta_fields)
                headlines.append(Headline(
                    text=h.get('headline', ''),
                    type='main' if idx == 0 else 'secondary',
                    position=idx+1,
                    metadata=metadata
                ))

            # 6. Save to database
            source_id = await self.db_service.get_source_id(source['name'])
            if not source_id:
                raise ValueError(f"Source not found: {source['name']}")

            await self.db_service.save_snapshot(
                source_id=source_id,
                display_timestamp=target_dt,
                actual_timestamp=actual_dt,
                s3_url=s3_url,
                wayback_url=wayback_url,
                headlines=headlines,
                image_meta=crop_meta
            )

            # Reset error count on success
            self.error_count = 0
            return s3_url, crop_meta

        except Exception as e:
            self.error_count += 1
            logging.error(f"Failed processing {source['name']} at {target_dt}: {e}")
            if self.error_count >= self.config.MAX_CONSECUTIVE_ERRORS:
                raise RuntimeError("Too many consecutive errors")
            return None

    async def process_date_range(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        times: Optional[List[str]] = None
    ):
        """Process screenshots for a date range"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start_dt
        time_slots = times or self.config.DEFAULT_TIMES

        current_dt = start_dt
        while current_dt <= end_dt:
            for time_str in time_slots:
                hour, minute = map(int, time_str.split(":"))
                target_dt = current_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                for source in self.config.NEWS_SOURCES:
                    await self.process_single_snapshot(source, target_dt)
                    # Small delay between requests
                    await asyncio.sleep(1)
            
            current_dt += timedelta(days=1)

async def main():
    """CLI entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Wayback Machine News Scraper")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Optional end date (YYYY-MM-DD)")
    parser.add_argument("--times", nargs="+", help="Optional time slots (HH:MM)")
    args = parser.parse_args()

    # Load environment variables
    Config.load_env(Path(".env"))

    # Initialize and run scraper
    scraper = WaybackScraper()
    await scraper.process_date_range(
        args.start_date,
        args.end_date,
        args.times
    )

if __name__ == "__main__":
    asyncio.run(main()) 