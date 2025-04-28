from datetime import datetime
from backend.db.connection import db_connection
from backend.db.models import HeadlineDocument, Headline, Screenshot, HeadlineMetadata
from backend.db.operations import db_ops

DISPLAY_TIMESTAMP = datetime.strptime("20250418060000", "%Y%m%d%H%M%S")  # 6 AM slot

# Hardcoded data for each source, using S3 key only (not full URI)
DATA = [
    {
        "short": "CNN",
        "source_id": None,  # to be filled in by lookup
        "main": "Sen. Van Hollen was able to spend time with the mistakenly deported man, but El Salvador's president says Abrego Garcia is staying put",
        "sub": "Emergency alerts, desks barricading doors, shoes abandoned in the grass: How the FSU mass shooting upended the campus",
        "actual_timestamp": "2025-04-19T16:13:43.771167",
        "s3_url": "manual/2025-04-18/cnn.png",
        "meta_url": "https://web.archive.org/web/20250418051928/https://www.cnn.com/"
    },
    {
        "short": "Fox News",
        "source_id": None,
        "main": "El Salvador president says what will happen to alleged MS-13 member after Dem senator's visit",
        "sub": "Sheriff deputy's son allegedly used her weapon to carry out deadly Florida State rampage",
        "actual_timestamp": "2025-04-19T16:26:48.165232",
        "s3_url": "manual/2025-04-18/fox.png",
        "meta_url": "https://web.archive.org/web/20250418105039/https://www.foxnews.com/"
    },
    {
        "short": "The New York Times",
        "source_id": None,
        "main": "Senator Meets With Wrongly Deported Maryland Man in El Salvador",
        "sub": "Dual Orders From Judges Edge Courts Closer to Confrontation With White House",
        "actual_timestamp": "2025-04-19T20:50:35.202319",
        "s3_url": "manual/2025-04-18/nytimes.png",
        "meta_url": "https://web.archive.org/web/20250418073220/https://www.nytimes.com/"
    },
    {
        "short": "USA Today",
        "source_id": None,
        "main": "What's inside the CECOT prison where Abrego Garcia is being held?",
        "sub": "Sean 'Diddy' Combs in court: Updates",
        "actual_timestamp": "2025-04-21T13:11:04.661187",
        "s3_url": "manual/2025-04-18/usatoday.png",
        "meta_url": "https://web.archive.org/web/20250418123941/https://www.usatoday.com/"
    },
    {
        "short": "The Washington Post",
        "source_id": None,
        "main": "Sen. Van Hollen recounts meeting in El Salvador with wrongly deported man",
        "sub": "'Sipping margaritas' is latest example in Bukele's propaganda machine",
        "actual_timestamp": "2025-04-21T10:50:30.358897",
        "s3_url": "manual/2025-04-18/wapo.png",
        "meta_url": "https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/"
    },
]

def get_source_id_map():
    sources = db_ops.list_sources(active_only=False)
    short_to_id = {src["name"]: src["_id"] for src in sources}
    return short_to_id

def migrate():
    short_to_id = get_source_id_map()
    db_ops.headlines.delete_many({})
    print("Deleted all existing headline records.")
    for entry in DATA:
        source_id = short_to_id.get(entry["short"])
        if not source_id:
            print(f"No source_id found for {entry['short']}")
            continue
        actual_timestamp = datetime.fromisoformat(entry["actual_timestamp"]) if entry.get("actual_timestamp") else DISPLAY_TIMESTAMP
        headlines = [
            Headline(
                text=entry["main"],
                type="main",
                position=1,
                metadata={}
            )
        ]
        if entry["sub"]:
            headlines.append(
                Headline(
                    text=entry["sub"],
                    type="secondary",
                    position=2,
                    metadata={}
                )
            )
        screenshot_info = {
            "url": entry["s3_url"],
            "thumbnail_url": entry["s3_url"],
            "format": "png",
            "size": 0,
            "dimensions": {"width": 1920, "height": 1080},
            "wayback_url": None,
        }
        meta = HeadlineMetadata(
            page_title=entry["short"],
            url=entry["meta_url"],
            user_agent="NewsLensBot/0.1",
            time_difference=0,
            confidence="high",
            collection_method="migration",
            status="success"
        )
        doc = HeadlineDocument(
            source_id=source_id,
            display_timestamp=DISPLAY_TIMESTAMP,
            actual_timestamp=actual_timestamp,
            headlines=headlines,
            screenshot=screenshot_info,
            metadata=meta
        )
        db_ops.add_headline(doc)
        print(f"Inserted headlines for {entry['short']} at {DISPLAY_TIMESTAMP}")

if __name__ == "__main__":
    migrate()