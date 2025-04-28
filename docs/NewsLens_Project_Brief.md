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
  - All 5x5 cells for a single day (2025-04-18) are now populated with real S3 images and headlines
- **Above-fold screenshots**: Captured from Wayback Machine, with plan to crop top whitespace/banners for better UX (crop values may vary by source)
- **Backend/Frontend integration**: Real S3 images and metadata served via API and displayed in React grid
- **Features:**
  - Thumbnail grid view with hover timestamp
  - Expandable detail view showing:
    - Full above-fold screenshot
    - Prioritized headlines with editorial tags (optional, per source)
    - Exact capture timestamp
  - Group snapshots by target timestamp (e.g., 6:00 AM) while preserving actual capture times
  - **Frontend additions (Next):**
    - Date navigation (move between days)
    - Filters for source, time slot, and editorial tag
    - Snap to current day/time on page load

## Suggested News Sites
- CNN
- Fox News
- The New York Times
- The Washington Post
- USA Today

## MVP Status
- [x] S3 integration and automated upload for all 5x5 cells for a single day
- [x] Backend API serving presigned URLs and metadata
- [x] Frontend grid displays real S3 images for all slots for a single day
- [x] End-to-end MVP demo complete for 5x5 grid
- [x] Expandable detail view and headline display for all slots
- [x] Robust error handling and retry logic in scraping
- [ ] Date navigation and filtering (in progress)
- [ ] Per-source screenshot cropping (planned)
- [ ] Production deployment readiness

## Next Steps
- Add support for date navigation and filtering in frontend and backend
- Implement per-source screenshot cropping to remove top whitespace/banners (crop values may vary by source)
- Enhance error handling and loading states
- Prepare for production deployment

## Future Enhancements (v1/v2)
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
   - Date navigation and filtering (in progress)
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

**Status:**
- [x] Complete and demoed for 2025-04-18
- [ ] Ready for date navigation and UX improvements
