# NewsLens Scraper Refactor TODO

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

- [ ] Testing & Documentation
  - [ ] Unit tests for base classes
  - [ ] Integration tests per source
  - [ ] Visual validation tools
  - [ ] Performance benchmarks
  - [ ] Update technical documentation

### Phase 3.5 Future Enhancements
- [ ] Add debug logging options
- [ ] Implement visual validation UI
- [ ] Add crop parameter tuning tools
- [ ] Consider ML-based boundary detection

## Phase 4: Storage Layer (Days 5-6)
- [ ] MongoDB Implementation
  - [ ] Set up models/schemas
  - [ ] Implement CRUD operations
  - [ ] Add indexes
- [ ] S3 Service
  - [ ] Create mock filesystem storage
  - [ ] Implement upload logic
  - [ ] Add URL generation
- [ ] Testing
  - [ ] Test with mock data
  - [ ] Verify data integrity
  - [ ] Check error handling

## Phase 5: CNN Pipeline (Days 7-8)
- [ ] CNN-Specific Components
  - [ ] Implement headline extractor
  - [ ] Create crop rules
  - [ ] Add selectors
- [ ] Integration
  - [ ] Build end-to-end flow
  - [ ] Add validation
  - [ ] Implement error handling
- [ ] Testing
  - [ ] Manual verification
  - [ ] Test different time slots
  - [ ] Validate headline accuracy

## Phase 6: Additional Sources (Days 9-10)
- [ ] Source Implementations
  - [ ] Fox News extractor & rules
  - [ ] NYTimes extractor & rules
  - [ ] WaPo extractor & rules
  - [ ] USA Today extractor & rules
- [ ] Testing
  - [ ] Test each source independently
  - [ ] Verify crop rules
  - [ ] Validate headline extraction

## Phase 7: Integration & Orchestration (Days 11-12)
- [ ] Main Controller
  - [ ] Implement orchestrator
  - [ ] Add batch processing
  - [ ] Set up concurrency control
- [ ] Error Management
  - [ ] Implement error tracking
  - [ ] Add failure recovery
  - [ ] Set up alerting
- [ ] Testing
  - [ ] End-to-end testing
  - [ ] Load testing
  - [ ] Failure scenario testing

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
- [ ] All sources working reliably
- [ ] Error handling in place
- [ ] Monitoring operational
- [ ] Documentation complete
- [ ] Tests passing
- [ ] Performance metrics met
