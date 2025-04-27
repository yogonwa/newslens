import os
import json
from PIL import Image
import io
from backend.services.s3_service import S3Service

# Constants
SOURCES = ["cnn", "fox", "nytimes", "usatoday", "wapo"]
DATE = "2025-04-18"
TIMESTAMP = "2025-04-18T06:00:00Z"
TESTS_DIR = os.path.dirname(__file__)
METADATA_PATH = os.path.join(TESTS_DIR, "snapshot_metadata.json")
THUMBNAIL_SIZE = (320, 180)

s3_service = S3Service()
metadata = []

def generate_thumbnail(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(THUMBNAIL_SIZE)
        output = io.BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()

for source in SOURCES:
    img_filename = f"{source}.png"
    img_path = os.path.join(TESTS_DIR, img_filename)
    s3_key = f"manual/{DATE}/{source}.png"
    thumbnail_key = f"manual/{DATE}/thumbnails/{source}.png"

    # Upload original image
    s3_service.upload_file(img_path, s3_key, content_type="image/png")

    # Generate and upload thumbnail
    thumb_bytes = generate_thumbnail(img_path)
    s3_service.upload_bytes(thumb_bytes, thumbnail_key, content_type="image/png")

    # Collect metadata
    metadata.append({
        "source": source,
        "timestamp": TIMESTAMP,
        "s3_key": s3_key,
        "thumbnail_key": thumbnail_key
    })

# Write metadata to JSON file
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Uploaded 5 images and thumbnails to S3. Metadata written to {METADATA_PATH}") 