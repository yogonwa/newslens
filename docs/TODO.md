# NewsLens Project - Progress and TODO

## Recent Progress (This Session)
- Automated 5x5 grid scraping for a single day (2025-04-18) for all 5 sources and 5 time slots
- Robust error handling, retry logic, and logging for scraping pipeline
- S3 and MongoDB integration for screenshots and metadata
- Confirmed end-to-end rendering in frontend grid

## Current MVP Focus
- 5x5 grid for a single day, fully automated and rendered in the frontend
- All data flows: Wayback → S3/MongoDB → API → FE

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

## In Progress / Next Steps
- [ ] **Date Navigation & Filtering**
  - Add date picker to frontend
  - Update API to accept date parameter and filter results
  - Allow user to view any day's 5x5 grid
- [ ] **Screenshot Cropping UX Improvement**
  - Crop top whitespace/banners from above-the-fold screenshots
  - Crop values may vary by source; needs tuning and testing
  - Parameterize crop per source in scraping script
- [ ] **Documentation**
  - Document scraping script usage, error recovery, and reprocessing
  - Add developer notes for onboarding and next steps

## Future Enhancements (Post-MVP)
- Editorial tag and headline metadata improvements
- Sentiment/framing analysis
- Go-forward and historical backfill automation
- Enhanced error monitoring and dashboards
- Topic clustering, word clouds, and AI-powered querying

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