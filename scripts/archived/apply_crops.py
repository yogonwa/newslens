import os
import json
import boto3
from PIL import Image
from io import BytesIO
import tempfile
from backend.config import get_config

# Load environment variables
config = get_config()

class ScreenshotCropper:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = config['S3_BUCKET_NAME']
        if not self.bucket:
            raise ValueError("S3_BUCKET_NAME environment variable not set")
        
        # Load crop parameters
        with open('source_crop_params.json', 'r') as f:
            self.params = json.load(f)
            
    def process_screenshot(self, source_key: str, crop_top: int) -> str:
        """
        Download screenshot from S3, crop it, and upload back with _cropped suffix
        Returns the new S3 key
        """
        try:
            # Download original
            response = self.s3.get_object(Bucket=self.bucket, Key=source_key)
            image_data = response['Body'].read()
            
            # Process image
            with Image.open(BytesIO(image_data)) as img:
                # Apply crop
                cropped = img.crop((0, crop_top, img.width, img.height))
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    cropped.save(tmp.name, 'PNG', optimize=True)
                    
                    # Generate new key
                    base, ext = os.path.splitext(source_key)
                    new_key = f"{base}_cropped{ext}"
                    
                    # Upload cropped version
                    self.s3.upload_file(
                        tmp.name,
                        self.bucket,
                        new_key,
                        ExtraArgs={'ContentType': 'image/png'}
                    )
                    
                # Clean up
                os.unlink(tmp.name)
                
                return new_key
                
        except Exception as e:
            print(f"Error processing {source_key}: {e}")
            return None
            
    def process_all(self):
        """Process all screenshots using saved parameters"""
        results = {}
        
        for source, config in self.params['sources'].items():
            source_key = config['file']
            crop_top = config['crop_top']
            
            print(f"Processing {source}...")
            new_key = self.process_screenshot(source_key, crop_top)
            
            if new_key:
                results[source] = {
                    'original': source_key,
                    'cropped': new_key,
                    'crop_top': crop_top
                }
                print(f"Successfully cropped {source} -> {new_key}")
            else:
                print(f"Failed to process {source}")
                
        # Save results
        with open('crop_results.json', 'w') as f:
            json.dump({
                'timestamp': self.params['timestamp'],
                'results': results
            }, f, indent=2)
            
def main():
    cropper = ScreenshotCropper()
    cropper.process_all()
    
if __name__ == "__main__":
    main() 