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
- [x] USA Today Implementation
  - Created USATodayHeadlineExtractor
  - Implemented comprehensive headline extraction
  - Added support for multiple content structures:
    - Top table with hero articles
    - Section bundles
    - Legacy structure fallback
  - Implemented priority-based sorting system
    - Hero articles (priority 0)
    - Top table categories (1-3)
    - News categories (4-6)
    - Sports/Entertainment (7-8)
    - Tech/Wellness (9-10)
    - Lifestyle categories (11-18)
  - Added metadata extraction:
    - Categories
    - Timestamps
    - Editorial tags
    - Subheadlines

## Immediate Next Steps

### 1. UI Prototype Development
- [ ] Design initial grid-based UI
  - Time-based X-axis (6 snapshots per day)
  - Source-based Y-axis (5 news sources)
  - Thumbnail preview system
  - Priority-based headline display
- [ ] Implement image optimization
  - Compress screenshots for faster loading
  - Generate thumbnails for grid view
  - Implement lazy loading
- [ ] Add interactive features
  - Click to expand screenshots
  - Hover previews with headline information
  - Side-by-side comparison view
  - Category filtering based on priority levels

### 2. Storage Implementation
- [ ] Design storage schema
  - Screenshot storage strategy (local vs cloud)
  - Metadata database structure with priority fields
  - Indexing for quick retrieval
- [ ] Evaluate storage options
  - Local file system vs Cloud storage (S3, etc.)
  - Database options (SQLite, PostgreSQL)
  - CDN for image delivery
- [ ] Implement backup strategy
  - Regular backups
  - Data retention policy
  - Recovery procedures

### 3. Integration
- [ ] Create main application loop
  - Scheduled scraping (every 3 hours)
  - Error handling and retry logic
  - Monitoring and alerts
- [ ] Build API layer
  - Endpoints for retrieving snapshots
  - Filtering by priority/category
  - Search capabilities
  - Metadata querying
- [ ] Implement caching
  - Cache frequently accessed images
  - Cache metadata queries
  - Optimize performance

## Future Considerations
- Analytics and insights generation
  - Category distribution analysis
  - Priority trend analysis
  - Source comparison by category
- User authentication system
- Advanced comparison tools
- AI-powered analysis of coverage differences
- Export and sharing capabilities
- Mobile-responsive design
- API access for researchers

## Notes
- Current focus should shift to UI prototype development
- Need to determine optimal storage solution for screenshots and metadata
- Consider implementing a logging system for better debugging
- May need to adjust screenshot dimensions based on common device sizes
- Consider implementing a configuration file for easy adjustments
- Priority system may need refinement based on user feedback 