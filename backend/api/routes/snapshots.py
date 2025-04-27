from fastapi import APIRouter
from backend.services.s3_service import S3Service
import os
import json
from pathlib import Path

router = APIRouter()

TESTS_DIR = Path(__file__).parent.parent.parent / "tests"
METADATA_PATH = TESTS_DIR / "snapshot_metadata.json"

@router.get("/snapshots")
def get_snapshots():
    s3_service = S3Service()
    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)
    
    # Build response for frontend
    response = []
    for entry in metadata:
        source_id = entry["source"]
        timestamp = entry["timestamp"]
        s3_key = entry["s3_key"]
        thumbnail_key = entry["thumbnail_key"]
        # Generate presigned URLs
        image_url = s3_service.generate_presigned_url(s3_key, expires_in=3600)
        thumbnail_url = s3_service.generate_presigned_url(thumbnail_key, expires_in=3600)
        # Placeholder headlines
        main_headline = f"Top story from {source_id.title()}"
        sub_headlines = [f"Secondary headline for {source_id}"]
        # Unique ID for frontend
        snapshot_id = f"{source_id}-20250418-0600"
        response.append({
            "id": snapshot_id,
            "sourceId": source_id,
            "timestamp": timestamp,
            "mainHeadline": main_headline,
            "subHeadlines": sub_headlines,
            "imageUrl": image_url,
            "thumbnailUrl": thumbnail_url
        })
    return response 