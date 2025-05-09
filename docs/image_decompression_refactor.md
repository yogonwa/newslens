# Image Decompression Refactor Proposal

## Problem Statement

The NewsLens backend pipeline is encountering `PIL.Image.DecompressionBombWarning` and `DecompressionBombError` exceptions during image processing. These errors are triggered when processing large screenshots, particularly during the cropping step, and can halt the pipeline for certain sources and times. This issue impacts reliability, scalability, and operational efficiency as the project scales to process 25 images per day from January 1 to present and ongoing.

## Where the Issue Occurs

- **File:** [`main_scraper.py`](../main_scraper.py)
- **Function:** `process_snapshot`
- **Step:** After capturing a screenshot and before uploading to S3, the image is loaded and cropped:
  ```python
  image = Image.open(image_bytesio)
  cropped_img, crop_meta = cropper.crop(image)
  ```
- **Trigger:** If the image's pixel count exceeds the PIL safety threshold, a warning or error is raised.

## Impact

- **Pipeline Reliability:** Some images are not processed, resulting in incomplete data for certain sources/times.
- **Operational Overhead:** Manual intervention may be required to address failed jobs.
- **Performance:** Large images increase memory usage, processing time, and storage/bandwidth costs.
- **Scalability:** As the dataset grows, the risk and cost of failures increase.

## Likely Cause

- **Full-page screenshots** are being captured, often resulting in extremely tall images (especially for news sites with long or infinite-scroll homepages).
- **Device pixel ratio (DPR)** may be set to 2.0, further increasing pixel count.
- **No pre-validation or downscaling** is performed before cropping and saving.

## Options for Repair

### 1. Limit Screenshot Height at Capture
- **Description:** Set a maximum viewport height in the browser automation tool (e.g., Playwright, Puppeteer) to avoid capturing excessively tall images.
- **Files/Functions to Change:**
  - `backend/scrapers/screenshot_service.py` (or equivalent screenshot logic)
- **Pros:**
  - Prevents large images at the source
  - Reduces memory, storage, and bandwidth usage
  - Simple to implement and maintain
- **Cons:**
  - May miss content below the fold if needed for headlines
- **Recommendation:** **Highly recommended** as a first-line defense.

### 2. Lower Device Pixel Ratio (DPR)
- **Description:** Set the device pixel ratio to 1.0 (instead of 2.0) when capturing screenshots.
- **Files/Functions to Change:**
  - `backend/scrapers/screenshot_service.py` (browser context/page setup)
- **Pros:**
  - Reduces pixel count by up to 75%
  - Maintains full-page context at lower resolution
- **Cons:**
  - Slightly lower image quality (usually acceptable for news screenshots)
- **Recommendation:** **Recommended** for all but the most quality-sensitive use cases.

### 3. Downscale After Cropping
- **Description:** After cropping, resize the image to a maximum width/height before saving/uploading.
- **Files/Functions to Change:**
  - `main_scraper.py` (`process_snapshot`)
- **Pros:**
  - Ensures all images are within safe limits
  - Can be tuned to frontend display requirements
- **Cons:**
  - Still processes large images in memory (risk of OOM)
  - Adds an extra processing step
- **Recommendation:** **Recommended** as a secondary safeguard.

### 4. Change Image Format to JPEG
- **Description:** Save screenshots as JPEG (with quality=85–95) instead of PNG, unless transparency is required.
- **Files/Functions to Change:**
  - `main_scraper.py` (`process_snapshot` S3 upload step)
- **Pros:**
  - Reduces file size and bandwidth
  - Faster frontend loading
- **Cons:**
  - Lossy compression (may not be suitable for all use cases)
- **Recommendation:** **Optional**; use for full-page screenshots, keep PNG for UI/graphics.

### 5. Pre-validate Image Size Before Processing
- **Description:** Check image dimensions before opening/cropping; skip or downscale if too large.
- **Files/Functions to Change:**
  - `main_scraper.py` (`process_snapshot`)
- **Pros:**
  - Prevents pipeline crashes
- **Cons:**
  - May skip some images if not handled with downscaling
- **Recommendation:** **Recommended** as a defensive measure.

## Recommendations

- **Primary:**
  1. Limit screenshot height at capture (in `screenshot_service.py`)
  2. Lower device pixel ratio to 1.0 (in `screenshot_service.py`)
  3. Downscale after cropping to a max width/height (in `main_scraper.py`)
- **Secondary:**
  4. Change to JPEG for full-page screenshots if transparency is not needed
  5. Pre-validate image size before processing

These changes are modular, low-complexity, and align with project goals of maintainability, extensibility, and production-readiness.

## Milestones

1. **Milestone 1:** Limit screenshot height and set DPR in `screenshot_service.py`
   - **Input:** Review and update browser automation logic
   - **Output:** Screenshots are never excessively tall or high-DPI
   - **Impact:** Immediate reduction in decompression errors and resource usage

2. **Milestone 2:** Downscale images after cropping in `main_scraper.py`
   - **Input:** Add resizing logic after cropping
   - **Output:** All images within safe pixel limits
   - **Impact:** No decompression errors, consistent image sizes for frontend

3. **Milestone 3:** (Optional) Switch to JPEG for full-page screenshots
   - **Input:** Update image save/upload logic
   - **Output:** Smaller file sizes, faster frontend
   - **Impact:** Lower storage and bandwidth costs

4. **Milestone 4:** Add pre-validation of image size before processing
   - **Input:** Add dimension checks before cropping
   - **Output:** Pipeline skips or downscales oversized images
   - **Impact:** Increased robustness

## Inputs and Outputs

- **Inputs:** Full-page screenshots from browser automation, current cropping logic, S3 upload logic
- **Outputs:** Cropped, downscaled, and compressed images stored in S3 and referenced in MongoDB, ready for frontend consumption

## References
- [`main_scraper.py`](../main_scraper.py) — cropping, resizing, and upload logic
- `backend/scrapers/screenshot_service.py` — screenshot capture settings (viewport, DPR)
- Frontend: [`frontend/src/components/NewsGrid.tsx`](../frontend/src/components/NewsGrid.tsx) — image display (no changes needed if backend is fixed)

## Conclusion

Implementing these changes will ensure the NewsLens pipeline is robust, scalable, and production-ready, with minimal risk of decompression errors and optimal performance for both backend and frontend. The recommended steps are modular, low-complexity, and align with the project's long-term goals. 