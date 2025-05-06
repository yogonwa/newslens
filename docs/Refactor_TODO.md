# NewsLens Scraper Refactor TODO

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
- [ ] Allow logs to be written to a file or external system for long-term retention.
- [ ] Optionally output a JSON or CSV summary of the run for downstream automation.
- [ ] Add enhanced validation for extracted headlines and for S3/DB operation integrity.
- [ ] Integrate with monitoring/alerting tools for high failure rates or performance issues.
- [ ] Complete documentation and runbooks for CLI, logging, and error handling.

## Architectural Improvements (TODO)
- [ ] Refactor Playwright page loading and capture logic into a dedicated service or utility (e.g., PageCaptureService) for better modularity and testability.
- [ ] Implement batch/concurrent processing using asyncio semaphores or task groups to improve throughput and scalability.
- [ ] Add structured logging and retry logic to all major pipeline steps for improved observability and robustness.

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
- Refactor backend to use a single, explicit environment loader as described above.
- Ensure backend/api/main.py (or main entrypoint) loads .env from the project root before any other imports.
- Remove all other load_dotenv() calls from backend/services and backend/config.
- Update all services to use config objects, not os.environ directly.
- Validate and document all required environment variables.
- Backend server is currently broken due to environment variable loading issues—address this as a priority before further development.

## Environment Variable Management Cleanup (TODO)
- [ ] Audit all modular libraries and their tests to ensure they do not load `.env` or access `os.environ` directly (except via `get_config()`).
- [ ] For any scripts or test files that need to be run standalone, add a top-of-file `.env` loader or use a test setup fixture as appropriate.
