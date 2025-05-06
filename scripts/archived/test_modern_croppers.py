from backend.scrapers.screenshot_service import ScreenshotService
from backend.scrapers.crop_rules.cnn import CNNCropper
from backend.scrapers.crop_rules.fox import FoxNewsCropper
from backend.scrapers.crop_rules.nyt import NYTimesCropper
from backend.scrapers.crop_rules.usatoday import USATodayCropper
from backend.scrapers.crop_rules.wapo import WaPostCropper
from PIL import Image
from pathlib import Path
import asyncio

URLS = {
    "cnn": "https://web.archive.org/web/20250418051928/https://www.cnn.com/",
    "foxnews": "https://web.archive.org/web/20250418105039/https://www.foxnews.com/",
    "nytimes": "https://web.archive.org/web/20250418073220/https://www.nytimes.com/",
    "usatoday": "https://web.archive.org/web/20250418123941/https://www.usatoday.com/",
    "washingtonpost": "https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/",
}

CROPPERS = {
    "cnn": CNNCropper,
    "foxnews": FoxNewsCropper,
    "nytimes": NYTimesCropper,
    "usatoday": USATodayCropper,
    "washingtonpost": WaPostCropper,
}

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

async def main():
    service = ScreenshotService()
    for name, url in URLS.items():
        print(f"Processing {name}...")
        full_img_path = TEMP_DIR / f"{name}_modern.png"
        cropped_img_path = TEMP_DIR / f"{name}_modern_cropped.png"
        cropper_cls = CROPPERS[name]
        
        # Step 1: Capture screenshot
        screenshot_bytes = await service.capture(url)
        if screenshot_bytes is None:
            print(f"Failed to capture screenshot for {name}.")
            continue
        with open(full_img_path, "wb") as f:
            f.write(screenshot_bytes.getbuffer())
        print(f"Saved full screenshot to {full_img_path}")

        # Step 2: Crop screenshot
        with Image.open(full_img_path) as img:
            cropper = cropper_cls()
            cropped_img, metadata = cropper.crop(img)
            cropped_img.save(cropped_img_path)
            print(f"Saved cropped image to {cropped_img_path}")

    await service.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 