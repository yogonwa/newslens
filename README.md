# NewsLens

NewsLens is a comprehensive news analysis platform that captures and analyzes news headlines from multiple sources over time. It combines Wayback Machine archiving with live site scraping to provide a historical perspective on news coverage.

## Features

### MVP (Current Focus)
- **Visual News Comparison**: 5x5 grid showing 5 major news sources at one point in time (first column populated, others empty for now)
- **Above-Fold Screenshots**: Captured from Wayback Machine archives or manual upload for MVP prototype
- **Editorial Context**: Headlines and editorial tags for each snapshot (optional, per source; placeholders for MVP)
- **Precise Timing**: Group snapshots by target time while preserving actual capture times
- **Interactive UI**: Thumbnail grid with expandable detailed views
- **Frontend Additions (Planned)**:
  - Filters for source, time slot, and editorial tag
  - Date range navigation (move between days)
  - Snap to current day/time on page load

### Future Enhancements
- Multi-column time progression view (fully populated)
- Sentiment analysis and emotional intensity tracking
- Topic clustering and theme analysis
- AI-powered querying and insights
- Timeline playback and historical comparison

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

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- MongoDB Atlas account
- AWS account (for S3)

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your MongoDB and AWS credentials
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

## Development Status

### Completed
- [x] Project structure and organization
- [x] MongoDB Atlas setup
- [x] Basic wayback scraping functionality
- [x] Frontend component prototypes
- [x] AWS S3 integration (bucket, IAM, env)
- [x] S3 service class implemented and tested
- [x] Manual upload plan for 5 images for MVP prototyping
- [x] MVP 5x5 grid: S3 images in first column, empty columns for future slots
- [x] Frontend/backend integration for MVP grid
- [x] Redundant seed scripts and test data removed

### In Progress
- [ ] Add support for multiple time slots (automated or manual)
- [ ] Integrate real headlines and editorial tags
- [ ] Enhance error handling and loading states
- [ ] Prepare for production deployment
- [ ] Add frontend filters, date navigation, and snap-to-current
- [ ] Build historical data capture script (Wayback, 1/1/2025 to present, all slots)
- [ ] Add go-forward scraper tool (live or Wayback, all slots)

## Next Steps
1. Add support for multiple time slots (all 5 slots, all sources)
2. Integrate real headlines and editorial tags (optional, per source)
3. Enhance error handling and loading states
4. Add frontend filters, date navigation, and snap-to-current
5. Build historical data capture script for 1/1/2025 to present (Wayback, all slots)
6. Add go-forward scraper tool for live or Wayback data
7. Prepare for production deployment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Wayback Machine](https://archive.org/web/) for providing archived web content
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Playwright](https://playwright.dev/) for browser automation
- [React](https://reactjs.org/) for frontend development
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [MongoDB](https://www.mongodb.com/) for database
- [AWS S3](https://aws.amazon.com/s3/) for image storage

## Audience
This README is for developers, contributors, and automation agents (e.g., Chat cursor bot) to understand project goals, current status, and next steps. All implementation should align with the day-based, multi-slot news comparison vision.
