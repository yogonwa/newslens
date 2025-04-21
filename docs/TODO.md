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

## Latest Progress (Phase 1 - Multi-Source Implementation)
- [x] CNN Implementation
  - Headline extraction with semantic structure
  - Unicode normalization
  - Subheadline support
- [x] Fox News Implementation
  - Headline extraction with semantic structure
  - Editorial tags/kickers capture
  - Unicode normalization
  - Subheadline support
- [x] New York Times Implementation
  - Created NYTHeadlineExtractor
  - Implemented basic headline extraction
  - Added test suite for headline extraction
  - Support for story-wrapper sections
- [x] Washington Post Implementation
  - Created WaPoHeadlineExtractor
  - Implemented basic headline extraction
  - Added support for Wayback Machine URL handling
  - Simplified to focus on core headline extraction

## Immediate Next Steps

### 1. Complete Source Implementations
- [ ] USA Today Implementation
  - Create USATodayHeadlineExtractor
  - Analyze and implement site-specific metadata
  - Test with wayback snapshots

### 2. UI Prototype Development
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

### 3. Storage Implementation
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

### 4. Integration
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
- Current focus is on completing USA Today implementation and moving to UI prototype
- Need to determine optimal storage solution for screenshots and metadata
- Consider implementing a logging system for better debugging
- May need to adjust screenshot dimensions based on common device sizes
- Consider implementing a configuration file for easy adjustments 