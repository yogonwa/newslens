import os
from backend.services.s3_service import S3Service
import sys
from datetime import datetime

def download_screenshots(date_str: str, time_str: str, output_dir: str = "downloaded_screenshots"):
    """
    Downloads screenshots from S3 for a specific date and time.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HHMM format (e.g., '0600')
        output_dir: Local directory to save screenshots
    """
    s3_service = S3Service()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List of news sources
    sources = [
        "cnn.com",
        "foxnews.com",
        "nytimes.com",
        "washingtonpost.com",
        "usatoday.com"
    ]
    
    print(f"Downloading screenshots for {date_str} at {time_str}...")
    
    for source in sources:
        s3_key = f"auto/{date_str}/{source}_{time_str}.png"
        local_path = os.path.join(output_dir, f"{source}_{time_str}.png")
        
        try:
            s3_service.s3_client.download_file(
                Bucket=s3_service.bucket_name,
                Key=s3_key,
                Filename=local_path
            )
            print(f"✓ Downloaded {source} screenshot to {local_path}")
            # Print file size
            size_mb = os.path.getsize(local_path) / (1024 * 1024)
            print(f"  Size: {size_mb:.2f} MB")
        except Exception as e:
            print(f"✗ Failed to download {source}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python download_screenshots.py YYYY-MM-DD HHMM")
        print("Example: python download_screenshots.py 2024-04-18 0600")
        sys.exit(1)
        
    date_str = sys.argv[1]
    time_str = sys.argv[2].replace(":", "")  # Convert HH:MM to HHMM if needed
    
    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format")
        sys.exit(1)
        
    download_screenshots(date_str, time_str) 