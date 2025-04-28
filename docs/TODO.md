# NewsLens Project - Progress and TODO

## Recent Progress (This Session)
- Connected MongoDB to frontend for end-to-end MVP test (6am slot, 5 sources, headlines displayed)
- Seed scripting and data shape aligned across MongoDB, S3, backend, and frontend
- Redundant seed scripts and mock data removed (except for local dev fallback)
- Most integration kinks resolved

## Current MVP Focus
Day-based 5x5 grid showing 5 major news sources × 5 fixed time slots (6am, 9am, 12pm, 3pm, 6pm) for a given day, with expandable views showing headlines and editorial context. Screenshots are cropped to above-fold content and grouped by target timestamp. Only 6am slot currently populated with real data.

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
- [x] Basic wayback scraping functionality
- [x] Frontend component prototypes
- [x] Initial headline extraction implementation
- [x] Documentation updates for MVP focus
- [x] AWS S3 Setup (bucket, IAM, env)
- [x] S3 service class implemented and tested
- [x] Manual upload plan for 5 images for MVP prototyping
- [x] MVP 5x5 grid: S3 images in first column, empty columns for future slots
- [x] Frontend/backend integration for MVP grid
- [x] Redundant seed scripts and test data removed

## Current Progress (MVP Phase)

### Infrastructure & Storage
- [x] AWS S3 Setup
- [x] S3 service class
- [x] Manual upload for MVP

### MVP Grid Prototype
- [x] 5x5 grid structure in frontend (day-based: 5 sources × 5 time slots)
- [x] Real S3 images in first column (6 AM)
- [x] Empty/grey columns for other time slots
- [x] Backend API serving presigned URLs and metadata
- [x] Frontend fetches and displays real data

### Next Steps (Backend)
- [ ] Build historical data capture script:
  - For each of 5 sources, across 1/1/2025 to present, for each fixed time slot (6/9/12/3/6)
  - Use Wayback archive, round to closest available time
  - Publish screenshots to S3 and metadata/headlines to MongoDB (with S3 URI ref)
  - Script should be programmatic, resumable, and log/report missing data
- [ ] Add go-forward scraper tool:
  - At each fixed time slot, fetch live homepage and headlines for each source
  - Save screenshot to S3 and metadata to MongoDB
  - Decide on live vs. Wayback as primary source for go-forward
- [ ] Generalize migration/seed script for all slots and sources
- [ ] Ensure editorial tag is supported in data model and API (optional, per source)
- [ ] Update API to serve all slots and editorial tags for frontend

### Next Steps (Frontend)
- [ ] Update grid to support and display all 5 time slots for all sources
- [ ] Add filters for source, time slot, and editorial tag
- [ ] Add date range navigation (move between days)
- [ ] Snap to current day/time on page load
- [ ] Design and implement clear UI for editorial tags (badge/label near headline)
- [ ] Remove mock data from production path (keep for local dev)
- [ ] Enhance error handling and loading states

### Integration & Testing
- [ ] Test end-to-end: seed → API → UI for at least two time slots
- [ ] Confirm editorial tags render correctly and are easy to spot in UI

### Documentation & Workflow
- [ ] Document process for adding new time slots, sources, and editorial tags
- [ ] Note any API changes and keep a changelog for FE/BE contract

## Notes
- MVP grid is visually and functionally complete for demo (6am slot)
- Ready for feedback and next feature iteration
- Focus on above-fold screenshots for MVP
- Grouping snapshots by target timestamp
- Preserving actual capture times in metadata

## Future Enhancements (Post-MVP)
- Expand to multi-column time grid (5x5)
- Add sentiment analysis
- Implement topic clustering
- Create timeline playback
- Add AI-powered querying
- Enhance mobile responsiveness
- Add data export capabilities

## Audience
This TODO is for developers, contributors, and automation agents (e.g., Chat cursor bot) to understand project status, priorities, and next steps. All implementation should align with the day-based, multi-slot news comparison vision.

## Intermediary Milestone: Full 5x5 Grid for a Single Day

**Goal:**
Automate the full pipeline for a single day, all 5 fixed time slots (6am, 9am, 12pm, 3pm, 6pm), for all 5 sources—using real Wayback data, publishing to S3 and MongoDB, and rendering in the frontend grid (no filters or navigation yet).

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