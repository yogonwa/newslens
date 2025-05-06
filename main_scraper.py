"""
main_scraper.py

Orchestrates the full NewsLens scraping pipeline:
Wayback snapshot fetch → Screenshot → Crop → Headline Extraction → S3 Upload → MongoDB Save.

Run with CLI options for date range, times, and dry-run mode.
See README.md for usage and docs/Scraper_Refactor.md for architecture.
"""
import asyncio
import click
from datetime import datetime, timedelta
from backend.config import SOURCES, DEFAULT_CAPTURE_TIMES
from backend.scrapers.wayback.fetcher import WaybackService
from backend.scrapers.screenshot_service import ScreenshotService
from backend.scrapers.extractors.headline_extractors import get_extractor
from backend.scrapers.crop_rules import get_cropper
from backend.services.s3_service import S3Service
from backend.db.operations import DBService

@click.command()
@click.option('--start-date', type=click.DateTime(formats=["%Y-%m-%d"]), required=True, help="Start date (YYYY-MM-DD)")
@click.option('--end-date', type=click.DateTime(formats=["%Y-%m-%d"]), help="End date (YYYY-MM-DD, defaults to start-date)")
@click.option('--times', type=click.STRING, multiple=True, help="Times to capture (HH:MM, 24h format)")
@click.option('--dry-run', is_flag=True, help="Skip DB and S3 operations")
@click.option('--verbose', is_flag=True, help="Enable detailed logging")
def main(start_date, end_date, times, dry_run, verbose):
    asyncio.run(run_pipeline(start_date, end_date, times, dry_run, verbose))

async def run_pipeline(start_date, end_date, times, dry_run, verbose):
    times = times or DEFAULT_CAPTURE_TIMES
    end_date = end_date or start_date

    # Initialize services
    wayback = WaybackService()
    screenshot = await ScreenshotService.create()
    s3 = S3Service() if not dry_run else None
    db = DBService() if not dry_run else None

    current = start_date
    while current <= end_date:
        for source in SOURCES:
            for time_str in times:
                target_dt = datetime.combine(current.date(), datetime.strptime(time_str, "%H:%M").time())
                try:
                    await process_snapshot(source, target_dt, wayback, screenshot, s3, db, dry_run, verbose)
                except Exception as e:
                    print(f"[ERROR] {source['name']} {target_dt}: {e}")
        current += timedelta(days=1)

async def process_snapshot(source, target_dt, wayback, screenshot, s3, db, dry_run, verbose):
    # 1. Fetch Wayback snapshot
    snapshot = await wayback.fetch_snapshot(source['url'], target_dt)
    if not snapshot:
        print(f"[WARN] No snapshot for {source['name']} at {target_dt}")
        return

    # 2. Capture screenshot
    image_bytes = await screenshot.capture(snapshot['wayback_url'])
    if not image_bytes:
        print(f"[WARN] Screenshot failed for {source['name']} at {target_dt}")
        return

    # 3. Crop image
    cropper = get_cropper(source['key'])
    cropped_img, crop_meta = cropper.crop(image_bytes)

    # 4. Extract headlines
    extractor = get_extractor(source['key'])
    headlines = extractor.extract_headlines_from_url(snapshot['wayback_url'])

    # 5. Upload to S3
    s3_url = None
    if not dry_run and s3:
        s3_url = await s3.upload_screenshot(cropped_img, source['key'], target_dt)

    # 6. Save to DB
    if not dry_run and db:
        await db.save_snapshot(
            source_id=source['id'],
            display_timestamp=target_dt,
            actual_timestamp=snapshot['timestamp'],
            headlines=headlines,
            screenshot_url=s3_url,
            metadata={
                'wayback_url': snapshot['wayback_url'],
                'capture_time': datetime.utcnow(),
                'crop_meta': crop_meta
            }
        )

    print(f"[OK] {source['name']} {target_dt} processed.")

if __name__ == "__main__":
    main() 