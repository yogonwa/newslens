# NewsLens Project - Progress and TODO

## Recent Progress (This Session)
- Connected 5 mockdata images to S3 and rendered them directly in the UI.
- Attempted to seed MongoDB with 5 instances containing headlines and associated S3 links.
- In progress: Unable to get MongoDB data connected to the UI. Remaining step is to get MongoDB connected to the UI to render headlines and S3 images correctly.

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
- [x] MVP 5x5 grid: S3 images in first column, empty columns for future slots
- [x] Frontend/backend integration for MVP grid

## Current Progress (MVP Phase)

### Infrastructure & Storage
- [x] AWS S3 Setup
- [x] S3 service class
- [x] Manual upload for MVP

### MVP Grid Prototype
- [x] 5x5 grid structure in frontend
- [x] Real S3 images in first column (6 AM)
- [x] Empty/grey columns for other time slots
- [x] Backend API serving presigned URLs and metadata
- [x] Frontend fetches and displays real data

### Next Steps
- [ ] Add support for multiple time slots (automated or manual)
- [ ] Integrate real headlines and editorial tags
- [ ] Enhance error handling and loading states
- [ ] Prepare for production deployment
- [ ] Connect MongoDB headline and S3 data to UI for rendering

## Notes
- MVP grid is visually and functionally complete for demo
- Ready for feedback and next feature iteration

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