# EPIC: Refactor and Unify Wayback News Scraper

## Overview
This project consolidates and modernizes the current fragmented logic used to scrape, process, crop, and store web page screenshots and metadata from the Wayback Machine for five major news sources: CNN, Fox News, The New York Times, The Washington Post, and USA Today.

The goal is to create a maintainable, modular pipeline that:
- Fetches Wayback snapshots for specific sources, dates, and times
- Captures a full-page screenshot
- Applies source-specific cropping rules
- Uploads the final image to S3
- Extracts headline metadata
- Saves the result to MongoDB

This refactor will centralize scattered logic from `scrape_day_grid_new.py`, `take_screenshots.py`, and the five `crop_*.py` modules into a unified and extensible architecture.

---

## Components

### 1. **Main Driver: `main_scraper.py`**
A new script that drives the end-to-end pipeline.

#### Responsibilities:
- Accept CLI args for date range and time slots
- For each news source, date, and time:
  - Query Wayback CDX API for nearest snapshot
  - Construct Wayback URL
  - Capture full-page screenshot (in memory)
  - Route to appropriate cropping logic
  - Upload cropped image to S3
  - Extract metadata (e.g., headlines)
  - Save to MongoDB

---

### 2. **Screenshot Capture: `screenshot_service.py`**
Extracted from `take_screenshots.py`

#### Responsibilities:
- Use Playwright to capture full-page PNG image from a Wayback URL
- Set viewport (`1920x2000`) and `device_scale_factor=2.0` for HiDPI consistency
- Return an in-memory image buffer (no local file saving)

---

### 3. **Cropping Logic: `crop_rules/` package**
Each source (`cnn`, `fox`, `nytimes`, `washingtonpost`, `usatoday`) has a crop module.

#### Refactor Tasks:
- Each `crop_*.py` should be updated to:
  - Accept an in-memory image (e.g., Pillow Image object)
  - Return a new Pillow Image object after cropping
- Remove any local filesystem references
- Create shared interface for routing by source key

---

### 4. **Storage Service: `s3_service.py`**
From existing logic in `scrape_day_grid_new.py`

#### Responsibilities:
- Upload in-memory image buffer to S3 bucket
- Use IAM roles or scoped credentials for security
- Use `BytesIO` for in-memory upload (avoid disk I/O)
- Return public or signed S3 URL
- Optionally use server-side encryption (SSE-S3 or SSE-KMS)

---

### 5. **Metadata Extraction: `extractors/` package**
Existing logic appears in `get_extractor()` and extractor modules

#### Responsibilities:
- Parse HTML of each Wayback URL
- Extract structured metadata like headline text, tags, subheadlines, etc.

---

### 6. **Persistence: `db_service.py`**
Wrapper for MongoDB insert/update operations.

#### Responsibilities:
- Insert new document into `HeadlineDocument`
- Include:
  - `source`
  - `display_timestamp` and `actual_timestamp`
  - `s3_url`
  - `headlines[]`
  - `meta fields` (e.g., confidence, collection method)
- Add indexes on `source`, `display_timestamp`, and `status`
- Sanitize and validate extracted data

---

## Inputs
- `start_date`, `end_date`
- `times = ["06:00", "09:00", "12:00", "15:00", "18:00"]`
- `sources = ['cnn.com', 'foxnews.com', 'nytimes.com', 'washingtonpost.com', 'usatoday.com']`

---

## Deliverables
- [ ] `main_scraper.py`
- [ ] `screenshot_service.py`
- [ ] `s3_service.py`
- [ ] `db_service.py`
- [ ] Unified crop rule system in `crop_rules/`
- [ ] Migrated logic from `take_screenshots.py`
- [ ] Refactored metadata extraction in `extractors/`

---

## Out of Scope
- Live news scraping (non-Wayback)
- Browser testing of mobile layouts
- Any redesign of the database schema

---

## Execution Model

### Loop Strategy:
- Use a `for source in SOURCES: for timestamp in TIMESTAMPS:` structure
- Encapsulate the entire snapshot process in a single `process_snapshot()` function
- Optionally parallelize using `ThreadPoolExecutor` or move to `Celery` for scale

### Function Flow:
```python
for source in SOURCES:
    for timestamp in TIMESTAMPS:
        wayback_url = build_url(source, timestamp)
        image = take_screenshot(wayback_url)
        cropped = crop_by_source(source, image)
        s3_url = upload_to_s3(cropped, key)
        metadata = extract_headlines(wayback_url, source)
        save_to_mongo(source, timestamp, s3_url, metadata)
```

---

## Security & Performance Considerations
- Use IAM roles for S3 + Mongo access; never hardcode secrets
- Leverage `BytesIO` for in-memory image processing to avoid disk I/O
- Use structured logging with error status fields (`success`, `skipped`, `failed`)
- Ensure all snapshot/crop/upload stages fail independently — don’t crash the pipeline
- Limit concurrency to 5–10 threads depending on bandwidth and system limits

---

## Next Steps
1. Create `main_scraper.py` scaffold with CLI and loop logic
2. Move full-page screenshot logic to `screenshot_service.py`
3. Refactor `crop_*.py` files to `crop_rules/{source}.py`, ensure all take and return Pillow `Image`
4. Wire up upload logic to S3 using `s3_service.py`
5. Migrate MongoDB inserts into a shared `db_service.py`
6. Final integration and test pass with CLI

---

## Notes for Cursor Copilot
- Use Playwright with `device_scale_factor=2.0` for high-res screenshots
- All cropping is pixel-based, not DOM-based
- Images should remain in memory as much as possible to reduce I/O overhead
- Consistency in timestamp formatting (`display vs actual`) is key for DB insert

---

## Future Enhancements
- Add retry logic and circuit breakers for Wayback/CDX queries
- Add `--dry-run` and `--verbose` modes
- Add batch mode for parallel processing
- Integrate Obsidian or Airtable logging of snapshots

