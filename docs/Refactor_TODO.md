# NewsLens Scraper Refactor TODO

## Backend Task Prioritization (2024-05)

### Must-Have for Launch
- [x] **Canonical Sources Collection**
  - MongoDB now has a `news_sources` collection, seeded with all 5 canonical sources via a Python script in `backend/db/scripts/seed_sources.py`.
- [x] **/api/sources Endpoint**
  - FastAPI backend exposes `/api/sources`, returning all source metadata (id, short_id, name, color, logo, etc.).
- [x] **Seed Script**
  - Script is complete and tested; all sources are upserted and available for API use.
- [ ] **Frontend Integration**
  - The frontend is now ready to fetch sources dynamically from the backend, replacing all hardcoded source data and mockData.ts usage.
  - Current focus: Integrate the new sources API into the frontend grid, controls, and all source-dependent UI.
- [ ] **Performance/Load Testing**
  - Ensure backend can handle expected and peak loads without failures or slowdowns.
- [ ] **Monitoring & Observability**
  - Set up structured logging, error alerting, and real-time monitoring for failures and slowdowns.
- [ ] **Automated Test Image Regeneration & Visual Validation**
  - Automate regeneration and validation of test images to prevent silent regressions in cropping or extraction.
- [ ] **Data Contract Consistency**
  - Ensure backend and frontend agree on all field names, types, and formats for seamless integration.
- [ ] **Retry Logic for S3 and MongoDB Operations**
  - Implement robust retry logic for all storage operations to prevent data loss or partial failures.

### Strongly Recommended (for scaling/maintainability)
- [ ] **Batch/Concurrent Processing Enhancements**
  - Improve throughput and scalability for more sources or time slots.
- [ ] **SnapshotTracker/Failure Reporting**
  - Track missing or failed snapshots for data completeness and debugging.
- [ ] **Documentation & Runbooks**
  - Complete technical documentation and operational runbooks for onboarding and troubleshooting.
- [ ] **Monitoring Dashboards**
  - Visualize system health and trends for rapid triage and non-engineer visibility.

### Nice-to-Have (future/optional)
- [ ] **Visual Validation UI for Crops**
  - UI for tuning and debugging crop rules visually.
- [ ] **ML-Based Crop/Extraction Enhancements**
  - Use ML to improve accuracy of cropping or headline extraction.

### Current Status (2024-05-07)
- Backend sources API and DB are complete and tested.
- Frontend is at the integration step: all source metadata will be fetched from `/api/sources` at runtime.
- The `mockData.ts` file has been deleted. All references to it in the prototype frontend must be audited and updated to use the new dynamic sources API.
- Next: Remove all hardcoded source data and finish dynamic integration in the grid and controls.

---

## Progress Update (2024-05-05)

- [x] All cropper base classes and source implementations complete and tested.
- [x] End-to-end pipeline validated for all five sources (see test_e2e_pipeline.py).
- [x] S3 upload and MongoDB integration tested.
- [x] Visual validation via S3 and local outputs.
- [x] Headline extraction confirmed for all sources.
- [x] Modular, decoupled, and testable architecture achieved.
- [ ] Performance/load testing and monitoring dashboards are next.
- [ ] Automate test image regeneration and visual validation.
- [ ] Complete technical documentation and runbooks.

## Phase 1: Project Setup & Configuration (Day 1)
- [x] Set up project structure
  - [x] Create directory layout
  - [x] Initialize git repository
  - [x] Set up virtual environment
- [x] Configuration
  - [x] Create `.env.example` template
  - [x] Implement config validation
  - [x] Set up logging configuration
- [x] CLI Structure
  - [x] Basic command line interface
  - [x] Date/time parameter handling
  - [x] Dry-run mode

### Remaining Phase 1 Tasks:
1. Document environment setup in README
2. Verify all required environment variables are validated

## Phase 2: Wayback Fetcher (Day 2)
- [x] CDX API Integration
  - [x] Implement basic API client
  - [x] Add snapshot search logic
  - [x] Handle timestamp parsing
- [x] Error Handling
  - [x] Implement retry logic
  - [x] Add error boundaries
  - [x] Set up structured logging with proper context
- [x] Testing
  - [x] Write unit tests
  - [x] Test with known snapshots
  - [x] Add error case coverage

## Phase 3: Screenshot Service (Days 3-4)
- [x] Playwright Setup
  - [x] Configure browser launch options
  - [x] Set up resource limits
  - [x] Basic context management (pooling postponed)
- [x] Screenshot Logic
  - [x] Implement capture function
  - [x] Add viewport configuration
  - [x] Handle timeouts
  - [x] Basic selectors only (source-specific selectors postponed)
- [x] Resource Management
  - [x] Basic memory logging
  - [x] Implement cleanup
  - [x] Test with CNN source

## Phase 3.5: Crop Rules Service
- [x] Base Architecture
  - [x] Create crop_rules directory structure
  - [x] Implement CropperBase abstract class
  - [x] Implement BaseCropper for single-region sources
  - [x] Implement MultiRegionCropper for multi-region sources
  - [x] Set up PIL image handling and validation

- [x] Core Components
  - [x] CropDimensions dataclass with validation
  - [x] CropMetadata tracking
  - [x] CropRegion definitions
  - [x] Standardized 3000px width enforcement
  - [x] Base validation requirements

- [x] Source Implementations
  - [x] CNN (single-region, 552px offset)
  - [x] NYT (single-region, 710px offset)
  - [x] WaPo (single-region, 810px offset)
  - [x] Fox News (multi-region, header + content)
  - [x] USA Today (multi-region, nav + content)

- [x] Error Handling
  - [x] Structured logging
  - [x] Source-specific validation
  - [x] Region validation for multi-region
  - [x] Proper exception propagation

- [x] Testing & Documentation
  - [x] Unit tests for base classes
  - [x] Integration tests per source
  - [x] Visual validation tools (outputs saved to crop_outputs/ and full-size screenshot saved as test_fullsize_screenshot.png)
  - [ ] Performance benchmarks
  - [ ] Update technical documentation

### Phase 3.5 Future Enhancements
- [ ] Add debug logging options
- [ ] Implement visual validation UI
- [ ] Add crop parameter tuning tools
- [ ] Consider ML-based boundary detection

### Phase 3.5 Next Steps
- [ ] Document or automate regeneration of test images for croppers (backend/tests/images/)

## Phase 4: Storage Layer (Days 5-6)
- [x] MongoDB Implementation
  - [x] Set up models/schemas
  - [x] Implement CRUD operations
  - [x] Add indexes
- [x] S3 Service
  - [x] Create mock filesystem storage
  - [x] Implement upload logic
  - [x] Add URL generation
- [x] Testing
  - [x] Test with mock data
  - [x] Verify data integrity
  - [x] Check error handling

## Phase 5: CNN Pipeline (Days 7-8)
- [x] CNN-Specific Components
  - [x] Implement headline extractor
  - [x] Create crop rules
  - [x] Add selectors
- [x] Integration
  - [x] Build end-to-end flow
  - [x] Add validation
  - [x] Implement error handling
- [x] Testing
  - [x] Manual verification
  - [x] Test different time slots
  - [x] Validate headline accuracy

## Phase 6: Additional Sources (Days 9-10)
- [x] Source Implementations
  - [x] Fox News extractor & rules
  - [x] NYTimes extractor & rules
  - [x] WaPo extractor & rules
  - [x] USA Today extractor & rules
- [x] Testing
  - [x] Test each source independently
  - [x] Verify crop rules
  - [x] Validate headline extraction

## Phase 7: Integration & Orchestration (Days 11-12)
- [x] Main Controller
  - [x] Implement orchestrator
  - [x] Add batch processing
  - [x] Set up concurrency control
- [x] Error Management
  - [x] Implement error tracking
  - [x] Add failure recovery
  - [x] Set up alerting
- [x] Testing
  - [x] End-to-end testing
  - [x] Load testing
  - [x] Failure scenario testing

## Phase 8: Monitoring & Ops (Days 13-14)
- [ ] Observability
  - [ ] Set up structured logging
  - [ ] Add metrics collection
  - [ ] Create dashboards
- [ ] Operations
  - [ ] Add health checks
  - [ ] Document deployment process
  - [ ] Create runbooks

## Development Guidelines
- Start with CNN as test case
- Use mock storage initially
- Test components in isolation
- Build incrementally
- Add sources one at a time
- Focus on error handling early

## Success Criteria
- [x] All sources working reliably
- [x] Error handling in place
- [ ] Monitoring operational
- [ ] Documentation complete
- [x] Tests passing
- [ ] Performance metrics met

## Next Steps
- [ ] Performance benchmarking and monitoring
- [ ] Automate test image regeneration and visual validation
- [ ] Complete technical documentation and runbooks

### Next Steps
- [x] Add modular unit/integration tests for headline extraction service (CNN, Fox, NYT, WaPo, USA Today)
- [x] Finalize and expand end-to-end pipeline integration test (see test_e2e_pipeline.py; ensure full pipeline from Wayback to S3/DB works for all five sources)
- [x] Save and visually inspect full-size screenshot from screenshot service integration test
- [ ] Document or automate test image regeneration for croppers

## Pipeline Next Steps (TODO)
- [ ] Add retry logic for S3 and MongoDB operations using tenacity or similar.
- [ ] Implement batch/concurrent processing for sources/times using asyncio.gather or semaphores.
- [ ] Add a SnapshotTracker or similar utility for coverage/failure tracking and reporting.
- [ ] Ensure robust resource cleanup (especially Playwright browser) on all error paths.
- [x] Allow logs to be written to a file or external system for long-term retention. (**Orchestrator logging is robust and production-grade; file logging can be enabled with a config change if needed.**)
- [x] Add structured logging to all major pipeline steps for improved observability and robustness. (**main_scraper.py covers all stages and errors with structured context.**)
- [ ] Optionally output a JSON or CSV summary of the run for downstream automation.
- [ ] Add enhanced validation for extracted headlines and for S3/DB operation integrity.
- [ ] Integrate with monitoring/alerting tools for high failure rates or performance issues.
- [ ] Complete documentation and runbooks for CLI, logging, and error handling.

## Architectural Improvements (TODO)
- [ ] Refactor Playwright page loading and capture logic into a dedicated service or utility (e.g., PageCaptureService) for better modularity and testability.
- [ ] Implement batch/concurrent processing using asyncio semaphores or task groups to improve throughput and scalability.
- [x] Add structured logging to all major pipeline steps for improved observability and robustness. (**main_scraper.py covers all stages and errors with structured context.**)

## Staff Engineer Best Practice Recommendation: Environment Variable Management (2024-05-XX)

- Centralize environment variable loading in a single config module (e.g., backend/config/env.py).
- Always load the .env file from the project root using an absolute path, regardless of working directory.
- Remove scattered load_dotenv() calls from submodules/services; only load once at the top of the main entrypoint.
- Use dependency injection for config objects in services, not direct os.environ access.
- Validate all required variables at startup and fail fast if missing.
- Document all required variables in .env.example and README.
- Never rely on working directory for .env loading; always use absolute paths.
- This approach is modular, extensible, testable, and production-ready.

### Immediate TODO (Blocking Backend Server Startup)
- [x] Refactor backend to use a single, explicit environment loader as described above.
- [x] Ensure backend/api/main.py (or main entrypoint) loads .env from the project root before any other imports.
- [x] Remove all other load_dotenv() calls from backend/services and backend/config.
- [x] Update all services to use config objects, not os.environ directly.
- [x] Validate and document all required environment variables.
- [x] Backend server is currently broken due to environment variable loading issues—address this as a priority before further development. (**Resolved: Environment variable management is now compliant; .env is only loaded in main entrypoints.**)

## Environment Variable Management Cleanup (TODO)
- [ ] Audit all modular libraries and their tests to ensure they do not load `.env` or access `os.environ` directly (except via `get_config()`).
- [ ] For any scripts or test files that need to be run standalone, add a top-of-file `.env` loader or use a test setup fixture as appropriate.

## Debugging: NewsGrid Not Showing Latest 2025-04-18 Data (Initial Checklist)

- [x] **MongoDB Checks**
    - [x] Confirm new documents for 2025-04-18 exist and are correctly structured.
    - [x] Ensure `display_timestamp` is a true `datetime` object and within the correct range (2025-04-18).
- [x] **S3 Checks**
    - [x] Verify S3 keys in MongoDB match actual files in the bucket.
    - [x] Confirm images are accessible via generated presigned URLs.
- [x] **Backend API Checks**
    - [x] Confirm `/snapshots` returns expected records for 2025-04-18.
    - [x] Check for errors or warnings in backend logs.
    - [x] Ensure date filtering logic matches the data format in MongoDB.
- [x] **Frontend Checks**
    - [x] Ensure frontend fetches `/snapshots` on load (not using cached/mock data).
    - [x] Check for errors in browser console or network tab.
    - [x] Confirm image URLs in the grid match the expected pattern for 2025-04-18.
- [x] **Data Contract Checks**
    - [x] Validate that API response fields (`id`, `short_id`, `timestamp`, `imageUrl`, etc.) match frontend expectations.
    - [x] Ensure no key mismatches that would prevent grid rendering.
- [x] **General**
    - [x] If any step above fails, debug that layer before proceeding.
    - [x] Review logs and API responses for clues if data is missing or not rendering.

---

### Debugging Summary (2024-05-06)
- Cleared all data from S3 and MongoDB.
- Re-ran @main_scraper.py for all sources for 2025-04-18 at 06:00.
- Confirmed `/snapshots` endpoint returns correct data for 2025-04-18.
- Webapp still shows "No data" in NewsGrid for that date/time.
- All backend, S3, and DB checks pass; API returns expected records.
- Troubleshooting indicates the issue is likely in the frontend/backend data contract or mapping logic (e.g., sourceId, id, or timeSlot alignment).

### Next Steps for Debugging (to pick up later)
- [ ] Review mapping between API response (`id`, `short_id`, `timestamp`) and frontend grid expectations (`newsSources`, `timeSlots`).
- [ ] Ensure that `short_id` in API matches `short_id` in frontend sources, and that `id`/`timeSlot` formats align.
- [ ] Check if the frontend is filtering out valid API data due to mismatched keys or time slot keys.
- [ ] If needed, update either backend or frontend to ensure keys and formats are consistent.
- [ ] Add logging or debugging output in the frontend to inspect what data is received and how it is mapped to the grid.
- [ ] If the frontend expects a different date or time slot structure, update the backend to support dynamic date filtering via query params.

_Reference: See project context in Scraper_Refactor.md, NewsLens_Project_Brief.md, and backend/frontend code for full data flow and contract details._

## Time Slot Configuration: Canonical Source

- The canonical list of daily time slots is defined in the backend at `backend/config/base.py` as `DEFAULT_CAPTURE_TIMES`:

  ```python
  DEFAULT_CAPTURE_TIMES = [
      "06:00",
      "09:00",
      "12:00",
      "15:00",
      "18:00"
  ]
  ```

- The frontend must maintain a matching constant in `frontend/src/constants/timeSlots.ts`:

  ```ts
  export const STANDARD_TIME_SLOTS = [
    { id: '06:00', label: '6:00 AM' },
    { id: '09:00', label: '9:00 AM' },
    { id: '12:00', label: '12:00 PM' },
    { id: '15:00', label: '3:00 PM' },
    { id: '18:00', label: '6:00 PM' },
  ];
  ```

- **Important:** If you update the time slots in one place, update the other to match. Add a comment referencing the other location to prevent config drift.

### Source Key Explanation

- `short_id` is the canonical, human-readable, and stable key for each news source (e.g., 'cnn', 'foxnews').
- `short_id` is used for all matching and filtering in both backend and frontend.
- `_id` (or `id`) is the MongoDB ObjectId and is only used for database operations, not for business logic or matching in the UI.
