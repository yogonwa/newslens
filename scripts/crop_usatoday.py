from PIL import Image
from pathlib import Path

def crop_usatoday_clean(input_path, output_path):
    # Define coordinates
    top_skip = 130
    nav_height = 157
    ad_height = 575
    body_start = top_skip + nav_height + ad_height
    content_height = 1800  # or adjust as needed

    target_width = 3000

    with Image.open(input_path) as img:
        full_width, full_height = img.size
        left = max((full_width - target_width) // 2, 0)
        right = left + target_width

        # Crop nav section
        nav_top = top_skip
        nav_bottom = nav_top + nav_height
        nav = img.crop((left, nav_top, right, nav_bottom))

        # Crop body
        body = img.crop((left, body_start, right, min(body_start + content_height, full_height)))

        # Stitch them together
        total_height = nav.height + body.height
        final = Image.new("RGB", (target_width, total_height), (255, 255, 255))

        y = 0
        final.paste(nav, (0, y))
        y += nav.height
        final.paste(body, (0, y))

        final.save(output_path)
        print(f"✅ Final USA Today cropped → {output_path} ({target_width}x{total_height})")

if __name__ == '__main__':
    temp_dir = Path("temp")
    input_path = temp_dir / "usatoday.png"
    output_path = temp_dir / "usatoday_cropped.png"

    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        exit(1)

    crop_usatoday_clean(str(input_path), str(output_path))
