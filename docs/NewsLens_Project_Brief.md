# Project Brief: Daily News Divergence (Working Name: NewsLens)

## Core Idea
Build a tool that automatically captures and archives homepage snapshots and headlines from major news outlets (e.g., CNN, Fox News, NYT) at fixed times each day. Over time, this creates a visual and textual library to compare how different sources present, frame, and prioritize news.

## Primary Goals
- Visually track how different outlets report the same events
- Build a historical archive of homepage snapshots
- Enable framing analysis through headlines, editorial tags, and layout
- Support AI-powered queries and advanced comparison tools

## MVP Scope (Updated)
- **5x5 grid**: 5 major news sources × 5 fixed time slots per day (6am, 9am, 12pm, 3pm, 6pm)
  - Grid is day-based: each row is a source, each column is a time slot for that day
  - First column (6am) currently populated with real S3 images and headlines; others to follow
- **Above-fold screenshots**: Captured from Wayback Machine or manual upload for MVP
- **Backend/Frontend integration**: Real S3 images and metadata served via API and displayed in React grid
- **Features:**
  - Thumbnail grid view with hover timestamp
  - Expandable detail view showing:
    - Full above-fold screenshot
    - Prioritized headlines with editorial tags (optional, per source)
    - Exact capture timestamp
  - Group snapshots by target timestamp (e.g., 6:00 AM) while preserving actual capture times
  - **Frontend additions:**
    - Filters for source, time slot, and editorial tag
    - Date range navigation (move between days)
    - Snap to current day/time on page load

## Suggested News Sites
- CNN
- Fox News
- The New York Times
- The Washington Post
- USA Today

## MVP Status
- [x] S3 integration and manual upload of 5 images (6am slot)
- [x] Backend API serving presigned URLs and metadata
- [x] Frontend grid displays real S3 images in first column, empty columns for future slots
- [x] End-to-end MVP demo complete for 6am slot
- [x] Expandable detail view and headline display for 6am slot
- [x] Redundant seed scripts and test data removed
- [ ] Multi-slot support (grid is 5x5, but only 6am slot has real data)
- [ ] Real editorial tags and headline metadata (placeholders only)
- [ ] Enhanced error handling/loading states
- [ ] Production deployment readiness
- [ ] Frontend filters, date navigation, and snap-to-current

## Next Steps
- Add support for multiple time slots (automated or manual)
- Integrate real headlines and editorial tags
- Enhance error handling and loading states
- Add frontend filters, date navigation, and snap-to-current
- Prepare for production deployment

## Future Enhancements (v1/v2)
- Expand to multi-column time grid (e.g., 5x5 for time progression)
- Sentiment & sensationalism scoring on headlines
- Visual heatmap overlays for emotional intensity
- Word clouds and n-gram language analysis
- Timeline playback and topic tracking
- AI querying layer (RAG + vector search)
- Tagging/search interface for themes like "Biden," "war," "immigration"

## Monetization Possibilities
- B2B SaaS for journalism schools, researchers, and watchdog groups
- Subscription tier for journalists, analysts, Substack writers
- Paid weekly newsletter with framing insights
- Grants (e.g., Knight Foundation, Mozilla)
- API access or CSV exports for power users
- Framing reports for major news events (elections, crises)

## Known Risks & Constraints
- Anti-bot protections may require Playwright, IP rotation, user-agent spoofing
- Storage considerations: Above-fold screenshots + thumbnails in S3
- Legal: Screenshots of public homepages are likely OK under fair use (non-commercial)
- UX: Visual grid needs to be clear, lightweight, and easy to navigate

## Next Steps
1. Infrastructure Setup
   - Configure AWS S3 for screenshot storage
   - Set up MongoDB with new schema
   - Create S3 service for image management
2. Data Collection
   - Update wayback scraper for above-fold screenshots
   - Implement headline and editorial metadata extraction
   - Add timestamp grouping logic
   - Build historical data capture script for 1/1/2025 to present (all slots)
3. Frontend Implementation
   - 5x5 grid with real data for all slots
   - Filters, date navigation, and snap-to-current
   - Expandable detail view
   - Implement hover states and timestamp display
4. Integration
   - Connect frontend to MongoDB and S3
   - Test end-to-end workflow
   - Deploy MVP version

## Audience
This document is for developers, contributors, and automation agents (e.g., Chat cursor bot) to understand project goals, current status, and next steps. All implementation should align with the day-based, multi-slot news comparison vision.

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
