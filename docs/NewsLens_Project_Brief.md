# Project Brief: Daily News Divergence (Working Name: NewsLens)

## Core Idea
Build a tool that automatically captures and archives homepage snapshots and headlines from major news outlets (e.g., CNN, Fox News, NYT) multiple times per day. Over time, this creates a visual and textual library to compare how different sources present, frame, and prioritize news.

## Primary Goals
- Visually track how different outlets report the same events
- Build a historical archive of homepage snapshots
- Enable framing analysis through headlines, sentiment, and layout
- Eventually support AI-powered queries like:
  *“How did CNN vs. Fox cover the US tariff announcement on April 12th at noon?”*

## MVP Scope
- Scrape `h1`/`h2` headlines and metadata from 3–5 news sites
- Capture full-page screenshots every 3 hours between 6AM and 9PM EST
- Store locally or in the cloud: Screenshots (PNG/JPEG) and structured headline metadata (JSON or SQLite)
- Display in a time-grid UI with time (X-axis), sources (Y-axis), and thumbnail previews with hover/expand behavior

## Suggested News Sites
- CNN
- Fox News
- The New York Times
- The Washington Post
- USA Today

## Wayback Machine Bootstrap Strategy (Phase Zero)
Before building your live scraping system, bootstrap your dataset using historical snapshots from the Wayback Machine:

- Query the CDX API for archived homepage timestamps across CNN, Fox, NYT, etc. (last 30 days)
- Example: `https://web.archive.org/cdx/search/cdx?url=cnn.com&from=20240312&to=20240412&output=json&filter=statuscode:200&collapse=digest`
- For each snapshot:
  - Save the timestamped URL (e.g., `https://web.archive.org/web/20240411120301/http://cnn.com/`)
  - Optionally extract h1/h2 headlines from the raw HTML
  - Optionally render and screenshot the page using Playwright/Selenium
- Use a polite custom user-agent:  
  `User-Agent: NewsLensBot/0.1 (+https://github.com/yourusername/newslens; contact: your@email.com)`

## Down-the-Road Enhancements
- Sentiment & sensationalism scoring on headlines
- Visual heatmap overlays for emotional intensity
- Word clouds and n-gram language analysis
- Timeline playback and topic tracking
- AI querying layer (RAG + vector search)
- Tagging/search interface for themes like “Biden,” “war,” “immigration”

## Monetization Possibilities
- B2B SaaS for journalism schools, researchers, and watchdog groups
- Subscription tier for journalists, analysts, Substack writers
- Paid weekly newsletter with framing insights
- Grants (e.g., Knight Foundation, Mozilla)
- API access or CSV exports for power users
- Framing reports for major news events (elections, crises)

## Known Risks & Constraints
- Anti-bot protections may require Playwright, IP rotation, user-agent spoofing
- Storage at scale: 6 snapshots/day × 5 sites × ~1MB = ~900MB/month
- Legal: Screenshots of public homepages are likely OK under fair use (non-commercial)
- UX: Visual grid needs to be clear, lightweight, and easy to navigate

## Next Steps (When You Resume)
- Define final list of sources and snapshot schedule
- Prototype a Playwright script to extract `h1/h2` and full-page screenshots
- Choose and set up data storage format (JSON folder structure, SQLite DB, or cloud bucket)
- Mock up the grid-based UI prototype (Streamlit or web framework of choice)
- Lock in a project name (contenders: NewsLens, TimeGrid, Daily Divergence)
- Optionally test Wayback bootstrap using CDX API to pull 30 days of archive data
