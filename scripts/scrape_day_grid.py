import argparse
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import List
import requests
from bs4 import BeautifulSoup
from backend.scrapers.extractors.headline_extractors import get_extractor
from backend.services.s3_service import S3Service
from backend.db.models import HeadlineDocument, Headline, Screenshot, HeadlineMeta, DocumentHeadlineMetadata
from backend.db.operations import db_ops
from bson import ObjectId
from playwright.sync_api import sync_playwright
import tempfile
import json
from time import sleep

# News sources and their canonical names
NEWS_SOURCES = [
    # {"name": "CNN", "url": "https://www.cnn.com", "key": "cnn.com"},
    # {"name": "Fox News", "url": "https://www.foxnews.com", "key": "foxnews.com"},
    {"name": "The New York Times", "url": "https://www.nytimes.com", "key": "nytimes.com"},
    {"name": "The Washington Post", "url": "https://www.washingtonpost.com", "key": "washingtonpost.com"},
    {"name": "USA Today", "url": "https://www.usatoday.com", "key": "usatoday.com"},
]

WAYBACK_CDX_API = "https://web.archive.org/cdx/search/cdx"
WAYBACK_BASE = "https://web.archive.org/web/"
USER_AGENT = "NewsLensBot/0.1 (+https://github.com/yourusername/newslens)"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="Scrape 5x5 news grid for a given day and times.")
    parser.add_argument('--date', required=True, help='Date in YYYY-MM-DD format (e.g., 2025-04-18)')
    parser.add_argument('--times', nargs='+', required=True, help='List of times in HH:MM 24h format (e.g., 06:00 09:00 12:00 15:00 18:00)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing records in DB')
    return parser.parse_args()

def get_target_timestamps(date_str: str, times: List[str]) -> List[datetime]:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return [date.replace(hour=int(t.split(":")[0]), minute=int(t.split(":")[1]), second=0, microsecond=0) for t in times]

def query_wayback_cdx(site: str, target_dt: datetime) -> dict:
    params = {
        "url": site,
        "from": target_dt.strftime("%Y%m%d"),
        "to": target_dt.strftime("%Y%m%d"),
        "output": "json",
        "filter": "statuscode:200",
        "collapse": "digest"
    }
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(WAYBACK_CDX_API, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if len(data) <= 1:
            return None
        # Find closest snapshot to target time
        target_ts = int(target_dt.strftime("%Y%m%d%H%M%S"))
        closest = min(data[1:], key=lambda x: abs(int(x[1]) - target_ts))
        return {"wayback_ts": closest[1], "original_url": closest[2]}
    except Exception as e:
        logging.error(f"Wayback CDX error for {site} at {target_dt}: {e}")
        return None

def take_screenshot(wayback_url: str, site_key: str, timestamp: str) -> (str, int, dict):
    max_retries = 3
    for attempt in range(max_retries):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=[
                '--disable-gpu', '--disable-dev-shm-usage', '--disable-setuid-sandbox', '--no-sandbox'])
            context = browser.new_context(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2.0)
            page = context.new_page()
            try:
                page.set_default_navigation_timeout(120000)
                page.set_default_timeout(120000)
                try:
                    page.goto(wayback_url, wait_until='domcontentloaded')
                except Exception as e:
                    logging.warning(f"[Attempt {attempt+1}] Navigation error for {wayback_url}: {e}")
                    if attempt < max_retries - 1:
                        sleep(2)
                        continue
                    else:
                        raise
                try:
                    page.wait_for_selector('body', timeout=30000)
                except Exception as e:
                    logging.warning(f"Timeout waiting for body element: {str(e)}")
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    try:
                        page.screenshot(path=tmp.name, full_page=False, clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080})
                        size = os.path.getsize(tmp.name)
                        return tmp.name, size, {"width": 1920, "height": 1080}
                    except Exception as e:
                        logging.warning(f"[Attempt {attempt+1}] Screenshot error for {wayback_url}: {e}")
                        if attempt < max_retries - 1:
                            sleep(2)
                            continue
                        else:
                            raise
            finally:
                context.close()
                browser.close()
    return None, 0, {}

def extract_headlines(wayback_url: str, site_key: str) -> List[dict]:
    headers = {"User-Agent": USER_AGENT}
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

def main():
    args = parse_args()
    s3_service = S3Service()
    source_map = {s["key"]: s for s in NEWS_SOURCES}
    # Map source name to ObjectId from DB
    db_sources = db_ops.list_sources(active_only=True)
    name_to_id = {s["name"]: s["_id"] for s in db_sources}
    target_dts = get_target_timestamps(args.date, args.times)
    failed_slots = []
    consecutive_errors = 0
    for source in NEWS_SOURCES:
        source_id = name_to_id.get(source["name"])
        if not source_id:
            logging.warning(f"No source_id for {source['name']}")
            continue
        for target_dt in target_dts:
            logging.info(f"Processing {source['name']} at {target_dt}")
            try:
                cdx = query_wayback_cdx(source["key"], target_dt)
                if not cdx:
                    logging.warning(f"No Wayback snapshot for {source['name']} at {target_dt}")
                    failed_slots.append((source['name'], target_dt.strftime('%Y-%m-%d %H:%M'), 'No Wayback snapshot'))
                    consecutive_errors += 1
                    if consecutive_errors > 3:
                        raise RuntimeError("More than 3 consecutive errors encountered. Stopping script.")
                    continue
                wayback_url = f"{WAYBACK_BASE}{cdx['wayback_ts']}/{cdx['original_url']}"
                actual_dt = datetime.strptime(cdx['wayback_ts'], "%Y%m%d%H%M%S")
                # Screenshot
                try:
                    screenshot_path, size, dimensions = take_screenshot(wayback_url, source["key"], cdx['wayback_ts'])
                except Exception as e:
                    logging.error(f"Screenshot failed for {source['name']} at {wayback_url}: {e}")
                    failed_slots.append((source['name'], target_dt.strftime('%Y-%m-%d %H:%M'), f'Screenshot error: {e}'))
                    consecutive_errors += 1
                    if consecutive_errors > 3:
                        raise RuntimeError("More than 3 consecutive errors encountered. Stopping script.")
                    continue
                if not screenshot_path:
                    logging.error(f"Screenshot failed for {source['name']} at {wayback_url}")
                    failed_slots.append((source['name'], target_dt.strftime('%Y-%m-%d %H:%M'), 'Screenshot path missing'))
                    consecutive_errors += 1
                    if consecutive_errors > 3:
                        raise RuntimeError("More than 3 consecutive errors encountered. Stopping script.")
                    continue
                s3_key = f"auto/{args.date}/{source['key']}_{target_dt.strftime('%H%M')}.png"
                s3_service.upload_file(screenshot_path, s3_key, content_type='image/png')
                # Headline extraction
                headlines_raw = extract_headlines(wayback_url, source["key"])
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
                # Metadata
                meta = DocumentHeadlineMetadata(
                    page_title=source["name"],
                    url=wayback_url,
                    user_agent=USER_AGENT,
                    time_difference=int((actual_dt - target_dt).total_seconds()),
                    confidence="high",
                    collection_method="wayback",
                    status="success"
                )
                screenshot_obj = Screenshot(
                    url=s3_key,
                    format="png",
                    size=size,
                    dimensions=dimensions,
                    wayback_url=wayback_url
                )
                doc = HeadlineDocument(
                    source_id=source_id,
                    display_timestamp=target_dt,
                    actual_timestamp=actual_dt,
                    headlines=headlines,
                    screenshot=screenshot_obj,
                    metadata=meta
                )
                # Upsert or insert
                if args.overwrite:
                    db_ops.headlines.delete_many({"source_id": source_id, "display_timestamp": target_dt})
                db_ops.add_headline(doc)
                logging.info(f"Saved {source['name']} {target_dt.strftime('%H:%M')} to DB and S3.")
                # Cleanup temp screenshot
                if screenshot_path and os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
                # Add a short sleep to avoid hammering services
                sleep(1)
                consecutive_errors = 0  # Reset on success
            except Exception as e:
                logging.error(f"Fatal error for {source['name']} at {target_dt}: {e}")
                failed_slots.append((source['name'], target_dt.strftime('%Y-%m-%d %H:%M'), f'Fatal error: {e}'))
                consecutive_errors += 1
                if consecutive_errors > 3:
                    raise RuntimeError("More than 3 consecutive errors encountered. Stopping script.")
                continue
    if failed_slots:
        print("\nSUMMARY OF FAILED SLOTS:")
        for name, dt, reason in failed_slots:
            print(f"- {name} at {dt}: {reason}")
    else:
        print("\nAll slots processed successfully.")

if __name__ == "__main__":
    main() 