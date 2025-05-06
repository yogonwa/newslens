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
from backend.scrapers.wayback.fetcher import WaybackFetcher
from backend.scrapers.screenshot_service import ScreenshotService
from backend.scrapers.extractors.headline_extractors import get_extractor
from backend.services.s3_service import S3Service
from backend.db.operations import db_ops
from backend.scrapers.crop_rules import get_cropper
from io import BytesIO
from PIL import Image
from loguru import logger
import sys

@click.command()
@click.option('--start-date', type=click.DateTime(formats=["%Y-%m-%d"]), required=True, help="Start date (YYYY-MM-DD)")
@click.option('--end-date', type=click.DateTime(formats=["%Y-%m-%d"]), help="End date (YYYY-MM-DD, defaults to start-date)")
@click.option('--times', type=click.STRING, multiple=True, help="Times to capture (HH:MM, 24h format)")
@click.option('--dry-run', is_flag=True, help="Skip DB and S3 operations")
@click.option('--verbose', is_flag=True, help="Enable detailed logging")
def main(start_date, end_date, times, dry_run, verbose):
    # Configure loguru logger
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    asyncio.run(run_pipeline(start_date, end_date, times, dry_run, verbose))

async def run_pipeline(start_date, end_date, times, dry_run, verbose):
    times = times or DEFAULT_CAPTURE_TIMES
    end_date = end_date or start_date
    summary = {"total": 0, "success": 0, "fail": 0, "failures": []}

    # Initialize services
    wayback = WaybackFetcher()
    screenshot = ScreenshotService()
    s3 = S3Service() if not dry_run else None
    db = db_ops if not dry_run else None

    current = start_date
    while current <= end_date:
        for source in SOURCES:
            for time_str in times:
                target_dt = datetime.combine(current.date(), datetime.strptime(time_str, "%H:%M").time())
                summary["total"] += 1
                context = {
                    "source": source['id'],
                    "display_timestamp": str(target_dt),
                }
                logger.info(f"Starting pipeline for {source['name']} at {target_dt}", extra={**context, "stage": "start"})
                try:
                    await process_snapshot(source, target_dt, wayback, screenshot, s3, db, dry_run, verbose)
                    summary["success"] += 1
                    logger.info(f"Completed pipeline for {source['name']} at {target_dt}", extra={**context, "stage": "end", "status": "success"})
                except Exception as e:
                    summary["fail"] += 1
                    summary["failures"].append({"source": source['id'], "display_timestamp": str(target_dt), "error": str(e)})
                    logger.error(f"Pipeline failed for {source['name']} at {target_dt}: {e}", extra={**context, "stage": "end", "status": "error", "error_message": str(e)})
        current += timedelta(days=1)
    # Log batch summary
    logger.info(f"Pipeline run summary: {summary}", extra={"stage": "summary", **summary})

async def process_snapshot(source, target_dt, wayback, screenshot, s3, db, dry_run, verbose):
    context = {"source": source['id'], "display_timestamp": str(target_dt)}
    # 1. Fetch Wayback snapshot
    logger.info("Fetching Wayback snapshot", extra={**context, "stage": "fetch"})
    snapshot = await wayback.fetch_snapshot(source['url'], target_dt)
    if not snapshot:
        logger.warning("No snapshot found", extra={**context, "stage": "fetch", "status": "not_found"})
        return

    # 2. Load page and capture screenshot/HTML using ScreenshotService
    logger.info("Loading page and capturing screenshot/HTML", extra={**context, "stage": "screenshot"})
    image_bytesio, html = None, None
    try:
        image_html_result = await screenshot.capture(snapshot['wayback_url'], return_html=True)
        if image_html_result is None or image_html_result[0] is None or image_html_result[1] is None:
            logger.warning("Screenshot or HTML capture failed", extra={**context, "stage": "screenshot", "status": "fail"})
            return
        image_bytesio, html = image_html_result
    except Exception as e:
        logger.error(f"ScreenshotService failed: {e}", extra={**context, "stage": "screenshot", "status": "error", "error_message": str(e)})
        return
    image_bytesio.seek(0)

    # 3. Crop image using modular factory
    logger.info("Cropping image", extra={**context, "stage": "crop"})
    cropper = get_cropper(source['id'])
    image = Image.open(image_bytesio)
    cropped_img, crop_meta = cropper.crop(image)

    # 4. Extract headlines from HTML using BeautifulSoup-based extractor
    logger.info("Extracting headlines", extra={**context, "stage": "extract"})
    extractor = get_extractor(source['id'])
    headlines = []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        base_url = source.get('url', '')
        if extractor:
            headlines = extractor.extract_headlines(soup, base_url=base_url)
            logger.info(f"Extracted {len(headlines)} headlines", extra={**context, "stage": "extract", "headlines_found": len(headlines)})
        else:
            logger.warning("No extractor found", extra={**context, "stage": "extract", "status": "no_extractor"})
    except Exception as e:
        logger.error(f"Headline extraction failed: {e}", extra={**context, "stage": "extract", "status": "error", "error_message": str(e)})

    # 5. Upload cropped image to S3 (sync)
    logger.info("Uploading cropped image to S3", extra={**context, "stage": "upload"})
    s3_url = None
    if not dry_run and s3:
        output_bytes = BytesIO()
        cropped_img.save(output_bytes, format="PNG")
        output_bytes.seek(0)
        try:
            s3_url = s3.upload_bytes(output_bytes.getvalue(), f"{source['id']}_{target_dt.strftime('%Y%m%d%H%M')}.png", content_type="image/png")
            logger.info("Image uploaded to S3", extra={**context, "stage": "upload", "status": "success", "s3_url": s3_url})
        except Exception as e:
            logger.error(f"S3 upload failed: {e}", extra={**context, "stage": "upload", "status": "error", "error_message": str(e)})

    # 6. Save snapshot document to MongoDB (sync)
    logger.info("Saving snapshot to MongoDB", extra={**context, "stage": "save"})
    if not dry_run and db:
        try:
            from backend.db.models import HeadlineDocument, Headline, Screenshot, DocumentHeadlineMetadata
            from bson import ObjectId
            # Convert extracted headline dicts to Headline objects
            headline_objs = [
                Headline(
                    text=h.get("headline", ""),
                    type="main",  # You may want to improve this if extractor provides type
                    position=i+1
                ) for i, h in enumerate(headlines)
            ]
            # Build Screenshot object
            screenshot_obj = Screenshot(
                url=s3_url or "",
                format="png",
                size=output_bytes.getbuffer().nbytes if not dry_run and s3 else 0,
                dimensions={"width": cropped_img.width, "height": cropped_img.height},
                wayback_url=snapshot['wayback_url']
            )
            # Build DocumentHeadlineMetadata object
            metadata_obj = DocumentHeadlineMetadata(
                page_title=source.get("name", ""),
                url=snapshot['wayback_url'],
                user_agent="NewsLensBot/0.1",  # Or pull from config
                time_difference=0,  # Could be calculated if needed
                confidence="high",  # Placeholder
                collection_method="main_scraper",
                status="success"
            )
            doc = HeadlineDocument(
                source_id=ObjectId(),  # You may want to use a real source ObjectId if available
                display_timestamp=target_dt,
                actual_timestamp=snapshot['timestamp'],
                headlines=headline_objs,
                screenshot=screenshot_obj,
                metadata=metadata_obj
            )
            db.add_headline(doc)
            logger.info("Snapshot saved to MongoDB", extra={**context, "stage": "save", "status": "success"})
        except Exception as e:
            logger.error(f"MongoDB save failed: {e}", extra={**context, "stage": "save", "status": "error", "error_message": str(e)})

    print(f"[OK] {source['name']} {target_dt} processed.")

if __name__ == "__main__":
    main() 