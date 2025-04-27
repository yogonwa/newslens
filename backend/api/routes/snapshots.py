from fastapi import APIRouter
from backend.db.operations import db_ops
from backend.services.s3_service import S3Service
from datetime import datetime

router = APIRouter()

@router.get("/snapshots")
def get_snapshots():
    s3_service = S3Service()
    # Fetch all headline documents for the MVP timeslot (6 AM, April 18, 2025)
    # You can generalize this filter as needed
    display_timestamp = datetime.strptime("20250418060000", "%Y%m%d%H%M%S")
    docs = db_ops.headlines.find({"display_timestamp": display_timestamp})
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
        response.append({
            "id": str(doc["_id"]),
            "sourceId": str(doc["source_id"]),
            "timestamp": doc["display_timestamp"].isoformat(),
            "mainHeadline": main_headline,
            "subHeadlines": sub_headlines,
            "imageUrl": image_url,
            "thumbnailUrl": thumbnail_url,
            "sentiment": {"score": 0, "magnitude": 0.5}  # Placeholder
        })
    return response 