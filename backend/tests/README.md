# Backend Test Suite

This directory contains unit, integration, and end-to-end tests for the backend services of the NewsLens project.

## Structure

- `test_fetcher.py`, `test_fetcher_integration.py`: Wayback fetcher unit/integration tests
- `test_croppers.py`: Cropper logic and visual output tests
- `test_headline_extractors.py`: Headline extraction logic
- `test_screenshot_service.py`, `test_screenshot_service_integration.py`: Screenshot service logic and integration (saves screenshots for manual review)
- `test_e2e_pipeline.py`: Full pipeline integration test
- `test_mongodb_crud.py`: MongoDB CRUD and schema validation
- `s3_service_test.py`, `s3_env_test.py`: S3 upload and environment tests
- `images/`: Test fixture images (do not delete)
- `crop_outputs/`: Cropped image outputs for visual inspection
- `fixtures/`: HTML and other test fixtures
- `archived/test_modern_croppers.py`: Modern cropper integration test for all 5 sources (see below)
- `../../scripts/generate_presigned_url.py`: Utility to generate S3 pre-signed URLs for test/e2e outputs

## Running Tests

1. **Install dependencies:**
   - Activate your virtual environment
   - `pip install -r requirements.txt`
   - `python -m playwright install`
2. **Set up environment:**
   - Copy `.env.example` to `.env` and fill in required values
3. **Run all tests:**
   - `pytest backend/tests`
4. **Run a specific test:**
   - `pytest backend/tests/test_croppers.py`

## Archived/Modern Cropper Integration Test

- **Script:** `scripts/archived/test_modern_croppers.py`
- **Description:** Runs the modern screenshot and cropper pipeline for all 5 major sources (CNN, Fox News, NYT, USA Today, Washington Post) using Wayback URLs. Saves both the full screenshot and cropped output for each source in the `temp/` directory for visual inspection.
- **Run with:**
  ```bash
  PYTHONPATH=. python scripts/archived/test_modern_croppers.py
  ```
- **Outputs:**
  - `temp/{source}_modern.png` (full screenshot)
  - `temp/{source}_modern_cropped.png` (cropped image)

## S3 Pre-signed URL Utility

- **Script:** `scripts/generate_presigned_url.py`
- **Description:** Generates pre-signed S3 URLs for the latest test/e2e PNGs for browser-based visual inspection. Useful for sharing or reviewing outputs stored in S3.
- **Run with:**
  ```bash
  python scripts/generate_presigned_url.py
  ```
- **Outputs:**
  - Prints pre-signed URLs for all 5 test/e2e PNGs to the console (valid for 1 hour by default).

## Headline Extraction Inspection Script

- **Script:** `scripts/inspect_headlines.py`
- **Description:** Fetches Wayback URLs for all 5 major sources and prints the extracted headlines using the standardized extractor interface. Useful for manual/visual validation of headline extraction logic.
- **Run with:**
  ```bash
  PYTHONPATH=. python scripts/inspect_headlines.py
  ```
- **Outputs:**
  - Prints extracted headlines for each source to the console for review.

## Outputs
- Screenshot integration tests save files as `