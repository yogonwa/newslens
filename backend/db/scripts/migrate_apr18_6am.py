import os
import json
from datetime import datetime
from bson import ObjectId
from pathlib import Path
from backend.db.connection import db_connection
from backend.db.models import HeadlineDocument, Headline, Screenshot, HeadlineMetadata
from backend.db.operations import db_ops

SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / "screenshots"
SNAPSHOT_META_PATH = Path(__file__).parent.parent.parent / "tests" / "snapshot_metadata.json"
TIMESLOT = "20250418060000"

# Map domain to source name as in DB
DOMAIN_TO_NAME = {
    "cnn.com": "cnn",
    "foxnews.com": "fox",
    "nytimes.com": "nytimes",
    "washingtonpost.com": "wapo",
    "usatoday.com": "usatoday",
}

# Load S3 keys from snapshot_metadata.json
with open(SNAPSHOT_META_PATH, "r") as f:
    snapshot_meta = {entry["source"]: entry for entry in json.load(f)}

def get_source_id_map():
    """Return a mapping from domain to MongoDB source _id."""
    sources = db_ops.list_sources(active_only=False)
    domain_to_id = {}
    for src in sources:
        domain = src["url"].split("//")[-1].split("/")[0].replace("www.", "")
        domain_to_id[domain] = src["_id"]
    return domain_to_id

def migrate():
    domain_to_id = get_source_id_map()
    for file in SCREENSHOTS_DIR.glob(f"*_" + TIMESLOT + "_metadata.json"):
        domain = file.name.split("_")[0]
        source_short = DOMAIN_TO_NAME.get(domain)
        if not source_short:
            print(f"No short name mapping for domain {domain}")
            continue
        print(f"Processing {file.name} for domain {domain} (source {source_short})")
        with open(file, "r") as f:
            data = json.load(f)
        source_id = domain_to_id.get(domain)
        if not source_id:
            print(f"No source_id found for domain {domain}")
            continue
        # Parse timestamp
        display_timestamp = datetime.strptime(TIMESLOT, "%Y%m%d%H%M%S")
        actual_timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else display_timestamp
        # Build headlines
        headlines = []
        for idx, h in enumerate(data["headlines"]):
            headlines.append(Headline(
                text=h["headline"],
                type="main" if idx == 0 else "secondary",
                position=idx + 1,
                metadata={
                    "editorial_tag": h.get("editorial_tag"),
                    "subheadline": h.get("subheadline"),
                    "article_url": h.get("url"),
                }
            ))
        # S3 keys from snapshot_metadata.json
        meta_entry = snapshot_meta.get(source_short)
        if not meta_entry:
            print(f"No S3 metadata for source {source_short}")
            continue
        screenshot_info = {
            "url": meta_entry["s3_key"],
            "thumbnail_url": meta_entry["thumbnail_key"],
            "format": "png",
            "size": 0,  # Size not needed for prototype
            "dimensions": {"width": 1920, "height": 1080},
            "wayback_url": None,
        }
        # Metadata
        meta = HeadlineMetadata(
            page_title=domain,
            url=data.get("url", ""),
            user_agent="NewsLensBot/0.1",
            time_difference=0,
            confidence="high",
            collection_method="migration",
            status="success"
        )
        # Remove existing record for this source/timeslot
        db_ops.headlines.delete_many({
            "source_id": source_id,
            "display_timestamp": display_timestamp
        })
        # Insert new document
        doc = HeadlineDocument(
            source_id=source_id,
            display_timestamp=display_timestamp,
            actual_timestamp=actual_timestamp,
            headlines=headlines,
            screenshot=screenshot_info,
            metadata=meta
        )
        db_ops.add_headline(doc)
        print(f"Inserted headlines for {domain} at {display_timestamp}")

if __name__ == "__main__":
    migrate() 