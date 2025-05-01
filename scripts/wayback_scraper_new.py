from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from PIL import Image
from io import BytesIO
import logging
import asyncio

class ScreenshotService:
    """Handles Wayback Machine screenshot capture"""
    def __init__(self, viewport_width=1920, viewport_height=2000, device_scale_factor=2.0):
        self.viewport_config = {
            "width": viewport_width,
            "height": viewport_height,
            "device_scale_factor": device_scale_factor
        }
    
    async def capture_screenshot(self, wayback_url: str) -> BytesIO:
        """Placeholder for screenshot capture logic"""
        # TODO: Implement Playwright screenshot capture
        pass

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
        self.db_service = DBService(config['mongo_uri'])
        self.cropper = NewsCropper()
        self.error_count = 0
        self.max_consecutive_errors = 3

    async def query_wayback_cdx(self, site: str, target_dt: datetime) -> Optional[Dict]:
        """Query Wayback CDX API for closest snapshot"""
        params = {
            "url": site,
            "from": target_dt.strftime("%Y%m%d"),
            "to": target_dt.strftime("%Y%m%d"),
            "output": "json",
            "filter": "statuscode:200",
            "collapse": "digest"
        }
        
        try:
            resp = await self.config['session'].get(
                self.config['wayback_cdx_api'],
                params=params,
                headers={"User-Agent": self.config['user_agent']}
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
                screenshot_buffer.close()

            # 4. Upload to S3
            s3_key = f"auto/{target_dt.date()}/{source['key']}_{target_dt.strftime('%H%M')}.png"
            try:
                s3_url = await self.s3_service.upload_buffer(
                    cropped_buffer,
                    s3_key,
                    metadata={
                        'source': source['name'],
                        'timestamp': target_dt.isoformat(),
                        'wayback_url': wayback_url
                    }
                )
            finally:
                cropped_buffer.close()

            # 5. Extract headlines
            headlines = await self.extract_headlines(wayback_url, source['key'])

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
            return {'s3_url': s3_url, 'meta': crop_meta}

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
    import aiohttp
    from .config import Config
    
    parser = argparse.ArgumentParser(description="Wayback Machine News Scraper")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Optional end date (YYYY-MM-DD)")
    parser.add_argument("--times", nargs="+", help="Optional time slots (HH:MM)")
    args = parser.parse_args()

    # Load config
    config = Config.load_env()
    
    # Create aiohttp session
    async with aiohttp.ClientSession() as session:
        config['session'] = session
        
        # Initialize and run scraper
        scraper = WaybackScraper(config)
        await scraper.process_date_range(
            args.start_date,
            args.end_date,
            args.times
        )

if __name__ == "__main__":
    asyncio.run(main()) 