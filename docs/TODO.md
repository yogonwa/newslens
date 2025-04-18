# NewsLens Project - Progress and TODO

## Completed Work (Phase 0 - Wayback Machine Prototype)
- [x] Created initial Wayback Machine CDX API scraper
- [x] Implemented screenshot capture functionality using Playwright
  - Successfully capturing "above the fold" (1920x1080) viewport
  - Also saving full-page screenshots for reference
- [x] Basic metadata extraction
  - Page title and description
  - Initial headline extraction
  - Raw HTML storage for debugging
- [x] File organization
  - Screenshots stored in `screenshots/` directory
  - Metadata JSON alongside screenshots
  - Raw HTML saved for debugging purposes

## Immediate Next Steps

### 1. Refine Metadata Extraction
- [ ] Improve headline detection accuracy
  - Create site-specific selectors for main headlines
  - Filter out navigation/section headers more effectively
  - Add priority/ranking to headlines based on position/prominence
- [ ] Add additional metadata fields
  - Article timestamps
  - Author information
  - Article categories/sections
  - Image captions/descriptions
- [ ] Create test suite for metadata extraction
  - Verify accuracy across different sites
  - Handle edge cases (missing data, different layouts)

### 2. Multi-Source Implementation
- [ ] Extend scraping to all target news sources:
  - CNN (current prototype)
  - Fox News
  - The New York Times
  - The Washington Post
  - USA Today
- [ ] Create source-specific configurations
  - Custom headline selectors per site
  - Site-specific metadata rules
  - Handle different page structures
- [ ] Implement rate limiting and polite scraping
  - Respect robots.txt
  - Add appropriate delays between requests
  - Handle errors gracefully

### 3. UI Prototype Development
- [ ] Design initial grid-based UI
  - Time-based X-axis (6 snapshots per day)
  - Source-based Y-axis (5 news sources)
  - Thumbnail preview system
- [ ] Implement image optimization
  - Compress screenshots for faster loading
  - Generate thumbnails for grid view
  - Implement lazy loading
- [ ] Add interactive features
  - Click to expand screenshots
  - Hover previews
  - Side-by-side comparison view

### 4. Storage Implementation
- [ ] Design storage schema
  - Screenshot storage strategy (local vs cloud)
  - Metadata database structure
  - Indexing for quick retrieval
- [ ] Evaluate storage options
  - Local file system vs Cloud storage (S3, etc.)
  - Database options (SQLite, PostgreSQL)
  - CDN for image delivery
- [ ] Implement backup strategy
  - Regular backups
  - Data retention policy
  - Recovery procedures

### 5. Integration
- [ ] Create main application loop
  - Scheduled scraping (every 3 hours)
  - Error handling and retry logic
  - Monitoring and alerts
- [ ] Build API layer
  - Endpoints for retrieving snapshots
  - Filtering and search capabilities
  - Metadata querying
- [ ] Implement caching
  - Cache frequently accessed images
  - Cache metadata queries
  - Optimize performance

## Future Considerations
- Analytics and insights generation
- User authentication system
- Advanced comparison tools
- AI-powered analysis of coverage differences
- Export and sharing capabilities
- Mobile-responsive design
- API access for researchers

## Notes
- Current focus is on perfecting single-source scraping before scaling to multiple sources
- Need to ensure consistent handling of paywalls and subscription-only content
- Consider implementing a logging system for better debugging
- May need to adjust screenshot dimensions based on common device sizes
- Consider implementing a configuration file for easy adjustments 