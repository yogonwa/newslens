# NewsLens

NewsLens is a comprehensive news analysis platform that captures and analyzes news headlines from multiple sources over time. It combines Wayback Machine archiving with live site scraping to provide a historical perspective on news coverage.

## Features

- **Multi-Source Support**: Currently supports CNN, Fox News, New York Times, Washington Post, and USA Today
- **Historical Analysis**: Captures news snapshots at regular intervals
- **Priority-Based Headlines**: Categorizes and prioritizes headlines based on importance
- **Interactive UI**: Grid-based interface for comparing news coverage
- **Metadata Extraction**: Captures headlines, subheadlines, editorial tags, and categories

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

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- MongoDB Atlas account (free tier sufficient)

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

3. Set up MongoDB Atlas:
- Create a free MongoDB Atlas account
- Create a new cluster
- Set up database access (username/password)
- Configure network access
- Get your connection string

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your MongoDB Atlas connection string and other settings
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
- [x] Multi-source headline extraction
- [x] Priority-based headline sorting
- [x] Basic UI prototype
- [x] MongoDB Atlas setup and configuration
- [x] Database schema design
- [x] Basic database operations implementation

### In Progress
- [ ] Complete database operations layer
- [ ] Storage service integration
- [ ] API implementation
- [ ] Frontend-backend integration

### Planned
- [ ] User authentication
- [ ] Advanced analytics
- [ ] Mobile responsiveness
- [ ] API documentation

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
