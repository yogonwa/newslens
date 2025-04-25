# NewsLens

NewsLens is a comprehensive news analysis platform that captures and analyzes news headlines from multiple sources over time. It combines Wayback Machine archiving with live site scraping to provide a historical perspective on news coverage.

## Features

### MVP (Current Focus)
- **Visual News Comparison**: Single-column grid showing 5 major news sources at one point in time
- **Above-Fold Screenshots**: Captured from Wayback Machine archives
- **Editorial Context**: Headlines and editorial tags for each snapshot
- **Precise Timing**: Group snapshots by target time while preserving actual capture times
- **Interactive UI**: Thumbnail grid with expandable detailed views

### Future Enhancements
- Multi-column time progression view
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

### In Progress
- [ ] S3 integration for screenshot storage
- [ ] Above-fold screenshot capture
- [ ] Headline extraction improvements
- [ ] Single-column grid view
- [ ] Detail view implementation

### Next Steps
1. Infrastructure Setup
   - Configure AWS S3
   - Update MongoDB schema
   - Create S3 service

2. Data Collection
   - Update wayback scraper
   - Implement metadata extraction
   - Add timestamp grouping

3. Frontend Implementation
   - Simplify grid view
   - Create detail view
   - Add hover states

4. Integration & Deployment
   - Connect all components
   - Test workflow
   - Deploy MVP

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
