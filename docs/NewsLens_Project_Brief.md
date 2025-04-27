# Project Brief: Daily News Divergence (Working Name: NewsLens)

## Core Idea
Build a tool that automatically captures and archives homepage snapshots and headlines from major news outlets (e.g., CNN, Fox News, NYT) multiple times per day. Over time, this creates a visual and textual library to compare how different sources present, frame, and prioritize news.

## Primary Goals
- Visually track how different outlets report the same events
- Build a historical archive of homepage snapshots
- Enable framing analysis through headlines, sentiment, and layout
- Eventually support AI-powered queries like:
  *"How did CNN vs. Fox cover the US tariff announcement on April 12th at noon?"*

## MVP Scope (Updated)
- **5x5 grid**: 5 major news sources × 5 time slots (first column populated with real S3 images, others empty for now)
- **Above-fold screenshots**: Captured from Wayback Machine or manual upload for MVP
- **Backend/Frontend integration**: Real S3 images and metadata served via API and displayed in React grid
- **Features:**
  - Thumbnail grid view with hover timestamp
  - Expandable detail view showing:
    - Full above-fold screenshot
    - Prioritized headlines with editorial tags (placeholders for MVP)
    - Exact capture timestamp
  - Group snapshots by target timestamp (e.g., 6:00 AM) while preserving actual capture times

## Suggested News Sites
- CNN
- Fox News
- The New York Times
- The Washington Post
- USA Today

## MVP Status
- [x] S3 integration and manual upload of 5 images
- [x] Backend API serving presigned URLs and metadata
- [x] Frontend grid displays real S3 images in first column, empty columns for future slots
- [x] End-to-end MVP demo complete

## Next Steps
- Add support for multiple time slots (automated or manual)
- Integrate real headlines and editorial tags
- Enhance error handling and loading states
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

3. Frontend Implementation
   - Simplify grid to single-column view (done for MVP, now 5x5 grid with first column populated)
   - Create expandable detail view
   - Implement hover states and timestamp display

4. Integration
   - Connect frontend to MongoDB and S3
   - Test end-to-end workflow
   - Deploy MVP version
