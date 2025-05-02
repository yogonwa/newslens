from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List
from PIL import Image
from io import BytesIO
import logging
import asyncio
from playwright.async_api import async_playwright
from backend.services.s3_service import S3Service
from backend.db.operations import db_ops
from backend.db.models import HeadlineDocument, Screenshot, DocumentHeadlineMetadata, Headline
from backend.scrapers.extractors.headline_extractors import get_extractor

# Default configuration
DEFAULT_CONFIG = {
    'wayback_cdx_api': 'https://web.archive.org/cdx/search/cdx',
    'wayback_base': 'https://web.archive.org/web/',
    'user_agent': 'NewsLensBot/0.1',
    'default_times': ['06:00', '09:00', '12:00', '15:00', '18:00'],
    'news_sources': [
        {"name": "CNN", "url": "https://www.cnn.com", "key": "cnn.com"},
        {"name": "Fox News", "url": "https://www.foxnews.com", "key": "foxnews.com"},
        {"name": "The New York Times", "url": "https://www.nytimes.com", "key": "nytimes.com"},
        {"name": "The Washington Post", "url": "https://www.washingtonpost.com", "key": "washingtonpost.com"},
        {"name": "USA Today", "url": "https://www.usatoday.com", "key": "usatoday.com"}
    ]
}

class ScreenshotService:
    """Service for capturing screenshots using Playwright"""
    
    def __init__(self):
        self.max_retries = 3
        
    async def capture_screenshot(self, url: str) -> Optional[BytesIO]:
        """Capture a full page screenshot of the given URL"""
        screenshot_buffer = None
        
        async with async_playwright() as p:
            try:
                # Launch browser with proper args
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--disable-gpu', '--disable-dev-shm-usage', '--disable-setuid-sandbox', '--no-sandbox']
                )
                
                # Create context with larger viewport
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 2000},
                    device_scale_factor=2.0
                )
                
                page = await context.new_page()
                page.set_default_navigation_timeout(120000)  # 2 minutes
                page.set_default_timeout(120000)
                
                # Navigate and wait for content
                logging.info(f"Loading {url}")
                await page.goto(url, wait_until='domcontentloaded')
                await page.wait_for_selector('body', timeout=30000)
                
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
                
                # Take full page screenshot
                screenshot_buffer = BytesIO()
                screenshot_bytes = await page.screenshot(full_page=True)
                screenshot_buffer.write(screenshot_bytes)
                screenshot_buffer.seek(0)
                
                await context.close()
                await browser.close()
                return screenshot_buffer
                
            except Exception as e:
                logging.error(f"Error capturing screenshot for {url}: {e}")
                if screenshot_buffer:
                    screenshot_buffer.close()
                return None
                
            finally:
                try:
                    await context.close()
                    await browser.close()
                except:
                    pass
                    
        return None

class NewsCropper:
    """Handles source-specific image cropping"""
    def __init__(self):
        self.target_width = 3000
        self.crop_params = {
            'cnn.com': {
                'type': 'single',
                'top_offset': 552,
                'content_height': 2000
            },
            'nytimes.com': {
                'type': 'single',
                'top_offset': 710,
                'content_height': 2000
            },
            'washingtonpost.com': {
                'type': 'single',
                'top_offset': 810,
                'content_height': 1900
            },
            'foxnews.com': {
                'type': 'two_region',
                'header_top': 195,
                'header_bottom': 395,
                'content_top': 1080,
                'content_height': 2000
            },
            'usatoday.com': {
                'type': 'two_region',
                'header_top': 120,
                'header_bottom': 825,
                'content_top': 1400,
                'content_height': 1900
            }
        }

    def crop_by_source(self, image_buffer: BytesIO, source_key: str) -> Tuple[BytesIO, Dict]:
        """Main entry point for source-specific cropping"""
        params = self.crop_params.get(source_key)
        if not params:
            raise ValueError(f"No crop parameters defined for source: {source_key}")

        # Convert buffer to PIL Image
        image = Image.open(image_buffer)

        if params['type'] == 'single':
            cropped = self.crop_single_region(image, params['top_offset'], params['content_height'])
        elif params['type'] == 'two_region':
            cropped = self.crop_two_region(
                image,
                params['header_top'],
                params['header_bottom'],
                params['content_top'],
                params['content_height']
            )
        else:
            raise ValueError(f"Unknown crop type: {params['type']}")

        # Convert back to BytesIO
        output_buffer = BytesIO()
        cropped.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        meta = {
            'dimensions': {
                'width': cropped.width,
                'height': cropped.height
            },
            'crop_type': params['type'],
            'crop_params': params
        }

        return output_buffer, meta

    def crop_single_region(self, image: Image.Image, top_offset: int, content_height: int) -> Image.Image:
        """Crop a single content region"""
        width = image.width
        
        # Crop the main content area
        cropped = image.crop((
            0,                  # left
            top_offset,        # top
            width,             # right
            top_offset + content_height  # bottom
        ))
        
        return cropped

    def crop_two_region(
        self,
        image: Image.Image,
        header_top: int,
        header_bottom: int,
        content_top: int,
        content_height: int
    ) -> Image.Image:
        """Crop and combine header and main content regions"""
        width = image.width
        
        # Crop header region
        header = image.crop((
            0,              # left
            header_top,     # top
            width,          # right
            header_bottom   # bottom
        ))
        
        # Crop main content region
        content = image.crop((
            0,              # left
            content_top,    # top
            width,          # right
            content_top + content_height  # bottom
        ))
        
        # Create new image to combine regions
        total_height = header.height + content.height
        combined = Image.new('RGB', (width, total_height))
        
        # Paste regions
        combined.paste(header, (0, 0))
        combined.paste(content, (0, header.height))
        
        return combined

class WaybackScraper:
    """Main orchestrator for the scraping process"""
    def __init__(self, config: Dict):
        self.config = config
        self.screenshot_service = ScreenshotService()
        self.s3_service = S3Service(config['s3_bucket'])
        self.db_service = db_ops  # Use the singleton instance
        self.cropper = NewsCropper()
        self.error_count = 0
        self.max_consecutive_errors = 3

    async def extract_headlines(self, wayback_url: str, source_key: str) -> List[Dict]:
        """Extract headlines from webpage"""
        import requests
        from bs4 import BeautifulSoup
        
        try:
            resp = await asyncio.to_thread(
                requests.get,
                wayback_url,
                headers={"User-Agent": self.config['user_agent']},
                timeout=30
            )
            resp.raise_for_status()
            html = resp.text
            
            # Use existing extractor logic
            extractor = get_extractor(source_key)
            if not extractor:
                logging.warning(f"No extractor for {source_key}")
                return []
                
            soup = BeautifulSoup(html, 'html.parser')
            return extractor.extract_headlines(soup, f"https://{source_key}")
                
        except Exception as e:
            logging.error(f"Headline extraction error for {source_key}: {e}")
            return []

    async def query_wayback_cdx(self, site: str, target_dt: datetime) -> Optional[Dict]:
        """Query Wayback CDX API for closest snapshot"""
        import requests
        
        params = {
            "url": site,
            "from": target_dt.strftime("%Y%m%d"),
            "to": target_dt.strftime("%Y%m%d"),
            "output": "json",
            "filter": "statuscode:200",
            "collapse": "digest"
        }
        headers = {"User-Agent": self.config['user_agent']}
        
        try:
            resp = await asyncio.to_thread(
                requests.get,
                self.config['wayback_cdx_api'],
                params=params,
                headers=headers,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            
            if len(data) <= 1:  # No snapshots (just header row)
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

    async def process_single_snapshot(self, source: Dict, target_dt: datetime) -> Optional[Dict]:
        """Process a single source at a specific time"""
        screenshot_buffer = None
        cropped_buffer = None
        
        try:
            # 1. Query Wayback for snapshot
            cdx_data = await self.query_wayback_cdx(source['url'], target_dt)
            if not cdx_data:
                logging.warning(f"No Wayback snapshot for {source['name']} at {target_dt}")
                return None

            wayback_url = f"{self.config['wayback_base']}{cdx_data['wayback_ts']}/{cdx_data['original_url']}"
            actual_dt = datetime.strptime(cdx_data['wayback_ts'], "%Y%m%d%H%M%S")

            # 2. Capture screenshot
            screenshot_buffer = await self.screenshot_service.capture_screenshot(wayback_url)
            if not screenshot_buffer:
                logging.error(f"Screenshot failed for {source['name']} at {wayback_url}")
                return None

            # 3. Crop screenshot
            try:
                cropped_buffer, crop_meta = self.cropper.crop_by_source(screenshot_buffer, source['key'])
            finally:
                if screenshot_buffer:
                    screenshot_buffer.close()

            # 4. Upload to S3
            s3_key = f"auto/{target_dt.date()}/{source['key']}_{target_dt.strftime('%H%M')}.png"
            try:
                s3_key = await asyncio.to_thread(
                    self.s3_service.upload_bytes,
                    cropped_buffer.getvalue(),
                    s3_key,
                    content_type='image/png'
                )
            finally:
                if cropped_buffer:
                    cropped_buffer.close()

            # 5. Extract headlines
            headlines = await self.extract_headlines(wayback_url, source['key'])

            # 6. Save to database
            sources = await asyncio.to_thread(self.db_service.list_sources)
            source_id = next((s['_id'] for s in sources if s['name'] == source['name']), None)
            if not source_id:
                raise ValueError(f"Source not found: {source['name']}")

            # Create headline document
            screenshot_obj = Screenshot(
                url=s3_key,
                format="png",
                size=len(cropped_buffer.getvalue()) if cropped_buffer else 0,
                dimensions=crop_meta['dimensions'],
                wayback_url=wayback_url
            )

            meta = DocumentHeadlineMetadata(
                page_title=source['name'],
                url=wayback_url,
                user_agent=self.config.get('user_agent', 'NewsLensBot/0.1'),
                time_difference=int((actual_dt - target_dt).total_seconds()),
                confidence="high",
                collection_method="wayback",
                status="success"
            )

            processed_headlines = []
            for idx, h in enumerate(headlines):
                processed_headlines.append(
                    Headline(
                        text=h.get('headline', ''),
                        type='main' if idx == 0 else 'secondary',
                        position=idx + 1,
                        metadata=h.get('metadata')
                    )
                )

            doc = HeadlineDocument(
                source_id=source_id,
                display_timestamp=target_dt,
                actual_timestamp=actual_dt,
                headlines=processed_headlines,
                screenshot=screenshot_obj,
                metadata=meta
            )

            await asyncio.to_thread(self.db_service.add_headline, doc)

            # Reset error count on success
            self.error_count = 0
            return {'s3_url': s3_key, 'meta': crop_meta}

        except Exception as e:
            self.error_count += 1
            logging.error(f"Failed processing {source['name']} for {target_dt}: {e}")
            if self.error_count >= self.max_consecutive_errors:
                raise RuntimeError("Too many consecutive errors")
            return None

    async def process_date_range(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        times: Optional[list] = None
    ):
        """Process screenshots for a date range"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start_dt
        time_slots = times or self.config['default_times']

        current_dt = start_dt
        while current_dt <= end_dt:
            for time_str in time_slots:
                hour, minute = map(int, time_str.split(":"))
                target_dt = current_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                for source in self.config['news_sources']:
                    result = await self.process_single_snapshot(source, target_dt)
                    if result:
                        logging.info(f"Processed {source['name']} for {target_dt}")
                    await asyncio.sleep(1)  # Rate limiting
            
            current_dt += timedelta(days=1)

async def main():
    """CLI entry point"""
    import argparse
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Wayback Machine News Scraper")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Optional end date (YYYY-MM-DD)")
    parser.add_argument("--times", nargs="+", help="Optional time slots (HH:MM)")
    args = parser.parse_args()

    # Initialize config with defaults and environment variables
    config = DEFAULT_CONFIG.copy()
    config['s3_bucket'] = os.getenv('S3_BUCKET_NAME')
    
    # Initialize and run scraper
    scraper = WaybackScraper(config)
    await scraper.process_date_range(
        args.start_date,
        args.end_date,
        args.times
    )

if __name__ == "__main__":
    asyncio.run(main()) 