from fastapi import APIRouter
from backend.db.operations import db_ops
from backend.services.s3_service import S3Service
from datetime import datetime

router = APIRouter()

# Mapping from MongoDB ObjectId to short string source keys
SOURCE_ID_MAP = {
    "6807e171fdec5451bda49cfb": "cnn",
    "6807e171fdec5451bda49cfc": "fox",
    "6807e171fdec5451bda49cfd": "nytimes",
    "6807e171fdec5451bda49cfe": "wapo",
    "6807e171fdec5451bda49cff": "usatoday",
}

@router.get("/snapshots")
def get_snapshots():
    s3_service = S3Service()
    # Filter for documents with display_timestamp on 2025-04-18
    start_dt = datetime(2025, 4, 18)
    end_dt = datetime(2025, 4, 19)
    docs = db_ops.headlines.find({
        "display_timestamp": {"$gte": start_dt, "$lt": end_dt}
    })
    response = []
    for doc in docs:
        # Main headline is the first in the list, subheadlines are the rest
        headlines = doc.get("headlines", [])
        main_headline = headlines[0]["text"] if headlines else ""
        sub_headlines = [h["text"] for h in headlines[1:]] if len(headlines) > 1 else []
        # S3 keys from MongoDB
        s3_key = doc["screenshot"]["url"]
        thumbnail_key = doc["screenshot"].get("thumbnail_url", s3_key)
        # Generate presigned URLs
        image_url = s3_service.generate_presigned_url(s3_key, expires_in=3600)
        thumbnail_url = s3_service.generate_presigned_url(thumbnail_key, expires_in=3600)
        # Use short_id if present, else fallback to mapping
        short_source_id = doc.get("short_id")
        if not short_source_id:
            source_id_str = str(doc["source_id"])
            short_source_id = SOURCE_ID_MAP.get(source_id_str, source_id_str)
        # Format timeSlotId as YYYYMMDD-HHMM from display_timestamp
        display_ts = doc["display_timestamp"]
        if hasattr(display_ts, "isoformat"):
            dt = display_ts
        else:
            dt = datetime.fromisoformat(str(display_ts))
        time_slot_id = dt.strftime("%Y%m%d-%H%M")
        snapshot_id = f"{short_source_id}-{time_slot_id}"
        response.append({
            "id": snapshot_id,
            "sourceId": short_source_id,
            "timestamp": dt.isoformat(),
            "mainHeadline": main_headline,
            "subHeadlines": sub_headlines,
            "imageUrl": image_url,
            "thumbnailUrl": thumbnail_url,
            "fullImageUrl": image_url,
            "sentiment": {"score": 0, "magnitude": 0.5}  # Placeholder
        })
    return response 