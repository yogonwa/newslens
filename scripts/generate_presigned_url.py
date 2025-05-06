"""
generate_presigned_url.py

Generates pre-signed S3 URLs for the latest test/e2e PNGs for browser-based visual inspection.
Useful for sharing or reviewing outputs stored in S3.

Run with:
    python scripts/generate_presigned_url.py
"""
import boto3
from botocore.exceptions import NoCredentialsError

BUCKET = "newslens-screenshots"
KEYS = [
    "test/e2e/cnn_202504180519.png",
    "test/e2e/foxnews_202504181050.png",
    "test/e2e/nytimes_202504180732.png",
    "test/e2e/usatoday_202504181239.png",
    "test/e2e/washingtonpost_202504180804.png",
]
EXPIRATION = 3600  # seconds

def generate_presigned_url(bucket, key, expiration=EXPIRATION):
    s3 = boto3.client("s3")
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration
        )
        return url
    except NoCredentialsError:
        print("AWS credentials not found. Run 'aws configure' or set env vars.")
        return None

if __name__ == "__main__":
    for key in KEYS:
        url = generate_presigned_url(BUCKET, key)
        if url:
            print(f"{key}:\n{url}\n") 