# NewsLens Project - Progress and TODO

## Recent Progress (This Session)
- Automated 5x5 grid scraping for a single day (2025-04-18) for all 5 sources and 5 time slots
- Robust error handling, retry logic, and logging for scraping pipeline
- S3 and MongoDB integration for screenshots and metadata
- Confirmed end-to-end rendering in frontend grid
- Improved screenshot cropping with source-specific crop values and proper viewport handling
- Successfully refetched all failed slots from April 18th
- Identified and fixed screenshot cropping logic (changed from scroll-based to proper clip-based cropping)

## Remaining Screenshot Refetch Tasks (April 18th)
### Failed Slots to Retry:
1. New York Times:
   - 18:00 (failed due to Wayback timeout)
2. USA Today:
   - 09:00 (connection refused)
   - 12:00 (connection refused)
   - 18:00 (connection refused)

### Command to Retry Failed Slots:
```bash
PYTHONPATH=/Users/joegonwa/Projects/newslens python scripts/scrape_day_grid.py --date 2025-04-18 --times 18:00 09:00 12:00 --overwrite
```

Note: USA Today slots are showing persistent connection refused errors with Wayback Machine. May need to:
- Try at a different time when Wayback service is less loaded
- Implement longer timeout values
- Consider alternative Wayback Machine endpoints

## Current MVP Focus
- 5x5 grid for a single day, fully automated and rendered in the frontend
- All data flows: Wayback → S3/MongoDB → API → FE
- Refetch screenshots with improved cropping for better visual consistency

## Project Structure
```
newslens/
├── backend/                    # Backend services and scrapers
│   ├── scrapers/              # Scraper implementations
│   │   ├── wayback/          # Wayback Machine scraping
│   │   └── extractors/      # Headline extractors
│   ├── services/            # Business logic & S3 service
│   ├── models/             # MongoDB models
│   └── api/                 # API endpoints
├── frontend/                 # React application
│   ├── src/                 # Source code
│   │   ├── components/      # UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   └── utils/          # Helper functions
│   └── public/             # Static assets
├── shared/                  # Shared code
│   ├── types/              # Type definitions
│   └── constants/          # Shared constants
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── docs/                   # Documentation
└── config/                 # Configuration files
```

## Completed Work
- [x] Project structure and organization
- [x] MongoDB Atlas setup and configuration
- [x] Wayback scraping and headline extraction for all sources
- [x] S3 integration and automated upload
- [x] 5x5 grid scraping for a single day (2025-04-18)
- [x] Frontend/backend integration for MVP grid
- [x] Robust error handling and retry logic in scraping
- [x] Screenshot cropping implementation with proper viewport handling

## In Progress / Next Steps
- [ ] **Screenshot Reprocessing**
  - Refetch and reprocess screenshots with new cropping logic
  - Verify visual consistency across all sources
  - Document final crop values for each source
- [ ] **Date Navigation & Filtering**
  - Add date picker to frontend
  - Update API to accept date parameter and filter results
  - Allow user to view any day's 5x5 grid
- [ ] **Documentation**
  - Document scraping script usage, error recovery, and reprocessing
  - Add developer notes for onboarding and next steps

## Future Enhancements (Post-MVP)
- Editorial tag and headline metadata improvements
- Sentiment/framing analysis
- Go-forward and historical backfill automation
- Enhanced error monitoring and dashboards
- Topic clustering, word clouds, and AI-powered querying

## Optimization Improvements

### Security
- Implement API key authentication with rate limiting
- Add SSL/TLS for MongoDB connections
- Secure database credentials with proper encryption
- Add input validation and sanitization

### Scalability
- Implement Redis caching layer for frequently accessed data
- Optimize database queries with proper indexing and projections
- Add database connection pooling
- Implement batch processing for large datasets

### Performance
- Add response compression (GZip)
- Implement database query optimization
- Add connection pooling for MongoDB
- Optimize image loading and caching strategies

### Monitoring & Logging
- Add Prometheus metrics for API and database monitoring
- Implement structured logging with proper log levels
- Add request tracing and performance monitoring
- Set up error tracking and alerting

### Code Quality
- Improve error handling with custom exception classes
- Add comprehensive API documentation with OpenAPI
- Implement better type checking and validation
- Add more detailed code documentation

### Testing
- Add comprehensive unit tests for all components
- Implement integration tests for API endpoints
- Add performance testing for database operations
- Set up continuous integration pipeline

### Configuration
- Implement environment-based configuration management
- Add proper secrets management
- Set up configuration validation
- Add deployment environment configurations

## Audience
This TODO is for developers, contributors, and automation agents (e.g., Chat cursor bot) to understand project status, priorities, and next steps. All implementation should align with the day-based, multi-slot news comparison vision.

## Intermediary Milestone: Full 5x5 Grid for a Single Day

**Goal:**
Automate the full pipeline for a single day, all 5 fixed time slots (6am, 9am, 12pm, 3pm, 6pm), for all 5 sources—using real Wayback data, publishing to S3 and MongoDB, and rendering in the frontend grid (no filters or navigation yet).

**Status:**
- [x] Complete and demoed for 2025-04-18
- [ ] Ready for date navigation and UX improvements

**Why:**
- Exercises the entire data pipeline (Wayback → S3/MongoDB → API → FE) for all grid cells for a single day.
- Surfaces edge cases (missing snapshots, time rounding, S3/Mongo errors) in a controlled scope.
- Provides a visually complete MVP grid for a single day, which is a powerful demo and a solid foundation for further automation.
- Keeps frontend changes minimal (just render the full 5x5 grid for a hardcoded day).

**Steps:**
1. Backend: Build a script to fetch Wayback snapshots for all 5 sources at all 5 fixed times for a single day (e.g., 2025-04-18), extract headlines/editorial tags, upload screenshots to S3, and save metadata to MongoDB. Ensure idempotency and logging.
2. Frontend: Update the grid to render all 5x5 cells for the chosen day, using real backend data. No filters, navigation, or date pickers yet—just a hardcoded day.
3. Integration: Confirm all cells populate as expected. Document any issues (e.g., missing data, API shape needs).

This milestone validates the architecture and sets up the next phase: historical backfill, date navigation, and go-forward scraping.

## Current Focus: Screenshot Cropping Fix
### Issue Identified
- Current screenshots in S3 still show large banner spaces because the previous cropping method was incorrectly using scroll instead of actual image cropping

### Next Steps
1. **Verify Crop Values** (Optional)
```python
# Current crop values to verify:
SOURCE_CROPS = {
    'cnn': 550,
    'fox': 936,
    'nytimes': 640,
    'usatoday': 730,
    'wapo': 725
}
```

2. **Refetch All Screenshots**
```bash
# Run from project root:
PYTHONPATH=/Users/joegonwa/Projects/newslens python scripts/scrape_day_grid.py --date 2025-04-18 --times 06:00 09:00 12:00 15:00 18:00 --overwrite
```

3. **Verify Results**
- Check frontend grid at http://localhost:5173
- Confirm banner spaces are properly cropped for all sources
- If any source's crop value needs adjustment, update SOURCE_CROPS and rerun for that source

4. **If Needed: Source-Specific Refetch**
To refetch specific sources, comment out others in NEWS_SOURCES and run the same command:
```python
# Example: Only fetch Fox News
NEWS_SOURCES = [
    # {"name": "CNN", "url": "https://www.cnn.com", "key": "cnn.com"},
    {"name": "Fox News", "url": "https://www.foxnews.com", "key": "foxnews.com"},
    # {"name": "The New York Times", "url": "https://www.nytimes.com", "key": "nytimes.com"},
    # {"name": "The Washington Post", "url": "https://www.washingtonpost.com", "key": "washingtonpost.com"},
    # {"name": "USA Today", "url": "https://www.usatoday.com", "key": "usatoday.com"},
]
```

### Implementation Details
The screenshot cropping has been updated to use Playwright's clip option instead of scrolling:
```python
page.screenshot(
    path=tmp.name,
    clip={
        'x': 0,
        'y': crop_top,
        'width': 1920,
        'height': 1080
    }
)
```

This ensures the top portion of each screenshot is actually removed rather than just scrolled out of view. 