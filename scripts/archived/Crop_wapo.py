from PIL import Image
from pathlib import Path

def crop_wapo_clean(input_path, output_path):
    # Define coordinates
    top_skip = 810  # Skip header and nav
    content_height = 1900  # Height of main content area
    target_width = 3000

    with Image.open(input_path) as img:
        full_width, full_height = img.size
        left = max((full_width - target_width) // 2, 0)
        right = left + target_width

        # Crop main content
        content = img.crop((left, top_skip, right, min(top_skip + content_height, full_height)))
        content.save(output_path)
        print(f"✅ WaPo cropped → {output_path} ({target_width}x{content.height})")

if __name__ == '__main__':
    temp_dir = Path("temp")
    input_path = temp_dir / "washingtonpost.png"
    output_path = temp_dir / "washingtonpost_cropped.png"

    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        exit(1)

    crop_wapo_clean(str(input_path), str(output_path))
