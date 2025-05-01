from PIL import Image
from pathlib import Path

def crop_cnn(input_path, output_path):
    crop_top = 552
    crop_height = 2000  # Increased from 1080 to capture more content
    target_width = 3000  # Increased to 3000px for wider content view
    
    with Image.open(input_path) as img:
        full_width, _ = img.size

        # Centered crop horizontally
        left = (full_width - target_width) // 2
        right = left + target_width

        cropped = img.crop((left, crop_top, right, crop_top + crop_height))
        cropped.save(output_path)
        print(f"Saved cropped image to: {output_path} ({target_width}x{crop_height})")

if __name__ == '__main__':
    # Define paths
    temp_dir = Path('temp')
    input_path = temp_dir / 'cnn.png'
    output_path = temp_dir / 'cnn_cropped.png'
    
    # Check if input file exists
    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        exit(1)
        
    # Run the crop
    crop_cnn(str(input_path), str(output_path))
