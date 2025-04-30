from PIL import Image

def crop_above_the_fold(image_path: str, site_key: str, crop_top_lookup: dict, output_path: str) -> dict:
    """
    Crops a 1920x1080 region from a full screenshot, starting after the banner.

    Args:
        image_path (str): Path to full screenshot
        site_key (str): News site key, like 'cnn.com'
        crop_top_lookup (dict): Dict of { 'cnn': 550, ... }
        output_path (str): Where to save cropped version

    Returns:
        dict: Cropped image dimensions
    """
    source_name = site_key.split('.')[0]
    crop_top = crop_top_lookup.get(source_name, 0)

    with Image.open(image_path) as img:
        cropped = img.crop((0, crop_top, 1920, crop_top + 1080))
        cropped.save(output_path)
        return {
            "width": 1920,
            "height": 1080,
            "crop_top": crop_top,
            "crop_type": "postprocessed_fixed"
        }


--

# Save cropped version before DB/S3 upload
cropped_path = tmp.name.replace(".png", "_cropped.png")
dimensions = crop_above_the_fold(tmp.name, site_key, SOURCE_CROPS, cropped_path)

size = os.path.getsize(cropped_path)
return cropped_path, size, dimensions
