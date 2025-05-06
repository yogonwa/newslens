import os
import json
import boto3
from PIL import Image
from io import BytesIO
import tempfile
from backend.config import get_config
from datetime import datetime

# Load environment variables
config = get_config()

class CLICropAnalyzer:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = config.get('S3_BUCKET_NAME')
        if not self.bucket:
            raise ValueError("S3_BUCKET_NAME environment variable not set")
        
        # Source configs
        self.sources = {
            'cnn': {'file': 'manual/2025-04-18/cnn.png', 'crop_top': 0},
            'fox': {'file': 'manual/2025-04-18/fox.png', 'crop_top': 0},
            'nytimes': {'file': 'manual/2025-04-18/nytimes.png', 'crop_top': 0},
            'usatoday': {'file': 'manual/2025-04-18/usatoday.png', 'crop_top': 0},
            'wapo': {'file': 'manual/2025-04-18/wapo.png', 'crop_top': 0}
        }
        
    def download_and_save_temp(self, source_key):
        """Download image from S3 and save to temp file"""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=source_key)
            image_data = response['Body'].read()
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp.write(image_data)
                return tmp.name
                
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
            
    def process_source(self, source_name):
        """Process a single source interactively"""
        source = self.sources[source_name]
        temp_path = self.download_and_save_temp(source['file'])
        if not temp_path:
            return False
            
        try:
            img = Image.open(temp_path)
            print(f"\nProcessing {source_name}")
            print(f"Image dimensions: {img.size}")
            
            while True:
                crop_px = input(f"Enter crop amount from top (current: {source['crop_top']}px, or 'q' to quit): ")
                if crop_px.lower() == 'q':
                    break
                    
                try:
                    crop_px = int(crop_px)
                    if crop_px < 0 or crop_px >= img.size[1]:
                        print("Invalid crop value - must be between 0 and image height")
                        continue
                        
                    # Apply crop and save preview
                    cropped = img.crop((0, crop_px, img.width, img.height))
                    preview_path = f"preview_{source_name}.png"
                    cropped.save(preview_path)
                    
                    print(f"\nSaved preview to {preview_path}")
                    print("Open this file to see how the crop looks")
                    
                    confirm = input("Keep this crop value? (y/n): ")
                    if confirm.lower() == 'y':
                        self.sources[source_name]['crop_top'] = crop_px
                        break
                        
                except ValueError:
                    print("Please enter a valid number")
                    
            # Cleanup
            os.remove(temp_path)
            if os.path.exists(f"preview_{source_name}.png"):
                os.remove(f"preview_{source_name}.png")
                
            return True
            
        except Exception as e:
            print(f"Error processing {source_name}: {e}")
            return False
            
    def save_parameters(self):
        """Save crop parameters to JSON file"""
        params = {
            'timestamp': datetime.now().isoformat(),
            'sources': self.sources
        }
        
        with open('source_crop_params.json', 'w') as f:
            json.dump(params, f, indent=2)
        print("\nSaved crop parameters to source_crop_params.json")
        
def main():
    analyzer = CLICropAnalyzer()
    
    print("NewsLens Screenshot Crop Analyzer (CLI Version)")
    print("---------------------------------------------")
    
    for source in analyzer.sources.keys():
        print(f"\nProcessing {source}...")
        if analyzer.process_source(source):
            print(f"Successfully processed {source}")
        else:
            print(f"Failed to process {source}")
            
        # Ask if user wants to continue to next source
        if source != list(analyzer.sources.keys())[-1]:  # If not the last source
            cont = input("\nContinue to next source? (y/n): ")
            if cont.lower() != 'y':
                break
                
    analyzer.save_parameters()
    print("\nDone! You can now run apply_crops.py to apply these parameters.")
    
if __name__ == "__main__":
    main() 