import pytest
from backend.scrapers.screenshot_service import ScreenshotService
from backend.services.s3_service import S3Service
from backend.db.operations import db_ops
from backend.db.models import HeadlineDocument, Headline, Screenshot, DocumentHeadlineMetadata
from backend.scrapers.extractors.headline_extractors import get_extractor
from datetime import datetime
from bson import ObjectId
from io import BytesIO
from bs4 import BeautifulSoup
import asyncio
import re
from backend.scrapers.crop_rules import get_cropper

# Parameterized test data for each source
E2E_SOURCES = [
    {
        "source": "cnn",
        "wayback_url": "https://web.archive.org/web/20250418051928/https://www.cnn.com/",
        "base_url": "https://www.cnn.com",
        "cropper_module": "backend.scrapers.crop_rules.cnn",
        "cropper_class": "CNNCropper",
        "datetime_fmt": "%Y%m%d%H%M",
    },
    {
        "source": "foxnews",
        "wayback_url": "https://web.archive.org/web/20250418105039/https://www.foxnews.com/",
        "base_url": "https://www.foxnews.com",
        "cropper_module": "backend.scrapers.crop_rules.fox",
        "cropper_class": "FoxNewsCropper",
        "datetime_fmt": "%Y%m%d%H%M",
    },
    {
        "source": "nytimes",
        "wayback_url": "https://web.archive.org/web/20250418073220/https://www.nytimes.com/",
        "base_url": "https://www.nytimes.com",
        "cropper_module": "backend.scrapers.crop_rules.nyt",
        "cropper_class": "NYTimesCropper",
        "datetime_fmt": "%Y%m%d%H%M",
    },
    {
        "source": "washingtonpost",
        "wayback_url": "https://web.archive.org/web/20250418080432/https://www.washingtonpost.com/",
        "base_url": "https://www.washingtonpost.com",
        "cropper_module": "backend.scrapers.crop_rules.wapo",
        "cropper_class": "WaPostCropper",
        "datetime_fmt": "%Y%m%d%H%M",
    },
    {
        "source": "usatoday",
        "wayback_url": "https://web.archive.org/web/20250418123941/https://www.usatoday.com/",
        "base_url": "https://www.usatoday.com",
        "cropper_module": "backend.scrapers.crop_rules.usatoday",
        "cropper_class": "USATodayCropper",
        "datetime_fmt": "%Y%m%d%H%M",
    },
]

uploaded_s3_keys = []

@pytest.mark.asyncio
@pytest.mark.parametrize("params", E2E_SOURCES)
async def test_e2e_pipeline(params):
    source = params["source"]
    wayback_url = params["wayback_url"]
    base_url = params["base_url"]
    cropper_module = params["cropper_module"]
    cropper_class = params["cropper_class"]
    datetime_fmt = params["datetime_fmt"]

    # Extract timestamp from Wayback URL for S3 key
    m = re.search(r"/web/(\d{12,14})/", wayback_url)
    if not m:
        raise ValueError(f"Could not extract timestamp from Wayback URL: {wayback_url}")
    dt_str = m.group(1)[:12]  # Use YYYYMMDDHHMM
    s3_key = f"test/e2e/{source}_{dt_str}.png"
    s3 = S3Service()

    # Cleanup before
    # s3.delete_prefix("test/e2e/")
    db_ops.headlines.delete_many({"test_marker": True})

    # 1. Capture screenshot
    service = ScreenshotService()
    await service._init_browser()
    image_bytesio = await service.capture(wayback_url)
    assert image_bytesio is not None
    image_bytesio.seek(0)

    # 2. Crop
    from PIL import Image
    image = Image.open(image_bytesio)
    cropper = get_cropper(source)
    # Support both BaseCropper and MultiRegionCropper
    if hasattr(cropper, "crop"):
        cropped, crop_metadata = cropper.crop(image)
    else:
        raise RuntimeError(f"Cropper for {source} does not have a crop() method")
    output_bytes = BytesIO()
    cropped.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    # 3. Upload to S3
    s3.upload_bytes(output_bytes.getvalue(), s3_key, content_type="image/png")
    files = s3.list_files("test/e2e/")
    assert s3_key in files
    uploaded_s3_keys.append(s3_key)

    # 4. Extract headlines
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(wayback_url, wait_until='domcontentloaded')
        html = await page.content()
        await browser.close()
    soup = BeautifulSoup(html, "html.parser")
    extractor = get_extractor(source)
    headlines = extractor.extract_headlines(soup, base_url=base_url)
    if source == "cnn" and not headlines:
        with open("backend/tests/cnn_wayback_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
    assert headlines and isinstance(headlines, list)

    # 5. Store in MongoDB
    doc = HeadlineDocument(
        source_id=ObjectId(),
        display_timestamp=datetime.strptime(dt_str, "%Y%m%d%H%M"),
        actual_timestamp=datetime.utcnow(),
        headlines=[Headline(text=h["headline"], type="main", position=i+1) for i, h in enumerate(headlines)],
        screenshot=Screenshot(
            url=s3_key,
            format="png",
            size=output_bytes.getbuffer().nbytes,
            dimensions={"width": cropped.width, "height": cropped.height},
            wayback_url=wayback_url
        ),
        metadata=DocumentHeadlineMetadata(
            page_title=f"{source.upper()} Test Page",
            url=wayback_url,
            user_agent="TestAgent",
            time_difference=0,
            confidence="high",
            collection_method="e2e_test",
            status="success"
        ),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        test_marker=True
    )
    inserted_id = db_ops.add_headline(doc)
    assert inserted_id is not None
    found = db_ops.headlines.find_one({"_id": inserted_id})
    assert found is not None
    assert found["screenshot"]["url"] == s3_key

    # Cleanup after
    # s3.delete_prefix("test/e2e/")
    db_ops.headlines.delete_many({"test_marker": True})


def test_print_uploaded_s3_keys():
    print("\nUploaded S3 keys for visual inspection:")
    for key in uploaded_s3_keys:
        print(key) 