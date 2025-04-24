# NewsLens

NewsLens is a tool to capture, archive, and analyze the homepages of major news websites. The goal is 
to visually and textually track how different sources frame and present news events throughout the day.

## Features

Current:
- Wayback Machine integration for historical data bootstrapping
- Homepage screenshot capture (above-the-fold and full-page)
- Headline and metadata extraction
- Support for multiple news sources (CNN, Fox News, NYT, WaPo, USA Today)

Coming Soon:
- Time-grid visual UI for easy comparison
- Sentiment and framing analysis
- Advanced search and filtering
- Historical trends and patterns

## Project Status

Currently in Phase 0 (Prototype):
- ✅ Wayback Machine CDX API integration
- ✅ Screenshot capture using Playwright
- ✅ Basic metadata extraction
- 🚧 Refining headline detection
- 🚧 Multi-source implementation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yogonwa/newslens.git
cd newslens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

3. Run the scraper:
```bash
python process_first_url.py
```

## Project Structure

```
newslens/
├── docs/
│   ├── NewsLens_Project_Brief.md   # Detailed project overview
│   └── TODO.md                     # Development roadmap
├── wayback_scraper.py             # Wayback Machine CDX API scraper
├── process_first_url.py           # Screenshot and metadata processor
├── requirements.txt               # Python dependencies
└── screenshots/                   # Generated screenshots and metadata
```

## Generated Files

The scraper generates three types of files for each capture:
- `{site}_{timestamp}.png` - Above-the-fold screenshot (1920x1080)
- `{site}_{timestamp}_metadata.json` - Extracted headlines and metadata
- `{site}_{timestamp}_raw.html` - Raw HTML for debugging

## Contributing

See [TODO.md](docs/TODO.md) for the current development roadmap.

## Future Plans

- Implement grid-based UI for visual comparison
- Add AI-powered analysis of coverage differences
- Create API for researchers and analysts
- Develop advanced comparison tools
- Add mobile-responsive design

## License

[License details to be added]

## Contact

[Contact information to be added]
