# EPIC: Refactor and Modularize Wayback News Scraper
last edited 5-01-25
we have old files from bad attemptes that need to be cleaned up 
(wayback_scraper.py and wayback_scraper_new.py). If we find a file that is no longer useful
to our project move it to /scripts/archived and we can remove it later.

## Objective

Create a **composable**, **modular**, and **scalable** system to scrape and archive headline screenshots and metadata from the Wayback Machine for five major news outlets. This refactor moves away from a monolithic, tightly coupled script toward a cleanly orchestrated `main_scraper.py` controller that delegates discrete responsibilities to standalone services.

---

## Outcome

A production-grade scraping system that:

* Pulls Wayback snapshots for specified dates/times per source
* Captures full-page, high-res screenshots
* Applies source-specific cropping rules
* Extracts headline metadata
* Uploads cropped images to S3
* Persists documents to MongoDB

---

## Principles

* **Separation of Concerns**: Each module owns exactly one job.
* **In-Memory Processing**: Avoid disk I/O using `BytesIO`.
* **Reusability**: Each service can be tested, reused, and composed.
* **Observability**: Logs are structured and traceable per snapshot.
* **Scalability**: System can fan out across time slots, sources.

---

## Environment Configuration

### Required Environment Variables

```bash
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017  # MongoDB connection string
MONGO_DB=newslens                    # Database name

# AWS Configuration
AWS_ACCESS_KEY_ID=                   # AWS access key
AWS_SECRET_ACCESS_KEY=               # AWS secret key
AWS_DEFAULT_REGION=                  # AWS region (e.g., us-east-1)
S3_BUCKET_NAME=                      # S3 bucket for screenshots

# Scraper Configuration
USER_AGENT="NewsLensBot/0.1"        # Bot identifier for requests
```

### Configuration Files
- `.env`: Production environment variables (gitignored)
- `.env.example`: Template with required variables
- `config.py`: Global settings (sources, times, S3 bucket)

### Local Development Setup
1. Copy `.env.example` to `.env`
2. Configure MongoDB connection
3. Set up AWS credentials
4. Configure S3 bucket permissions

### Validation
The system validates environment on startup:
- MongoDB connection
- AWS credentials
- S3 bucket access
- Required variables present

---

## Entry Points

### CLI Interface

```python
@click.command()
@click.option('--start-date', type=click.DateTime(formats=["%Y-%m-%d"]), required=True,
              help="Start date in YYYY-MM-DD format")
@click.option('--end-date', type=click.DateTime(formats=["%Y-%m-%d"]),
              help="End date in YYYY-MM-DD format (defaults to start-date)")
@click.option('--times', type=click.STRING, multiple=True,
              help="Times to capture (HH:MM in 24h format)")
@click.option('--dry-run', is_flag=True, help="Skip DB and S3 operations")
@click.option('--verbose', is_flag=True, help="Enable detailed logging")
async def main(start_date: datetime, end_date: datetime = None, 
              times: List[str] = None, dry_run: bool = False,
              verbose: bool = False):
    """
    NewsLens Snapshot Scraper
    Captures news homepage snapshots from Wayback Machine
    """
    # Use default times if none provided
    times = times or DEFAULT_CAPTURE_TIMES
    end_date = end_date or start_date
    
    # Initialize services
    services = await initialize_services(dry_run)
    
    # Process date range
    current = start_date
    while current <= end_date:
        await process_day(current, times, services)
        current += timedelta(days=1)
```

### Execution Flow

```python
async def process_day(date: datetime, times: List[str], services: Services):
    """Process all snapshots for a given day"""
    for source in SOURCES:
        for time_str in times:
            target_dt = combine_date_time(date, time_str)
            
            try:
                await process_snapshot(source, target_dt, services)
            except Exception as e:
                logger.error(f"Failed to process {source['name']} at {target_dt}: {e}")
                continue

async def process_snapshot(source: Dict, target_dt: datetime, services: Services):
    """Core processing pipeline for a single snapshot"""
    # 1. Fetch Wayback snapshot
    snapshot = await services.wayback.fetch_snapshot(source['url'], target_dt)
    if not snapshot:
        services.tracker.record_missing(source['key'], target_dt)
        return

    # 2. Capture screenshot
    image = await services.screenshot.capture(snapshot['wayback_url'])
    
    # 3. Extract headlines
    headlines = await services.extractor.extract_headlines(source['key'], snapshot['wayback_url'])
    
    # 4. Upload screenshot
    s3_url = await services.storage.upload_screenshot(image, source['key'], target_dt)
    
    # 5. Save to database
    await services.db.save_snapshot(
        source_id=source['id'],
        display_timestamp=target_dt,
        actual_timestamp=snapshot['timestamp'],
        headlines=headlines,
        screenshot_url=s3_url,
        metadata={
            'wayback_url': snapshot['wayback_url'],
            'capture_time': datetime.utcnow()
        }
    )
```

### Service Container

```python
@dataclass
class Services:
    """Container for all service instances"""
    wayback: WaybackService
    screenshot: ScreenshotService
    extractor: HeadlineService
    storage: S3Service
    db: DBService
    tracker: SnapshotTracker

async def initialize_services(dry_run: bool = False) -> Services:
    """Initialize all required services"""
    return Services(
        wayback=WaybackService(),
        screenshot=await ScreenshotService.create(),  # Launches browser
        extractor=HeadlineService(),
        storage=S3Service() if not dry_run else MockS3Service(),
        db=DBService() if not dry_run else MockDBService(),
        tracker=SnapshotTracker()
    )
```

### Configuration

```python
# Default capture times
DEFAULT_CAPTURE_TIMES = [
    "06:00",
    "09:00",
    "12:00",
    "15:00",
    "18:00"
]

# News sources configuration
SOURCES = [
    {
        "name": "CNN",
        "url": "https://www.cnn.com",
        "key": "cnn.com"
    },
    # ... other sources ...
]
```

---

## Service Startup Sequence

### Boot Order

```python
async def bootstrap_application() -> Services:
    """
    Initialize application in correct order with proper resource management
    """
    # 1. Load Configuration
    config = load_config()
    logger.configure(config.logging)
    
    # 2. Initialize Browser (singleton)
    browser = await initialize_browser()
    
    # 3. Initialize Clients (lazy-loaded)
    mongo_client = MongoClient(lazy=True)
    s3_client = S3Client(lazy=True)
    
    # 4. Create Service Instances
    services = Services(
        wayback=WaybackService(),
        screenshot=ScreenshotService(browser),
        extractor=HeadlineService(),
        storage=S3Service(s3_client),
        db=DBService(mongo_client),
        tracker=SnapshotTracker()
    )
    
    return services

async def initialize_browser() -> Browser:
    """
    Initialize singleton Playwright browser instance
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-setuid-sandbox',
            '--no-sandbox'
        ]
    )
    
    # Register shutdown handler
    async def cleanup():
        await browser.close()
        await playwright.stop()
    
    atexit.register(lambda: asyncio.run(cleanup()))
    return browser

class LazyMongoClient:
    """Lazy-loaded MongoDB client"""
    def __init__(self, uri: str):
        self._uri = uri
        self._client = None
    
    @property
    def client(self):
        if not self._client:
            self._client = MongoClient(self._uri)
        return self._client

class LazyS3Client:
    """Lazy-loaded S3 client"""
    def __init__(self, config: Dict):
        self._config = config
        self._client = None
    
    @property
    def client(self):
        if not self._client:
            self._client = boto3.client('s3', **self._config)
        return self._client
```

### Resource Management

```python
class ScreenshotService:
    def __init__(self, browser: Browser):
        self._browser = browser
        self._context_pool = []
        self._semaphore = asyncio.Semaphore(2)  # Limit concurrent contexts
    
    async def get_context(self) -> BrowserContext:
        """Get browser context from pool or create new"""
        async with self._semaphore:
            if not self._context_pool:
                context = await self._browser.new_context(
                    viewport={'width': 1920, 'height': 2000},
                    device_scale_factor=2.0
                )
                self._context_pool.append(context)
            return self._context_pool.pop()
    
    async def release_context(self, context: BrowserContext):
        """Return context to pool"""
        self._context_pool.append(context)

class DBService:
    def __init__(self, client: LazyMongoClient):
        self._client = client
        self._collection = None
    
    @property
    def collection(self):
        """Lazy-load collection"""
        if not self._collection:
            db = self._client.client[MONGO_CONFIG['database']]
            self._collection = db[MONGO_CONFIG['collection']]
        return self._collection
```

### Main Entry Point

```python
async def main():
    """
    Main application entry point with proper startup sequence
    """
    try:
        # 1. Parse CLI args
        args = parse_arguments()
        
        # 2. Bootstrap services
        services = await bootstrap_application()
        
        # 3. Process date range
        current = args.start_date
        while current <= args.end_date:
            # Process snapshots for current day
            await process_day(current, args.times, services)
            current += timedelta(days=1)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        # Cleanup will be handled by atexit handlers
        pass

if __name__ == "__main__":
    asyncio.run(main())
```

### Key Principles

1. **Resource Initialization**
   - Config loads first
   - Browser initializes once
   - Clients lazy-load on first use
   - Resource cleanup registered early

2. **Connection Management**
   - Reuse browser instance
   - Pool browser contexts
   - Lazy-load database connections
   - Proper cleanup on exit

3. **Concurrency Control**
   - Limited browser contexts
   - Connection pooling
   - Resource semaphores
   - Graceful shutdown

4. **Error Handling**
   - Startup validation
   - Resource cleanup
   - Connection retries
   - Graceful degradation

---

## MongoDB Architecture

### Collections
- **headlines**: Main collection storing snapshot data and metadata
- **sources**: Collection storing news source configurations

### Document Models

#### HeadlineDocument
```python
class HeadlineDocument:
    source_id: ObjectId            # Reference to source document
    display_timestamp: datetime    # Target capture time
    actual_timestamp: datetime     # Actual capture time
    headlines: List[Headline]      # Array of extracted headlines
    screenshot: Screenshot         # Screenshot metadata and S3 link
    metadata: DocumentMetadata     # Capture metadata
    created_at: datetime
    updated_at: datetime
```

#### Headline
```python
class Headline:
    text: str                     # Headline text
    type: str                     # 'main' or 'secondary'
    position: int                 # Display order
    sentiment: Optional[float]    # Future sentiment analysis
    metadata: Optional[HeadlineMeta]  # Additional headline data
```

#### Screenshot
```python
class Screenshot:
    url: str                      # S3 URL
    format: str                   # Image format
    size: int                     # File size
    dimensions: Dict[str, int]    # Image dimensions
    wayback_url: Optional[str]    # Source URL
```

#### SourceDocument
```python
class SourceDocument:
    name: str                     # Display name
    url: str                      # Base URL
    active: bool                  # Source status
    metadata: SourceMetadata      # Source configuration
```

### Indexes
```python
INDEXES = {
    'headlines': [
        ('source_id', 1), ('display_timestamp', -1)  # Primary query path
        ('display_timestamp', -1)                    # Time-based queries
        ('source_id', 1)                            # Source filtering
        ('status', 1)                               # Status monitoring
    ],
    'sources': [
        ('active', 1)                               # Active source filtering
        ('name', 1)                                 # Source lookup
    ]
}
```

### Data Operations
- Upsert based on (source_id, display_timestamp)
- In-memory processing of screenshots before storage
- Structured error handling and status tracking
- Support for metadata extraction and enrichment

---

## S3 Architecture

### Configuration
```python
class S3Service:
    bucket_name: str              # From S3_BUCKET_NAME env var
    region: str                   # From AWS_DEFAULT_REGION env var
    credentials: Dict             # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
```

### Storage Structure
```
s3://[bucket_name]/
    auto/                         # Root for automated captures
        YYYY-MM-DD/              # Date-based partitioning
            [source_key]_HHMM.png # e.g., cnn.com_0600.png
```

### Operations
```python
class S3Operations:
    async def upload_screenshot(image: BytesIO, key: str) -> str:
        """Upload screenshot with proper content-type and metadata"""
        
    async def check_exists(key: str) -> bool:
        """Verify if screenshot already exists"""
        
    def generate_url(key: str) -> str:
        """Generate URL for frontend access"""
```

### Requirements

#### Storage
- Format: PNG images
- Content-Type: image/png
- Metadata: Capture timestamp, source, dimensions
- Expected size: ~1-2MB per screenshot

#### Access Patterns
- Write: Sequential uploads from scraper
- Read: High-volume reads from frontend
- Access: Public read via presigned URLs
- Concurrency: Multiple parallel uploads

#### Performance
- Support parallel uploads for different sources
- Quick access for frontend grid display
- Efficient storage for long-term archival

#### Error Handling
- Retry logic for failed uploads
- Logging of upload metrics
- Storage quota monitoring
- Duplicate detection

### Integration Points
- Screenshot Service → S3: Direct upload of captures
- Frontend → S3: URL-based access to images
- MongoDB → S3: URL references in documents
- Monitoring → S3: Storage metrics and alerts

---

## Screenshot Service Requirements

### Browser Management
```python
class PlaywrightConfig:
    version = "1.42.0"                     # Pinned in requirements.txt
    install_command = "playwright install chromium"
    browser_args = [
        '--disable-gpu',
        '--disable-dev-shm-usage', 
        '--disable-setuid-sandbox',
        '--no-sandbox'
    ]
```

### Resource Requirements
```python
class BrowserResources:
    ram_per_instance = "300-500MB"         # Baseline usage
    concurrent_contexts = 2                 # Via asyncio.Semaphore
    viewport = {
        "width": 1920,
        "height": 2000
    }
    device_scale_factor = 2.0              # High-DPI screenshots
```

### Capture Configuration
```python
class CaptureConfig:
    timeout = 120000                       # 2 minutes max per page
    wait_conditions = [
        "domcontentloaded",               # Initial page load
        "selector=body"                    # Basic content ready
    ]
    source_selectors = {
        "nytimes": "#main-content",
        "washingtonpost": ".main-content",
        # Add others as needed
    }
```

### Implementation Requirements

1. **Browser Instance Management**
   - Use singleton browser object
   - Create new context per capture
   - Clean up contexts immediately
   - Monitor memory usage

2. **Concurrency Control**
   ```python
   semaphore = asyncio.Semaphore(2)  # Limit concurrent captures
   
   async def capture(url: str) -> bytes:
       async with semaphore:
           return await take_screenshot(url)
   ```

3. **Resource Monitoring**
   - Track RAM usage per capture
   - Log duration and peak memory
   - Alert on resource exhaustion
   - Implement circuit breaking

4. **Error Handling**
   - Retry on network errors
   - Timeout for hung renders
   - Clean browser context on failure
   - Log screenshot metadata

### Example Implementation

```python
async def take_screenshot(url: str) -> bytes:
    """
    Capture full-page screenshot with proper resource management
    """
    context = await browser.new_context(
        viewport=BrowserResources.viewport,
        device_scale_factor=BrowserResources.device_scale_factor
    )
    
    try:
        page = await context.new_page()
        await page.goto(url, wait_until='domcontentloaded')
        await page.wait_for_selector('body')
        
        # Optional: Wait for source-specific content
        if source_selector := CaptureConfig.source_selectors.get(source_key):
            await page.wait_for_selector(source_selector)
            
        return await page.screenshot(full_page=True)
        
    finally:
        await context.close()
```

---

## Wayback Integration

### Snapshot Handling
```python
async def fetch_snapshot(url: str, target_dt: datetime) -> Optional[Dict]:
    """
    Fetch closest snapshot, returning None if not available
    """
    try:
        # Find closest snapshot to target time
        snapshot = await query_wayback_cdx(url, target_dt)
        if not snapshot:
            logger.warning(f"No snapshot found for {url} at {target_dt}")
            return None
            
        return {
            "wayback_url": f"{WAYBACK_BASE}{snapshot['wayback_ts']}/{url}",
            "timestamp": parse_wayback_timestamp(snapshot['wayback_ts'])
        }
    except Exception as e:
        logger.error(f"Failed to fetch snapshot: {e}")
        return None
```

### Coverage Tracking
```python
class SnapshotTracker:
    def __init__(self):
        self.missing_slots = []
        
    def record_missing(self, source: str, target_dt: datetime):
        self.missing_slots.append({
            "source": source,
            "target_time": target_dt,
            "checked_at": datetime.utcnow()
        })
    
    def report_coverage(self) -> Dict:
        return {
            "total_slots": len(self.missing_slots),
            "missing_by_source": Counter(s["source"] for s in self.missing_slots),
            "missing_by_hour": Counter(s["target_time"].hour for s in self.missing_slots)
        }
```

---

## Headline Extraction

### Service Structure
```
extractors/
├── __init__.py          # Service entry point
├── base.py             # Abstract extractor class
├── factory.py          # Extractor factory
├── sources/            # Source-specific implementations
│   ├── __init__.py
│   ├── cnn.py
│   ├── foxnews.py
│   ├── nytimes.py
│   ├── wapo.py
│   └── usatoday.py
└── selectors/          # Selector configurations
    ├── __init__.py
    ├── cnn.json
    ├── foxnews.json
    └── ...
```

### Base Extractor Interface
```python
class HeadlineExtractor(ABC):
    """Abstract base class for source-specific headline extractors"""
    
    @abstractmethod
    async def extract(self, page) -> List[Dict]:
        """Extract headlines from a loaded page"""
        pass
    
    @abstractmethod
    async def validate(self, headlines: List[Dict]) -> bool:
        """Validate extracted headlines"""
        pass
```

### Source-Specific Implementations

#### CNN Example
```python
@dataclass
class CNNSelectors:
    MAIN_HEADLINE = ".container__headline"
    SECONDARY = ".card__headline"
    BREAKING = ".breaking-news__headline"
    CONTAINER_LINK = "a.container__link--type-article"
    HEADLINE_TEXT = "span.container__headline-text"

class CNNExtractor(HeadlineExtractor):
    async def extract(self, page) -> List[Dict]:
        headlines = []
        
        # Wait for content
        await page.wait_for_selector(CNNSelectors.CONTAINER_LINK)
        
        # Extract headlines
        containers = await page.query_selector_all(CNNSelectors.CONTAINER_LINK)
        for container in containers:
            headline = await container.query_selector(CNNSelectors.HEADLINE_TEXT)
            if headline:
                text = await headline.text_content()
                url = await container.get_attribute('href')
                headlines.append({
                    'text': text.strip(),
                    'url': url,
                    'type': 'main' if CNNSelectors.MAIN_HEADLINE in await container.get_attribute('class') else 'secondary'
                })
        
        return headlines[:3]  # Top 3 headlines
```

#### Fox News Example
```python
@dataclass
class FoxNewsSelectors:
    ARTICLE = "article"
    HEADLINE = ["h2", "h3"]
    SUBHEADLINE = "p.dek, p.subtitle"
    EDITORIAL = "div.kicker span.kicker-text"
    MAIN_CONTENT = "main"

class FoxNewsExtractor(HeadlineExtractor):
    async def extract(self, page) -> List[Dict]:
        headlines = []
        
        # Wait for main content
        await page.wait_for_selector(FoxNewsSelectors.MAIN_CONTENT)
        
        # Extract headlines
        articles = await page.query_selector_all(FoxNewsSelectors.ARTICLE)
        for article in articles:
            headline = await article.query_selector(','.join(FoxNewsSelectors.HEADLINE))
            if headline:
                text = await headline.text_content()
                url = await headline.evaluate('el => el.closest("a")?.href')
                
                # Get editorial tag if present
                editorial = await article.query_selector(FoxNewsSelectors.EDITORIAL)
                tag = await editorial.text_content() if editorial else None
                
                headlines.append({
                    'text': text.strip(),
                    'url': url,
                    'editorial_tag': tag,
                    'type': 'main' if await self._is_main_headline(article) else 'secondary'
                })
        
        return headlines[:3]
```

### Quality Validation

```python
class HeadlineValidator:
    def __init__(self, source: str):
        self.source = source
        self.min_headlines = 3
        self.required_fields = ['text', 'url', 'type']
    
    def validate(self, headlines: List[Dict]) -> bool:
        if not headlines:
            logger.error(f"No headlines found for {self.source}")
            return False
            
        if len(headlines) < self.min_headlines:
            logger.warning(f"Found only {len(headlines)} headlines for {self.source}")
            return False
            
        # Verify required fields
        for headline in headlines:
            missing = [f for f in self.required_fields if f not in headline]
            if missing:
                logger.error(f"Missing required fields {missing} in headline")
                return False
                
        # Verify at least one main headline
        if not any(h['type'] == 'main' for h in headlines):
            logger.error(f"No main headline found for {self.source}")
            return False
            
        return True
```

### Integration

```python
class HeadlineService:
    def __init__(self):
        self.extractors = {
            'cnn.com': CNNExtractor(),
            'foxnews.com': FoxNewsExtractor(),
            # ... other extractors
        }
        
    async def extract_headlines(self, source: str, page) -> List[Dict]:
        extractor = self.extractors.get(source)
        if not extractor:
            raise ValueError(f"No extractor found for {source}")
            
        headlines = await extractor.extract(page)
        if not HeadlineValidator(source).validate(headlines):
            logger.warning(f"Validation failed for {source}")
            return []
            
        return headlines
```

This modular approach:
1. Separates concerns (extraction, validation, configuration)
2. Makes selectors configurable
3. Allows easy addition of new sources
4. Provides consistent validation
5. Uses async patterns consistently

---

## Basic Testing Requirements

### Manual Verification
```bash
# Test single source end-to-end
python scraper.py --source cnn --date 2024-02-20 --time "09:00" --verbose

# Expected output:
# ✓ Wayback snapshot found
# ✓ Screenshot captured (1920x2000)
# ✓ Found 12 headlines
# ✓ Saved to MongoDB
# ✓ Image uploaded to S3
```

### Local Setup Checklist
1. Environment
   ```bash
   python -m playwright install  # Install browser
   cp .env.example .env         # Configure environment
   ```

2. MongoDB
   ```bash
   mongod --dbpath ./data      # Start local MongoDB
   python utils/verify_db.py    # Test connection
   ```

3. Smoke Test
   ```bash
   # Test each source
   for source in cnn foxnews nytimes washingtonpost usatoday; do
     python scraper.py --source $source --smoke-test
   done
   ```

---

## Directory Structure

```
/wayback_scraper
├── main_scraper.py                 # CLI + Orchestrator
├── config.py                       # Global settings (sources, times, S3 bucket)
├── utils.py                        # Logging, retry, timestamp utils
│
├── wayback/
│   └── fetcher.py                  # CDX API querying logic
│
├── screenshot_service/
│   └── playwright_capture.py       # Persistent Playwright instance to return screenshots
│
├── crop_rules/
│   ├── __init__.py
│   ├── cnn.py                      # Crop params and logic per source
│   └── ...
│
├── extractors/
│   ├── __init__.py
│   ├── cnn.py                      # Metadata extractor per source
│   └── ...
│
├── s3_service/
│   └── uploader.py                 # In-memory upload to S3
│
├── db_service/
│   └── mongo_client.py             # Insert/save documents
│
└── tests/                          # Unit/integration tests
```

---

## main\_scraper.py — Sample Skeleton

```python
from datetime import datetime
from config import SOURCES, TIMES
from wayback.fetcher import fetch_snapshot
from screenshot_service.playwright_capture import ScreenshotService
from crop_rules import crop_by_source
from extractors import extract_metadata
from s3_service.uploader import upload_image
from db_service.mongo_client import save_document

async def process_snapshot(source, dt):
    snapshot = await fetch_snapshot(source['url'], dt)
    if not snapshot:
        return

    url = snapshot['wayback_url']
    image = await ScreenshotService.capture(url)
    cropped, crop_meta = crop_by_source(source['key'], image)
    s3_url = upload_image(cropped, source['key'], dt)
    headlines = extract_metadata(url, source['key'])

    save_document(
        source=source,
        timestamp=dt,
        actual_timestamp=snapshot['timestamp'],
        s3_url=s3_url,
        crop_meta=crop_meta,
        headlines=headlines
    )

# Loop and CLI omitted for brevity
```

---

## Component Contracts

### ScreenshotService

* `capture(url: str) -> PIL.Image`
* Reuses browser for efficiency


### crop\_by\_source

* `crop_by_source(key: str, image: Image) -> Tuple[Image, Dict]`
* All crop rules in `crop_rules/{source}.py`
See source-specific rules defined in scripts/archived/crop_* for all 5 sources

### fetch\_snapshot

* `fetch_snapshot(url: str, dt: datetime) -> Optional[Dict]`
* Queries CDX API, returns `{timestamp, wayback_url}`
See /scripts/archived/take_screenshots.py for a good model of how we were grabbing full-
size screenshots via Playwright

### extract\_metadata

* `extract_metadata(url: str, key: str) -> List[Dict]`
see /scripts/archived/scrape_day_grid_new.py for example of how we process metadata to mongodb

### upload\_image

* `upload_image(image: Image, key: str, dt: datetime) -> str`
* Returns S3 URL
see /scripts/archived/scrape_day_grid_new.py for example of how we process s3

### save\_document

* `save_document(...) -> None`
* Serializes all fields into MongoDB

---

## Retry Strategies

Each service requires specific retry handling to ensure reliability while preventing cascading failures.

### Service-Specific Retry Policies

#### Wayback CDX API (fetch_snapshot)
```python
@retry(max_attempts=3, backoff=exponential)
async def fetch_snapshot(...):
    """
    - Retry on: 5xx errors, timeouts
    - Backoff: Exponential with jitter
    - Expect gaps: CDX API can be flaky
    """
```

#### Screenshot Capture (ScreenshotService)
```python
@retry(max_attempts=2, backoff=fixed)
async def capture(...):
    """
    - Retry on: Network errors, page load timeouts
    - Abort on: Browser crashes, OOM errors
    - Conservative retry: Avoid hanging on fatal errors
    """
```

#### S3 Upload (upload_image)
```python
@retry(max_attempts=3, backoff=exponential)
async def upload_image(...):
    """
    - Retry on: Network errors, 5xx responses
    - Leverage: Built-in boto3 retry handling
    - Track: Upload attempts for observability
    """
```

#### Metadata Extraction (extract_metadata)
```python
@retry(max_attempts=2, backoff=fixed)
async def extract_metadata(...):
    """
    - Retry on: Failed requests, empty HTML
    - Skip retry: Malformed HTML structure
    - Validate: Content before retry attempt
    """
```

#### MongoDB Operations (save_document)
```python
@retry(max_attempts=2, backoff=exponential)
async def save_document(...):
    """
    - Retry on: Transient connection errors
    - Fallback: Log to disk if DB unreachable
    - Monitor: Failed write operations
    """
```

### Implementation Requirements

1. **Standardized Retry Utility**
   - Use tenacity or custom wrapper
   - Implement exponential backoff with jitter
   - Only retry idempotent operations

2. **Logging Requirements**
   - Tag all retries with:
     - attempt_number
     - retry_count
     - retry_delay
     - error_type
   - Log final failure state

3. **Circuit Breaking**
   - Track error rates per service
   - Break circuit on consecutive failures
   - Implement cool-down periods

4. **Monitoring**
   - Alert on retry rate increases
   - Track success rate after retries
   - Monitor average retry counts

---

## Error Reporting

### Structured Logging Requirements

Each log entry MUST contain the following fields for traceability and debugging:

```python
{
    # Required Source Context
    "source": str,                    # e.g., "cnn.com"
    "display_timestamp": datetime,    # User-intended capture time
    "actual_timestamp": datetime,     # Actual Wayback snapshot time
    
    # Operation Context
    "stage": str,                    # One of: fetch, screenshot, crop, extract, upload, save
    "status": str,                   # One of: success, failed, skipped, retried
    "snapshot_id": str,              # UUID or hash(source + timestamp)
    
    # Error Details
    "error_message": str,            # Clear, concise error description
    "error_type": str,              # Exception class name
    "stacktrace": str,              # Full stack trace (debug mode only)
    
    # Additional Context
    "attempt": int,                 # Current attempt number
    "duration_ms": int,             # Operation duration
    "metadata": dict                # Operation-specific details
}
```

### Stage-Specific Metadata

#### Fetch Stage
```python
{
    "cdx_url": str,
    "response_code": int,
    "response_size": int
}
```

#### Screenshot Stage
```python
{
    "browser_version": str,
    "viewport_size": dict,
    "page_metrics": dict
}
```

#### Crop Stage
```python
{
    "original_dimensions": dict,
    "crop_dimensions": dict,
    "crop_rules_version": str
}
```

#### Extract Stage
```python
{
    "headlines_found": int,
    "extraction_confidence": float,
    "parser_version": str
}
```

#### Upload Stage
```python
{
    "file_size": int,
    "content_type": str,
    "s3_key": str
}
```

### Implementation Guidelines

1. **Log Levels**
   - ERROR: Operation failures
   - WARNING: Retries, degraded performance
   - INFO: Successful operations
   - DEBUG: Detailed operation data

2. **Storage**
   - JSON format for machine readability
   - Rotate logs daily
   - Compress logs older than 24h
   - Retain logs for 30 days

3. **Monitoring Integration**
   - Forward logs to central collector
   - Index for quick searching
   - Set up alerts on error patterns
   - Dashboard for error rates by stage

4. **Recovery Workflow**
   - Log sufficient data for replay
   - Track dependencies between stages
   - Enable point-in-time recovery
   - Document manual intervention steps

---

## Fallback Strategy

### Null-Handling Patterns

Each service MUST implement defensive null-handling to prevent cascading failures:

```python
class ServiceResponses:
    # Wayback Fetcher
    FetchResult = {
        "wayback_url": str | "",
        "timestamp": datetime | None,
        "snapshots": List[Dict] | []
    }
    
    # Screenshot Service
    ScreenshotResult = {
        "image": BytesIO | None,
        "dimensions": Dict[str, int] | {"width": 0, "height": 0},
        "metadata": Dict | {}
    }
    
    # Headline Extractor
    HeadlineResult = {
        "headlines": List[Dict] | [],
        "confidence": float | 0.0,
        "metadata": Dict | {}
    }
    
    # S3 Upload
    UploadResult = {
        "url": str | "",
        "key": str | "",
        "metadata": Dict | {}
    }
```

### Implementation Requirements

1. **Empty Collections**
   ```python
   # DO:
   headlines = []  # Empty list
   metadata = {}   # Empty dict
   
   # DON'T:
   headlines = None
   metadata = None
   ```

2. **Optional Fields**
   ```python
   # DO:
   class Headline:
       text: str = ""              # Empty string
       position: int = 0           # Zero
       metadata: Dict = field(default_factory=dict)  # Empty dict
   
   # DON'T:
   class Headline:
       text: Optional[str] = None
       position: Optional[int] = None
       metadata: Optional[Dict] = None
   ```

3. **Service Results**
   ```python
   async def extract_headlines(url: str) -> HeadlineResult:
       try:
           # ... extraction logic ...
       except Exception as e:
           log_error(e)
           return HeadlineResult(headlines=[], confidence=0.0)
   ```

### Future Fallback Considerations

1. **Wayback Machine**
   - Return empty snapshot list on API failure
   - Prepare for future live scraping fallback
   - Cache previous successful snapshots

2. **Screenshot Service**
   - Return empty BytesIO on capture failure
   - Prepare for alternative browser engines
   - Consider cached screenshots

3. **Headline Extraction**
   - Return empty headline list on parse failure
   - Prepare for multiple parser strategies
   - Consider ML-based extraction backup

4. **Storage Services**
   - Return empty success response on failure
   - Prepare for local file system fallback
   - Consider multi-region S3 backup

### Monitoring Requirements

1. **Track Null Returns**
   ```python
   metrics.increment(f"{service_name}.empty_result", tags=[
       f"stage:{stage}",
       f"reason:{reason}"
   ])
   ```

2. **Alert Thresholds**
   - Warning: >10% empty results in 5 minutes
   - Critical: >25% empty results in 5 minutes
   - Emergency: >50% empty results in 1 minute

---

## Batch Processing

### Concurrent Snapshot Processing

```python
async def process_batch(sources: List[Dict], timestamps: List[datetime]):
    """
    Process multiple snapshots concurrently with failure isolation
    """
    semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
    failed_snapshots = []
    success_count = 0
    skip_count = 0
    
    async def safe_process_snapshot(source: Dict, dt: datetime):
        try:
            async with semaphore:
                await process_snapshot(source, dt)
                return True
        except Exception as e:
            failed_snapshots.append({
                'source': source['key'],
                'timestamp': dt,
                'error': str(e),
                'stage': getattr(e, 'stage', 'unknown')
            })
            return False

    # Create processing tasks
    tasks = [
        safe_process_snapshot(source, dt)
        for source in sources
        for dt in timestamps
    ]
    
    # Run all tasks
    results = await asyncio.gather(*tasks, return_exceptions=False)
    
    # Generate summary
    summary = {
        'total': len(tasks),
        'successful': sum(1 for r in results if r),
        'failed': len(failed_snapshots),
        'skipped': skip_count,
        'failures': failed_snapshots
    }
    
    # Log summary
    logger.info("Batch Processing Summary", extra=summary)
    
    # Detailed failure logging
    if failed_snapshots:
        logger.error(
            "Failed Snapshots",
            extra={'failures': failed_snapshots}
        )

    return summary
```

### Implementation Requirements

1. **Concurrency Control**
   - Use `asyncio.Semaphore(5)` to limit concurrent operations
   - Prevent resource exhaustion
   - Allow configuration via environment

2. **Error Isolation**
   - Wrap each `process_snapshot()` call in try/except
   - Continue batch on individual failures
   - Track failure details for reporting

3. **Failure Tracking**
   - Maintain list of failed operations
   - Record source, timestamp, error, and stage
   - Enable retry/resume capabilities

4. **Batch Summary**
   - Log total/success/fail/skip counts
   - Track timing and performance metrics
   - Enable monitoring and alerting

### Monitoring Integration

```python
# Batch-level metrics
metrics.gauge('batch.concurrent_operations', semaphore.count)
metrics.counter('batch.total_processed', len(tasks))
metrics.counter('batch.successful', summary['successful'])
metrics.counter('batch.failed', summary['failed'])
metrics.counter('batch.skipped', summary['skipped'])

# Timing metrics
metrics.timing('batch.duration', batch_duration)
metrics.timing('snapshot.average_duration', avg_snapshot_duration)
```

---

## Execution Diagram

```text
main_scraper.py
│
├── fetch_snapshot(site, dt)
│
├── ScreenshotService.capture(url)
│
├── crop_by_source(source_key, image)
│
├── upload_image(cropped_img, key, dt)
│
├── extract_metadata(url, source_key)
│
└── save_document({...})
```

---

## Next Steps

1. Stub out `main_scraper.py` with loop logic
2. Build persistent `ScreenshotService`
3. Refactor existing crop code into isolated `crop_rules/`
4. Isolate CDX logic in `wayback/fetcher.py`
5. Ensure each module returns typed outputs
6. Add minimal logging in each module
7. Add concurrency control via `asyncio.Semaphore`

---

## Future Enhancements

* Add `--dry-run`, `--only-screenshot`, and `--only-metadata` flags
* Move to Celery or distributed queue later
* Persist logs to external store (e.g., S3, Airtable)

## Service Interactions

### Strategy: Functional Composition

The system uses simple functional composition for service interactions. Each service:
- Takes Python primitives as input
- Returns Python primitives as output
- Avoids complex messaging patterns (no event bus, queues, or pub/sub)

### Data Flow

```
main_scraper.py
  └── fetch_snapshot()     → {"wayback_url": str, "timestamp": datetime}
      └── capture()        → PIL.Image
          └── crop()       → (PIL.Image, {"dimensions": dict, "crop_rules": dict})
              └── upload() → str  # S3 URL
                  └── extract() → List[Dict]  # headline metadata
                      └── save() → None
```

### Service Return Types

1. **Wayback Service**
   ```python
   def fetch_snapshot(url: str, dt: datetime) -> Optional[Dict]:
       return {
           "wayback_url": str,        # Full Wayback Machine URL
           "timestamp": datetime,      # Actual snapshot time
           "snapshots": List[Dict]    # All available snapshots
       }
   ```

2. **Screenshot Service**
   ```python
   def capture(url: str) -> PIL.Image:
       # Returns raw PIL Image object
       return screenshot
   ```

3. **Crop Service**
   ```python
   def crop_by_source(key: str, image: PIL.Image) -> Tuple[PIL.Image, Dict]:
       return (
           cropped_image,
           {
               "dimensions": {"width": int, "height": int},
               "crop_rules": {"top": int, "bottom": int, ...},
               "source": str
           }
       )
   ```

4. **S3 Service**
   ```python
   def upload_image(image: PIL.Image, key: str, dt: datetime) -> str:
       # Returns S3 URL for the uploaded image
       return f"s3://{bucket}/{key}"
   ```

5. **Headline Service**
   ```python
   def extract_metadata(url: str, source_key: str) -> List[Dict]:
       return [
           {
               "text": str,
               "type": str,  # "main" or "secondary"
               "position": int,
               "metadata": Dict  # Additional headline metadata
           }
       ]
   ```

6. **DB Service**
   ```python
   def save_document(**kwargs) -> None:
       # Saves to MongoDB, returns None
       pass
   ```

### Error Propagation

Each service should:
1. Handle its own internal errors
2. Return `None` or empty collections on recoverable errors
3. Raise exceptions for fatal errors that should stop processing
4. Include error context in return types where appropriate

Example:
```python
def fetch_snapshot(url: str, dt: datetime) -> Optional[Dict]:
    try:
        # ... fetching logic ...
        return {
            "wayback_url": snapshot_url,
            "timestamp": snapshot_time,
            "snapshots": available_snapshots
        }
    except NetworkError:
        # Recoverable - return None
        return None
    except InvalidURLError:
        # Fatal - raise
        raise
```

### Benefits of This Approach

1. **Simplicity**
   - Clear data flow
   - Easy to test
   - Easy to debug
   - No complex messaging patterns

2. **Flexibility**
   - Services can be used independently
   - Easy to modify or replace individual services
   - Simple to add new processing steps

3. **Testability**
   - Each service can be tested in isolation
   - Easy to mock return values
   - Clear interface contracts

4. **Maintainability**
   - No hidden dependencies
   - Clear error boundaries
   - Simple to trace data flow

## State Management

### Storage Strategy

The system uses three primary storage mechanisms, each optimized for specific types of data:

1. **MongoDB: Document Storage**
   ```python
   {
       "source_id": ObjectId,
       "display_timestamp": datetime,
       "actual_timestamp": datetime,
       "headlines": [
           {
               "text": str,
               "type": str,
               "position": int,
               "metadata": dict
           }
       ],
       "screenshot": {
           "url": str,          # S3 URL
           "format": str,
           "size": int,
           "dimensions": dict
       },
       "metadata": {
           "wayback_url": str,
           "capture_time": datetime
       }
   }
   ```
   - Stores structured headline data
   - References to S3 images
   - Query-optimized for time-based access
   - No runtime state

2. **S3: Image Storage**
   ```
   s3://{bucket}/
     └── auto/
         └── YYYY-MM-DD/
             └── {source_key}_{HHMM}.png
   ```
   - Raw or cropped screenshots
   - Organized by date and source
   - Public read access via presigned URLs
   - No processing state

3. **Logs: Operational Data**
   ```json
   {
     "timestamp": "2024-02-20T09:00:00Z",
     "level": "INFO|ERROR|WARNING",
     "source": "cnn.com",
     "stage": "fetch|screenshot|crop|extract",
     "status": "success|failed|skipped",
     "metadata": {
       "wayback_url": "...",
       "error": "...",
       "duration_ms": 1234
     }
   }
   ```
   - Structured JSONL format
   - Rotated daily
   - Compressed after 24h
   - Retained for 30 days

### Stateless Design

The system is designed to be stateless across processing runs:

1. **No Runtime State**
   - Each time slot processes independently
   - No caching between sources
   - No shared memory requirements

2. **Idempotent Operations**
   ```python
   # Example: Safe to run multiple times
   async def process_snapshot(source: Dict, dt: datetime):
       # Check if already processed
       if await db_ops.snapshot_exists(source['id'], dt):
           logger.info(f"Snapshot already exists for {source['name']} at {dt}")
           return
       
       # Process normally
       snapshot = await fetch_snapshot(source['url'], dt)
       # ...
   ```

3. **Failure Recovery**
   - Each stage can restart independently
   - No cleanup needed between runs
   - Safe to retry failed operations

4. **Resource Management**
   ```python
   class ScreenshotService:
       def __init__(self):
           self._browser = None
           
       async def __aenter__(self):
           self._browser = await launch_browser()
           return self
           
       async def __aexit__(self, *args):
           if self._browser:
               await self._browser.close()
               self._browser = None
   ```
   - Resources cleaned up after each operation
   - No persistent connections
   - No background tasks

### Benefits

1. **Simplicity**
   - Clear data ownership
   - No state synchronization needed
   - Easy to understand data flow

2. **Scalability**
   - Multiple instances can run safely
   - No shared state to coordinate
   - Easy to parallelize

3. **Reliability**
   - Failures don't corrupt state
   - Easy to retry operations
   - Clear audit trail in logs

4. **Maintenance**
   - Simple backup requirements
   - Clear data lifecycle
   - Easy to monitor and debug

## Implementation Order

### 1. Wayback Fetcher (`wayback/fetcher.py`)
- **Why First**: Small scope, enables all other development
- **Implementation Strategy**:
  ```python
  class WaybackFetcher:
      def __init__(self):
          self.cdx_url = "https://web.archive.org/cdx/search/cdx"
          
      async def fetch_snapshot(self, url: str, dt: datetime) -> Optional[Dict]:
          """Get closest snapshot to target time."""
          params = {
              'url': url,
              'closest': dt.strftime("%Y%m%d%H%M%S"),
              'output': 'json'
          }
          # Returns: {"wayback_url": str, "timestamp": datetime}
  ```
- **Test Strategy**: Use real CDX API with known snapshots
- **Dependencies**: Only `aiohttp` or `httpx`

### 2. Screenshot Service (`screenshot_service/playwright_capture.py`)
- **Why Second**: Core functionality, needed for visual validation
- **Implementation Strategy**:
  ```python
  class ScreenshotService:
      async def __aenter__(self):
          self._browser = await launch_browser()
          return self
          
      async def capture(self, url: str) -> PIL.Image:
          """Capture full-page screenshot."""
          page = await self._browser.new_page()
          # Returns: PIL.Image
  ```
- **Test Strategy**: Start with single source (CNN)
- **Dependencies**: `playwright`, `PIL`

### 3. Crop Rules (`crop_rules/`)
- **Why Third**: Needed for clean screenshots
- **Implementation Strategy**:
  ```python
  # crop_rules/cnn.py
  class CNNCropRules:
      def get_crop_dimensions(self, image: PIL.Image) -> Dict[str, int]:
          """Get crop coordinates for CNN."""
          return {
              "top": 100,
              "bottom": 800,
              "left": 0,
              "right": 1920
          }
  ```
- **Test Strategy**: Manual verification with CNN screenshots
- **Dependencies**: `PIL`, screenshot service

### 4. Headline Extractors (`extractors/`)
- **Why Fourth**: Can develop independently with static HTML
- **Implementation Strategy**:
  ```python
  # extractors/cnn.py
  class CNNExtractor:
      async def extract(self, html: str) -> List[Dict]:
          """Extract headlines from CNN HTML."""
          soup = BeautifulSoup(html, 'html.parser')
          # Returns: List of headline dictionaries
  ```
- **Test Strategy**: 
  - Use saved HTML files
  - Manual verification
  - Unit tests with static content
- **Dependencies**: `beautifulsoup4`

### 5. S3 Service (`s3_service/`)
- **Why Fifth**: Can mock initially
- **Implementation Strategy**:
  ```python
  class S3Service:
      def __init__(self, mock: bool = False):
          self.storage = MockS3() if mock else RealS3()
          
      async def upload(self, image: PIL.Image, key: str) -> str:
          """Upload image to S3 or mock storage."""
          # Returns: URL string
  ```
- **Test Strategy**:
  - Start with local file system
  - Mock S3 for testing
  - Transition to real S3
- **Dependencies**: `boto3`, temp directory for mocks

### 6. DB Service (`db_service/`)
- **Why Last**: Can develop with local DB
- **Implementation Strategy**:
  ```python
  class DBService:
      def __init__(self):
          self.client = MongoClient(get_config().mongodb['uri'])
          
      async def save_snapshot(self, data: Dict) -> ObjectId:
          """Save snapshot data to MongoDB."""
          # Returns: MongoDB ObjectId
  ```
- **Test Strategy**:
  - Use local MongoDB
  - Test with MongoDB Atlas free tier
  - Integration tests with test database
- **Dependencies**: `pymongo`, `motor`

### Development Guidelines

1. **Incremental Testing**
   - Build one source end-to-end first (CNN)
   - Add sources one at a time
   - Manual verification before automation

2. **Mocking Strategy**
   ```python
   # Example: Mock S3 for development
   class MockS3Storage:
       def __init__(self, tmp_dir: str = "/tmp/newslens"):
           self.tmp_dir = tmp_dir
           
       async def upload(self, image: PIL.Image, key: str) -> str:
           path = f"{self.tmp_dir}/{key}"
           image.save(path)
           return f"file://{path}"
   ```

3. **Validation Points**
   - Screenshot visual inspection
   - Headline text verification
   - Storage path validation
   - Document structure checks

4. **Integration Steps**
   - Start with single source
   - Add error handling
   - Add logging
   - Add remaining sources


