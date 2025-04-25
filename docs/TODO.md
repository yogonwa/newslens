# NewsLens Project - Progress and TODO

## Current MVP Focus
Single-column grid showing 5 major news sources at one point in time, with expandable views showing headlines and editorial context. Screenshots are cropped to above-fold content and grouped by target timestamp.

## Project Structure
```
newslens/
├── backend/                    # Backend services and scrapers
│   ├── scrapers/              # Scraper implementations
│   │   ├── wayback/          # Wayback Machine scraping
│   │   └── extractors/      # Headline extractors
│   ├── services/            # Business logic & S3 service
│   ├── models/             # MongoDB models
│   └── api/                 # API endpoints
├── frontend/                 # React application
│   ├── src/                 # Source code
│   │   ├── components/      # UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   └── utils/          # Helper functions
│   └── public/             # Static assets
├── shared/                  # Shared code
│   ├── types/              # Type definitions
│   └── constants/          # Shared constants
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── docs/                   # Documentation
└── config/                 # Configuration files
```

## Completed Work
- [x] Project structure and organization
- [x] MongoDB Atlas setup and configuration
- [x] Basic wayback scraping functionality
- [x] Frontend component prototypes
- [x] Initial headline extraction implementation
- [x] Documentation updates for MVP focus

## Current Progress (MVP Phase)

### Infrastructure & Storage
- [ ] AWS S3 Setup
  - [ ] Create S3 bucket for screenshots
  - [ ] Configure IAM roles and permissions
  - [ ] Set up environment variables
  - [ ] Create S3 service class
  - [ ] Implement upload/download utilities
  - [ ] Add thumbnail generation

### MongoDB Schema Updates
- [ ] Update schema for MVP focus
  - [ ] Revise snapshot model for S3 integration
  - [ ] Add timestamp grouping support
  - [ ] Update source configuration model
  - [ ] Add indexes for efficient querying
  - [ ] Implement data validation

### Data Collection
- [ ] Wayback Scraper Improvements
  - [ ] Modify for above-fold capture only
  - [ ] Add screenshot cropping/resizing
  - [ ] Enhance headline extraction
  - [ ] Implement editorial tag detection
  - [ ] Improve timestamp grouping logic
  - [ ] Add S3 upload integration

### Frontend MVP Components
- [ ] Grid View Simplification
  - [ ] Reduce to single column
  - [ ] Add hover states with timestamps
  - [ ] Implement loading states
  - [ ] Add error handling
  - [ ] Create placeholder components

- [ ] Detail View Implementation
  - [ ] Create expandable view component
  - [ ] Add headline list display
  - [ ] Show editorial context
  - [ ] Implement image loading states
  - [ ] Add error boundaries

### API Development
- [ ] Core Endpoints
  - [ ] Snapshot retrieval by timestamp
  - [ ] S3 presigned URL generation
  - [ ] Source configuration endpoint
  - [ ] Health check implementation
  - [ ] Basic error handling
  - [ ] Simple caching layer

### Testing & Quality
- [ ] Test Implementation
  - [ ] S3 service unit tests
  - [ ] API integration tests
  - [ ] Frontend component tests
  - [ ] Screenshot processing tests
  - [ ] Error handling tests

## Next Steps (Prioritized)

1. **Storage Infrastructure** (Foundation)
   - Set up AWS S3 bucket and permissions
   - Create S3 service for managing screenshots
   - Update MongoDB schema for S3 references
   - Implement thumbnail generation
   - Configure AWS credentials

2. **Data Collection** (Content)
   - Update wayback scraper for above-fold capture
   - Implement screenshot processing
   - Enhance headline extraction
   - Add S3 upload integration
   - Test with multiple sources

3. **API & Frontend** (Display)
   - Create core API endpoints
   - Update frontend for real data
   - Implement simplified grid
   - Add detail view
   - Test end-to-end flow

## Future Enhancements (Post-MVP)
- Expand to multi-column time grid (5x5)
- Add sentiment analysis
- Implement topic clustering
- Create timeline playback
- Add AI-powered querying
- Enhance mobile responsiveness
- Add data export capabilities

## Notes
- Using AWS S3 for screenshot storage
- MongoDB for metadata and references
- Focus on above-fold screenshots for MVP
- Grouping snapshots by target timestamp
- Preserving actual capture times in metadata 