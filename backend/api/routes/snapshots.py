from fastapi import APIRouter, Query, HTTPException
from backend.db.operations import db_ops
from backend.services.s3_service import S3Service
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/snapshots")
def get_snapshots(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    s3_service = S3Service()
    try:
        # Parse the date string
        start_dt = datetime.strptime(date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

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
        # Use only short_id, raise if missing
        short_id = doc.get("short_id")
        if not short_id:
            raise ValueError(f"Document missing short_id: {doc.get('_id')}")
        # Format timeSlotId as YYYYMMDD-HH:MM from display_timestamp
        display_ts = doc["display_timestamp"]
        if hasattr(display_ts, "isoformat"):
            dt = display_ts
        else:
            dt = datetime.fromisoformat(str(display_ts))
        date_str = dt.strftime("%Y%m%d")
        time_slot_id = dt.strftime("%H:%M")  # Use colon for canonical format
        snapshot_id = f"{short_id}-{date_str}-{time_slot_id}"
        response.append({
            "id": snapshot_id,
            "short_id": short_id,
            "timestamp": dt.isoformat(),
            "mainHeadline": main_headline,
            "subHeadlines": sub_headlines,
            "imageUrl": image_url,
            "thumbnailUrl": thumbnail_url,
            "fullImageUrl": image_url,
            "sentiment": {"score": 0, "magnitude": 0.5}  # Placeholder
        })
    return response 