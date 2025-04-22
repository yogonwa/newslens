# NewsLens Project - Progress and TODO

## Project Structure
```
newslens/
├── backend/                    # Backend services and scrapers
│   ├── scrapers/              # Scraper implementations
│   │   ├── wayback/          # Wayback Machine scraping
│   │   ├── live/            # Live site scraping
│   │   └── extractors/      # Headline extractors
│   ├── services/            # Business logic
│   ├── models/             # Database models
│   └── api/                 # API endpoints
├── frontend/                 # UI application
│   ├── src/                 # React application
│   │   ├── components/      # UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   └── utils/          # Helper functions
│   └── public/             # Static assets
├── shared/                  # Shared code between frontend/backend
│   ├── types/              # Type definitions
│   └── constants/          # Shared constants
├── scripts/                # Utility scripts
├── tests/                  # Test suite
│   ├── backend/
│   └── frontend/
├── docs/                   # Documentation
└── config/                 # Configuration files
```

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
- [x] Project Restructuring
  - Organized code into backend/frontend structure
  - Moved UI prototype into frontend/
  - Created dedicated directories for scrapers, tests, and scripts
  - Updated documentation to reflect new structure

- [x] Source Implementations
  - CNN Implementation
    - Headline extraction with semantic structure
    - Unicode normalization
    - Subheadline support
  - Fox News Implementation
    - Headline extraction with semantic structure
    - Editorial tags/kickers capture
    - Unicode normalization
    - Subheadline support
  - New York Times Implementation
    - Created NYTHeadlineExtractor
    - Implemented basic headline extraction
    - Added test suite for headline extraction
    - Support for story-wrapper sections
  - Washington Post Implementation
    - Created WaPoHeadlineExtractor
    - Implemented basic headline extraction
    - Added support for Wayback Machine URL handling
    - Simplified to focus on core headline extraction
  - USA Today Implementation
    - Created USATodayHeadlineExtractor
    - Implemented comprehensive headline extraction
    - Added support for multiple content structures
    - Implemented priority-based sorting system
    - Added metadata extraction (categories, timestamps, etc.)

### Database Implementation Progress
- [x] Set up MongoDB Atlas
  - Created cluster and database
  - Configured connection string
  - Implemented connection testing
  - Merged environment configurations
- [x] Implement database schema
  - Created NewsSource model
  - Created Headline model
  - Created Screenshot model
  - Defined indexes and relationships
- [ ] Create data access layer
  - Implemented basic CRUD operations
  - Set up connection pooling
  - Need to add query builders

## Immediate Next Steps

### 1. Database Implementation
- [ ] Complete data access layer
  - Add remaining CRUD operations
  - Implement query builders
  - Add data validation
  - Set up error handling
- [ ] Add data migration scripts
  - Create initial data seeding
  - Add backup procedures
  - Implement version control for schema

### 2. Storage Service
- [ ] Implement file storage
  - Create screenshot storage service
  - Set up directory structure
  - Implement cleanup routines
- [ ] Add data retention
  - Implement archiving strategy
  - Set up cleanup schedules
  - Add backup procedures

### 3. API Development
- [ ] Create API endpoints
  - Headline retrieval
  - Source management
  - Screenshot access
- [ ] Implement authentication
  - Add API key support
  - Set up rate limiting
  - Add request validation

### 4. Frontend Integration
- [ ] Connect to backend
  - Create API client
  - Implement data fetching
  - Add error handling
- [ ] Enhance UI
  - Add loading states
  - Implement error boundaries
  - Add data visualization

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
- Using local MongoDB for development
- Will implement data retention to manage storage
- Screenshots will be stored in filesystem with MongoDB references
- API will be versioned from the start
- Consider implementing a configuration file for easy adjustments
- Priority system may need refinement based on user feedback 