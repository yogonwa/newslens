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

## Outputs
- Screenshot integration tests save files as `test_fullsize_screenshot_<source>.png` in the project root.
- Cropper tests save outputs in `backend/tests/crop_outputs/`.

## Troubleshooting
- Ensure test images in `backend/tests/images/` are present and not gitignored.
- If Playwright or browser errors occur, rerun `python -m playwright install`.
- MongoDB and S3 tests require valid credentials in `.env`.

## Notes
- Do not delete or ignore `backend/tests/images/` unless you have a backup.
- `.DS_Store` and other system files are ignored by default. 