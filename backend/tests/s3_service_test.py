import os
from backend.services.s3_service import S3Service

# Path to the test image (assume it's saved as 'wapo_test.png' in the tests directory)
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'wapo_test.png')
S3_KEY = 'test/wapo_test.png'
CONTENT_TYPE = 'image/png'

def main():
    s3_service = S3Service()
    # Upload the image
    print(f"Uploading {IMAGE_PATH} to S3 key: {S3_KEY}")
    s3_service.upload_file(IMAGE_PATH, S3_KEY, content_type=CONTENT_TYPE)
    print("Upload successful.")
    # Generate a presigned URL
    url = s3_service.generate_presigned_url(S3_KEY, expires_in=600)
    print(f"Presigned URL (valid for 10 min): {url}")

if __name__ == "__main__":
    main() 