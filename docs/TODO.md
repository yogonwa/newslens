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

## Immediate Next Steps

### 1. Backend Setup
- [ ] Create virtual environment
  - Set up Python 3.9+ environment
  - Install required dependencies
  - Configure development environment
- [ ] Implement storage service
  - Design database schema
  - Create storage interface
  - Implement file system storage
- [ ] Create API layer
  - Set up FastAPI framework
  - Define API endpoints
  - Implement authentication

### 2. Frontend Development
- [ ] Set up development environment
  - Install Node.js dependencies
  - Configure TypeScript
  - Set up Tailwind CSS
- [ ] Implement API integration
  - Create API client services
  - Add error handling
  - Implement loading states
- [ ] Enhance UI components
  - Add priority-based headline display
  - Implement category filtering
  - Add hover previews
  - Create side-by-side comparison view

### 3. Testing and Quality Assurance
- [ ] Backend testing
  - Expand test coverage for extractors
  - Add unit tests for services
  - Implement API tests
- [ ] Frontend testing
  - Add component tests
  - Implement integration tests
  - Add end-to-end tests
- [ ] Performance testing
  - Test scraping performance
  - Measure API response times
  - Optimize image loading

### 4. Deployment Preparation
- [ ] Environment configuration
  - Create production config
  - Set up environment variables
  - Configure logging
- [ ] CI/CD setup
  - Configure GitHub Actions
  - Add automated testing
  - Set up deployment pipeline
- [ ] Monitoring
  - Implement error tracking
  - Set up performance monitoring
  - Configure alerts

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
- Current focus is on backend setup and frontend development
- Need to determine optimal storage solution for screenshots and metadata
- Consider implementing a logging system for better debugging
- May need to adjust screenshot dimensions based on common device sizes
- Consider implementing a configuration file for easy adjustments
- Priority system may need refinement based on user feedback 