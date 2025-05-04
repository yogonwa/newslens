import pytest
from backend.scrapers.screenshot_service import ScreenshotService
from backend.scrapers.crop_rules.cnn import CNNCropper
from backend.services.s3_service import S3Service
from backend.db.operations import db_ops
from backend.db.models import HeadlineDocument, Headline, Screenshot, DocumentHeadlineMetadata
from backend.scrapers.extractors.headline_extractors import get_extractor
from datetime import datetime
from bson import ObjectId
from io import BytesIO
from bs4 import BeautifulSoup
import asyncio

WAYBACK_URL = "https://web.archive.org/web/20240101000000/https://www.cnn.com/"
S3_TEST_PREFIX = "test/e2e/"
S3_IMAGE_KEY = f"{S3_TEST_PREFIX}cnn_20240101_0000.png"

@pytest.mark.asyncio
async def test_e2e_cnn_pipeline():
    # Cleanup before
    s3 = S3Service()
    s3.delete_prefix(S3_TEST_PREFIX)
    db_ops.headlines.delete_many({"test_marker": True})

    # 1. Capture screenshot
    service = ScreenshotService()
    await service._init_browser()
    image_bytesio = await service.capture(WAYBACK_URL)
    assert image_bytesio is not None
    image_bytesio.seek(0)

    # 2. Crop
    from PIL import Image
    image = Image.open(image_bytesio)
    cropper = CNNCropper()
    cropped, crop_metadata = cropper.crop(image)
    output_bytes = BytesIO()
    cropped.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    # 3. Upload to S3
    s3.upload_bytes(output_bytes.getvalue(), S3_IMAGE_KEY, content_type="image/png")
    files = s3.list_files(S3_TEST_PREFIX)
    assert S3_IMAGE_KEY in files

    # 4. Extract headlines
    # Use Playwright to get HTML for extraction
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(WAYBACK_URL, wait_until='domcontentloaded')
        html = await page.content()
        await browser.close()
    soup = BeautifulSoup(html, "html.parser")
    extractor = get_extractor("cnn")
    headlines = extractor.extract_headlines(soup, base_url="https://www.cnn.com/")
    assert headlines and isinstance(headlines, list)

    # 5. Store in MongoDB
    doc = HeadlineDocument(
        source_id=ObjectId(),
        display_timestamp=datetime(2024, 1, 1, 0, 0),
        actual_timestamp=datetime.utcnow(),
        headlines=[Headline(text=h["headline"], type="main", position=i+1) for i, h in enumerate(headlines)],
        screenshot=Screenshot(
            url=S3_IMAGE_KEY,
            format="png",
            size=output_bytes.getbuffer().nbytes,
            dimensions={"width": cropped.width, "height": cropped.height},
            wayback_url=WAYBACK_URL
        ),
        metadata=DocumentHeadlineMetadata(
            page_title="CNN Test Page",
            url=WAYBACK_URL,
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
    assert found["screenshot"]["url"] == S3_IMAGE_KEY

    # Cleanup after
    s3.delete_prefix(S3_TEST_PREFIX)
    db_ops.headlines.delete_many({"test_marker": True}) 