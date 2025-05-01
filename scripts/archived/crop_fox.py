from PIL import Image
from pathlib import Path

def smart_crop_foxnews(input_path, output_path):
    # Region 1: Keep header + nav
    header_top = 195
    header_bottom = 395

    # Region 2: Skip ad, keep main content
    content_top = 1080
    content_height = 2000
    content_bottom = content_top + content_height

    target_width = 3000

    with Image.open(input_path) as img:
        full_width, full_height = img.size

        # Center horizontally
        left = max((full_width - target_width) // 2, 0)
        right = left + target_width

        # Crop slices
        header = img.crop((left, header_top, right, header_bottom))
        content = img.crop((left, content_top, right, content_bottom))

        # Create stitched image
        total_height = (header_bottom - header_top) + (content_bottom - content_top)
        stitched = Image.new('RGB', (target_width, total_height))
        
        # Paste the regions
        stitched.paste(header, (0, 0))
        stitched.paste(content, (0, header_bottom - header_top))
        
        # Save the result
        stitched.save(output_path)
        print(f"Saved smart-cropped image to: {output_path} ({target_width}x{total_height})")

if __name__ == '__main__':
    temp_dir = Path('temp')
    input_path = temp_dir / 'foxnews.png'
    output_path = temp_dir / 'foxnews_cropped.png'

    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}")
        exit(1)

    smart_crop_foxnews(str(input_path), str(output_path))
