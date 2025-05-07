# NewsLens

**NewsLens** is a modular full-stack system that captures, analyzes, and visualizes how news outlets frame headlines over time using historical snapshots from the Wayback Machine.

It consists of:

* 🧠 A **modular backend** for scraping, image cropping, metadata extraction, and uploading to MongoDB/S3
* 🖥️ A **frontend app** for exploring and filtering snapshots visually across date, source, and time slots

---

## 🎯 MVP Features

### ✅ Back End

* Pulls Wayback snapshots per source & date
* Captures full-page screenshots and crops per source rules
* Extracts headline metadata and computes sentiment
* Uploads cropped images to S3
* Stores snapshot documents in MongoDB

### ✅ Front End

* Responsive grid UI showing 5x5 matrix of sources and time slots
* Toggle sources on/off
* Filter by text query
* Navigate modal detail view w/ full image, headlines, sentiment, Wayback link
* Pick a date and auto-refresh content
* Accessible and responsive layout

---

## 🔮 Future Enhancements

* 🎥 Timeline playback mode (auto-cycle through snapshots by day)
* ⏱️ Cluster/word theme visualizations across time
* 🧠 Compare sentiment or framing by outlet ("Fox vs CNN on Topic X")
* 📦 Export filtered grid snapshots as image archive

---

## 🧱 Tech Stack

### Backend

* Python 3.9+ (FastAPI, Uvicorn)
* MongoDB Atlas
* AWS S3 (via `boto3`)
* HTML scraping with `requests`, `beautifulsoup4`, `playwright`
* Async: `motor`, `aiohttp`, `tenacity`
* Image processing with Pillow
* Logging with Loguru

### Frontend

* React 18 + TypeScript
* Tailwind CSS
* `@tanstack/react-query`
* `axios`
* Routing with React Router v6
* Visualization: `recharts`, `d3-cloud`

---

## 📂 Project Layout

```bash
NewsLens/
├── backend/                 # FastAPI + scraping + S3 + MongoDB logic
│   └── api/routes/snapshots.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── routes/          # Top-level pages like Home, Analysis, NotFound
│   │   ├── services/        # API client via axios
│   │   ├── types/           # Shared TS interfaces
│   │   └── App.tsx
│   └── public/
├── scripts/
│   └── main_scraper.py      # CLI runner to orchestrate full backend snapshot run
└── docs/
    └── Frontend_Integration_Plan.md
```

---

## 🧪 Running the App

### 1. Backend

```bash
cd backend
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Then visit: [http://localhost:5173](http://localhost:5173)

Make sure the backend API is available at `/api/snapshots?date=YYYY-MM-DD`

---

## 🌐 Routing Behavior

* `/` → redirects to `/:date` for today's snapshots
* `/:date` → main NewsGrid view
* `/analysis` → planned v2 route for visualizations
* `*` → 404 Not Found fallback

---

## 🔌 API Contract

* `GET /api/snapshots?date=YYYY-MM-DD`
* Returns array of `NewsSnapshot` objects:

```ts
interface NewsSnapshot {
  id: string; // `${sourceId}-${timeSlot}`
  source: string;
  time_slot: string;
  main_headline: string;
  sub_headlines: string[];
  thumbnailUrl: string;
  fullImageUrl: string;
  sentiment: {
    score: number;
    magnitude: number;
  };
  wayback_url: string;
}
```

---

## 📈 Development Progress

*  Snapshot grid w/ modal detail view
*  Source toggle + text search filtering
*  Date picker and dynamic route loading
*  Performance optimizations (lazy loading, shimmer cells)
*  404 fallback route
* 🔄 Analysis page scaffolding (planned for v2)

> For full component breakdown and implementation steps, see [`Frontend_Integration_Plan.md`](./docs/Frontend_Integration_Plan.md)

---

## 🙋 Contributing

This is a solo project for now, but code is modular and organized for future contributors (or AI agents like Cursor).

---

## 📜 License

MIT License. See [LICENSE](./LICENSE).

---

## 🙏 Acknowledgments

Inspired by projects and research in media bias detection, data visualization, and archival tools.

Wayback Machine snapshots © Internet Archive.




--- BELOW IS OLD README TO BE CLEANED UP-----
# NewsLens

NewsLens is a comprehensive news analysis platform that captures and analyzes news headlines from multiple sources over time. It combines Wayback Machine archiving with live site scraping to provide a historical perspective on news coverage.

## Features

### MVP (Current Focus)
- **Visual News Comparison**: 5x5 grid showing 5 major news sources at 5 fixed times for a single day (all cells now populated for 2025-04-18)
- **Above-Fold Screenshots**: Captured from Wayback Machine archives, with plan to crop top whitespace/banners for better UX (crop values may vary by source)
- **Editorial Context**: Headlines and editorial tags for each snapshot (optional, per source; placeholders for MVP)
- **Precise Timing**: Group snapshots by target time while preserving actual capture times
- **Interactive UI**: Thumbnail grid with expandable detailed views
- **Frontend Additions (Planned/Next):**
  - Date navigation (move between days)
  - Filters for source, time slot, and editorial tag
  - Snap to current day/time on page load

### Future Enhancements
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
- [x] Automated 5x5 grid scraping for a single day (2025-04-18) for all 5 sources and 5 time slots
- [x] Robust error handling, retry logic, and logging for scraping pipeline
- [x] S3 and MongoDB integration for screenshots and metadata
- [x] End-to-end rendering in frontend grid

### In Progress
- [ ] Date navigation and filtering in frontend and backend
- [ ] Per-source screenshot cropping to remove top whitespace/banners (crop values may vary by source)
- [ ] Documentation and developer onboarding notes

### Next Steps
- Add support for date navigation and filtering in frontend and backend
- Implement per-source screenshot cropping to remove top whitespace/banners
- Prepare for production deployment

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


## Backend Orchestration

The main entry point for the full scraping pipeline is `main_scraper.py` at the project root.

**To run the full pipeline:**
```bash
python main_scraper.py --start-date 2025-04-18 --end-date 2025-04-18 --times 06:00 09:00 12:00 15:00 18:00
```

See `docs/Scraper_Refactor.md` and `backend/tests/README.md` for detailed backend and test documentation.
