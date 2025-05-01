from PIL import Image
from pathlib import Path

def crop_nytimes(input_path, output_path):
    crop_top = 710
    crop_height = 2000
    target_width = 3000

    with Image.open(input_path) as img:
        full_width, _ = img.size

        # Center crop horizontally
        left = max((full_width - target_width) // 2, 0)
        right = left + target_width

        cropped = img.crop((left, crop_top, right, crop_top + crop_height))
        cropped.save(output_path)
        print(f"Saved NYT cropped image to: {output_path} ({target_width}x{crop_height})")

if __name__ == '__main__':
    temp_dir = Path('temp')
    input_path = temp_dir / 'nytimes.png'
    output_path = temp_dir / 'nytimes_cropped.png'

    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        exit(1)

    crop_nytimes(str(input_path), str(output_path))
