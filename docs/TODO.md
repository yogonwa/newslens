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
- [x] AWS S3 Setup (bucket, IAM, env)
- [x] S3 service class implemented and tested
- [x] Manual upload plan for 5 images for MVP prototyping

## Current Progress (MVP Phase)

### Infrastructure & Storage
- [x] AWS S3 Setup
  - [x] Create S3 bucket for screenshots
  - [x] Configure IAM roles and permissions
  - [x] Set up environment variables
  - [x] Create S3 service class
  - [x] Implement upload/download utilities
  - [x] Add thumbnail generation (optional for prototype)

### Manual Data Upload for MVP
- [ ] Upload 5 local images to S3 for MVP prototype
- [ ] (Optional) Generate and upload thumbnails
- [ ] Prepare simple metadata for each image (source, timestamp, S3 key)

### Retrieval API & Frontend Integration
- [ ] Build retrieval API endpoint (presigned URLs + metadata)
- [ ] Connect frontend to API and display images
- [ ] Visual prototype of MVP grid

### MongoDB Schema Updates
- [ ] Update schema for S3 references (after prototype)

### Data Collection (Full Automation - Post-MVP)
- [ ] Integrate automated scraping logic

## Next Steps (Prioritized)

1. **Manual Upload & Metadata**
   - Upload 5 images to S3
   - Prepare metadata for each image
2. **Retrieval API**
   - Build endpoint to serve presigned URLs and metadata
3. **Frontend Integration**
   - Connect FE to API, display images
4. **(Post-prototype) Resume scraping automation**

## Notes
- Decoupling scraping logic from MVP prototype
- Focus on rapid visual prototyping with real S3 images
- S3 integration and service class complete

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