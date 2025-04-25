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
- Focus on single-column grid view showing 5 major news sources at one point in time
- Capture above-fold screenshots and headlines from Wayback Machine archives
- Store in AWS S3 (screenshots) and MongoDB (metadata)
- Features:
  - Thumbnail grid view with hover timestamp
  - Expandable detail view showing:
    - Full above-fold screenshot
    - Prioritized headlines with editorial tags
    - Exact capture timestamp
  - Group snapshots by target timestamp (e.g., 12:00 PM) while preserving actual capture times

## Suggested News Sites
- CNN
- Fox News
- The New York Times
- The Washington Post
- USA Today

## Wayback Machine Bootstrap Strategy
Before building your live scraping system, bootstrap your dataset using historical snapshots from the Wayback Machine:

- Query the CDX API for archived homepage timestamps across CNN, Fox, NYT, etc. (last 30 days)
- Example: `https://web.archive.org/cdx/search/cdx?url=cnn.com&from=20240312&to=20240412&output=json&filter=statuscode:200&collapse=digest`
- For each snapshot:
  - Save the timestamped URL (e.g., `https://web.archive.org/web/20240411120301/http://cnn.com/`)
  - Extract main headlines and editorial metadata
  - Capture above-fold screenshot using Playwright
  - Group snapshots by target timestamp while preserving actual capture time
- Use a polite custom user-agent:  
  `User-Agent: NewsLensBot/0.1 (+https://github.com/yourusername/newslens; contact: your@email.com)`

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
   - Simplify grid to single-column view
   - Create expandable detail view
   - Implement hover states and timestamp display

4. Integration
   - Connect frontend to MongoDB and S3
   - Test end-to-end workflow
   - Deploy MVP version
